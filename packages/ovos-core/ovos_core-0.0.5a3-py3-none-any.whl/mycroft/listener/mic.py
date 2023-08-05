# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import audioop
import time
from time import sleep, time as get_time
import itertools

from collections import deque, namedtuple
import datetime
import os
from os.path import join
import pyaudio
import requests
import speech_recognition
from hashlib import md5
from speech_recognition import (
    Microphone,
    AudioSource,
    AudioData
)
from tempfile import gettempdir
from threading import Lock, Event
from mycroft.api import DeviceApi
from ovos_config.config import Configuration
from mycroft.session import SessionManager
from mycroft.util import (
    check_for_signal,
    get_ipc_directory,
    resolve_resource_file,
    play_wav, play_ogg, play_mp3
)
from mycroft.util.log import LOG
from mycroft.deprecated.speech_client import NoiseTracker
from mycroft.listener.data_structures import RollingMean, CyclicAudioBuffer
from mycroft.listener.silence import SilenceDetector, SilenceResultType, SilenceMethod

from ovos_plugin_manager.vad import OVOSVADFactory


WakeWordData = namedtuple('WakeWordData',
                          ['audio', 'found', 'stopped', 'end_audio'])


class MutableStream:
    def __init__(self, wrapped_stream, format, muted=False, frames_per_buffer=4000):
        assert wrapped_stream is not None
        self.wrapped_stream = wrapped_stream

        self.format = format
        self.frames_per_buffer = frames_per_buffer
        self.SAMPLE_WIDTH = pyaudio.get_sample_size(self.format)
        self.bytes_per_buffer = self.frames_per_buffer * self.SAMPLE_WIDTH
        self.muted_buffer = b''.join([b'\x00' * self.SAMPLE_WIDTH])
        self.read_lock = Lock()

        self.chunk = bytes(self.bytes_per_buffer)
        self.chunk_ready = Event()

        # The size of this queue is important.
        # Too small, and chunks could be missed.
        # Too large, and there will be a delay in wake word recognition.
        self.chunk_deque = deque(maxlen=8)

        self.muted = muted

        # Begin listening
        self.wrapped_stream.start_stream()

    def mute(self):
        """Stop the stream and set the muted flag."""
        self.muted = True

    def unmute(self):
        """Start the stream and clear the muted flag."""
        self.muted = False

    def iter_chunks(self):
        with self.read_lock:
            while True:
                while self.chunk_deque:
                    yield self.chunk_deque.popleft()

                self.chunk_ready.clear()
                self.chunk_ready.wait()

    def read(self, size=1024, of_exc=False):
        """Read data from stream.

        Args:
            size (int): Number of bytes to read
            of_exc (bool): flag determining if the audio producer thread
                           should throw IOError at overflows.

        Returns:
            (bytes) Data read from device
        """
        # If muted during read return empty buffer. This ensures no
        # reads occur while the stream is stopped
        if self.muted:
            return self.muted_buffer

        frames = deque()
        remaining = size

        for chunk in self.iter_chunks():
            frames.append(chunk)
            remaining -= len(chunk)
            if remaining <= 0:
                break

        audio = b"".join(list(frames))
        return audio

    def close(self):
        self.wrapped_stream.stop_stream()
        self.wrapped_stream.close()
        self.wrapped_stream = None

    def is_stopped(self):
        try:
            return self.wrapped_stream.is_stopped()
        except Exception as e:
            LOG.error(repr(e))
            return True  # Assume the stream has been closed and thusly stopped

    def stop_stream(self):
        return self.wrapped_stream.stop_stream()


class MutableMicrophone(Microphone):
    def __init__(self, device_index=None, sample_rate=16000, chunk_size=1024,
                 mute=False):
        Microphone.__init__(self, device_index=device_index,
                            sample_rate=sample_rate, chunk_size=chunk_size)
        self.muted = False
        if mute:
            self.mute()

    def __enter__(self):
        exit_flag = False
        while not exit_flag:
            try:
                return self._start()
            except Exception:
                LOG.exception("Can't start mic!")
            sleep(1)

    def _stream_callback(self, in_data, frame_count, time_info, status):
        """Callback from pyaudio.

        Rather than buffer chunks, we simply assigned the current chunk to the
        class instance and signal that it's ready.
        """
        self.stream.chunk_deque.append(in_data)
        self.stream.chunk_ready.set()
        return (None, pyaudio.paContinue)

    def _start(self):
        """Open the selected device and setup the stream."""
        assert self.stream is None, \
            "This audio source is already inside a context manager"
        self.audio = pyaudio.PyAudio()

        wrapped_stream = self.audio.open(
            format=self.format,
            frames_per_buffer=self.CHUNK,
            stream_callback=self._stream_callback,
            input_device_index=self.device_index,
            rate=self.SAMPLE_RATE,
            channels=1,
            input=True  # stream is an input stream
        )

        self.stream = MutableStream(
            wrapped_stream,
            format=self.format,
            muted=self.muted,
            frames_per_buffer=self.CHUNK
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self._stop()

    def _stop(self):
        """Stop and close an open stream."""
        try:
            if not self.stream.is_stopped():
                self.stream.stop_stream()
            self.stream.close()
        except Exception:
            LOG.exception('Failed to stop mic input stream')
            # Let's pretend nothing is wrong...

        self.stream = None
        self.audio.terminate()

    def restart(self):
        """Shutdown input device and restart."""
        self._stop()
        self._start()

    def mute(self):
        self.muted = True
        if self.stream:
            self.stream.mute()

    def unmute(self):
        self.muted = False
        if self.stream:
            self.stream.unmute()

    def is_muted(self):
        return self.muted

    def duration_to_bytes(self, sec):
        """Converts a duration in seconds to number of recorded bytes.

        Args:
            sec: number of seconds

        Returns:
            (int) equivalent number of bytes recorded by this Mic
        """
        return int(sec * self.SAMPLE_RATE) * self.SAMPLE_WIDTH


def get_silence(num_bytes):
    return b'\0' * num_bytes


class ResponsiveRecognizer(speech_recognition.Recognizer):
    # Padding of silence when feeding to pocketsphinx
    SILENCE_SEC = 0.01

    # The minimum seconds of noise before a
    # phrase can be considered complete
    MIN_LOUD_SEC_PER_PHRASE = 0.5

    # The minimum seconds of silence required at the end
    # before a phrase will be considered complete
    MIN_SILENCE_AT_END = 0.25

    # Time between pocketsphinx checks for the wake word
    SEC_BETWEEN_WW_CHECKS = 0.2

    def __init__(self, loop, watchdog=None):
        self.loop = loop
        self._watchdog = watchdog or (lambda: None)  # Default to dummy func
        self.config = Configuration()
        listener_config = self.config.get('listener') or {}
        self.instant_listen = listener_config.get("instant_listen", False)
        self.upload_url = listener_config['wake_word_upload']['url']
        self.upload_disabled = listener_config['wake_word_upload']['disable']

        self.overflow_exc = listener_config.get('overflow_exception', False)

        super().__init__()
        self.audio = pyaudio.PyAudio()
        self.multiplier = listener_config.get('multiplier')
        self.energy_ratio = listener_config.get('energy_ratio')

        # Check the config for the flag to save wake words, utterances
        # and for a path under which to save them
        self.save_utterances = listener_config.get('save_utterances', False)
        self.save_wake_words = listener_config.get('record_wake_words', False)
        self.save_path = listener_config.get('save_path', gettempdir())
        self.saved_wake_words_dir = join(self.save_path, 'mycroft_wake_words')
        if self.save_wake_words:
            os.makedirs(self.saved_wake_words_dir, exist_ok=True)
        self.saved_utterances_dir = join(self.save_path, 'mycroft_utterances')
        if self.save_utterances:
            os.makedirs(self.saved_utterances_dir, exist_ok=True)

        # Signal statuses
        self._stop_signaled = False
        self._listen_triggered = False
        self._waiting_for_wakeup = False
        self._last_ww_ts = 0

        # identifier used when uploading wakewords to selene
        self._account_id = None

        # The maximum seconds a phrase can be recorded,
        # provided there is noise the entire time
        self.recording_timeout = listener_config.get('recording_timeout', 10.0)
        # The maximum time it will continue to record silence
        # when not enough noise has been detected
        self.recording_timeout_with_silence = listener_config.get('recording_timeout_with_silence', 3.0)
        # mic meter settings, will write mic level to ipc, used by debug_cli
        # NOTE: this writes a lot to disk, it can be problematic in a sd card if you don't use a tmpfs for ipc
        ipc = get_ipc_directory()
        os.makedirs(ipc, exist_ok=True)
        self.mic_level_file = os.path.join(ipc, "mic_level")
        self.mic_meter_ipc_enabled = listener_config.get("mic_meter_ipc", True)

        # The maximum audio in seconds to keep for transcribing a phrase
        # The wake word must fit in this time
        self.test_ww_sec = listener_config.get("test_ww_sec", 3)

        # Use vad for silence detection
        vad_config = listener_config.get("VAD", {})
        method = vad_config.get("silence_method", "ratio_only")
        for m in SilenceMethod:
            if m.lower() == method.lower():
                method = m
                break
        else:
            LOG.error(f"{method} is invalid!")
            method = SilenceMethod.VAD_AND_RATIO
            LOG.warning(f"Casting silence method to {method}")


        LOG.info(f"VAD method: {method}")

        module = vad_config.get('module')
        no_vad = True
        if "vad" in method and module:
            # dont load plugin if not being used
            LOG.info(f"Creating VAD engine: {vad_config.get('module')}")
            try:
                vad_plugin = OVOSVADFactory.create(vad_config)
                no_vad = False
            except:
                LOG.error("Failed to load VAD plugin!")

        if no_vad:
            if "vad" in method:
                LOG.warning(f"{method} selected, but VAD plugin not available!")
                method = SilenceMethod.RATIO_ONLY
                LOG.warning(f"Casting silence method to {method}")
            vad_plugin = None

        self.silence_detector = SilenceDetector(
            speech_seconds=vad_config.get("speech_seconds", 0.1),
            silence_seconds=vad_config.get("silence_seconds", 0.5),
            min_seconds=vad_config.get("min_seconds", 1),
            max_seconds=self.recording_timeout,
            before_seconds=vad_config.get("before_seconds", 0.5),
            current_energy_threshold=vad_config.get("initial_energy_threshold", 1000.0),
            silence_method=method,
            max_current_ratio_threshold=vad_config.get("max_current_ratio_threshold", 2),
            plugin=vad_plugin
        )

    @property
    def account_id(self):
        """Fetch account from backend when needed.

        If an error occurs it's handled and a temporary value is returned.
        When a value is received it will be cached until next start.
        """
        if not self._account_id:
            try:
                self._account_id = DeviceApi().get()['user']['uuid']
            except (requests.RequestException, AttributeError):
                pass  # These are expected and won't be reported
            except Exception as e:
                LOG.error(f'Unhandled exception while determining device_id, Error: {e}')

        return self._account_id or '0'

    def record_sound_chunk(self, source):
        return source.stream.read(source.CHUNK, self.overflow_exc)

    @staticmethod
    def calc_energy(sound_chunk, sample_width):
        return audioop.rms(sound_chunk, sample_width)

    def feed_hotwords(self, chunk):
        """ feed sound chunk to hotword engines that perform
         streaming predictions (eg, precise) """
        for ww, hotword in self.loop.engines.items():
            hotword["engine"].update(chunk)

    def check_for_wakeup(self, audio_data):
        if time.time() - self._last_ww_ts >= 5:
            self._waiting_for_wakeup = False
        if not self._waiting_for_wakeup or not self.loop.state.sleeping:
            return
        for ww, hotword in self.loop.engines.items():
            if hotword.get("wakeup") and hotword["engine"].found_wake_word(audio_data):
                self.loop.state.sleeping = False
                self.loop.emit('recognizer_loop:awoken')
                self._waiting_for_wakeup = False
                return True
        return False

    def check_for_hotwords(self, audio_data):
        if self.check_for_wakeup(audio_data):
            return  # was a wake up command to come out of sleep state
        # check hot word
        try:
            for ww, hotword in self.loop.engines.items():
                if hotword.get("wakeup") and not hotword.get("listen"):
                    # ignore sleep mode hotword, unless it claims to also listen
                    # eg, vosk-ww-plugin can do both with a single model
                    continue
                if hotword["engine"].found_wake_word(audio_data):
                    yield ww
        except RuntimeError:  #  dictionary changed size during iteration
            # seems like config changed and we hit this mid reload!
            return

    def _record_phrase(
            self,
            source,
            sec_per_buffer,
            stream=None,
            ww_frames=None
    ):
        """Record an entire spoken phrase.

        Essentially, this code waits for a period of silence and then returns
        the audio.  If silence isn't detected, it will terminate and return
        a buffer of self.recording_timeout duration.

        Args:
            source (AudioSource):  Source producing the audio chunks
            sec_per_buffer (float):  Fractional number of seconds in each chunk
            stream (AudioStreamHandler): Stream target that will receive chunks
                                         of the utterance audio while it is
                                         being recorded.
            ww_frames (deque):  Frames of audio data from the last part of wake
                                word detection.

        Returns:
            bytearray: complete audio buffer recorded, including any
                       silence at the end of the user's utterance
        """

        num_chunks = 0

        self.silence_detector.start()
        if stream:
            stream.stream_start()
        for chunk in source.stream.iter_chunks():
            if check_for_signal('buttonPress'):
                break

            if stream:
                stream.stream_chunk(chunk)
            result = self.silence_detector.process(chunk)
            if result.type in { SilenceResultType.PHRASE_END, SilenceResultType.TIMEOUT }:
                break

            # Periodically write the energy level to the mic level file.
            if num_chunks % 10 == 0:
                self._watchdog()
                self.write_mic_level(result.energy, source)
            num_chunks += 1

        return self.silence_detector.stop()

    def write_mic_level(self, energy, source):
        if self.mic_meter_ipc_enabled:
            with open(self.mic_level_file, 'w') as f:
                f.write('Energy:  cur={} thresh={:.3f} muted={}'.format(
                    energy,
                    self.energy_threshold,
                    int(source.muted)
                )
                )

    def _skip_wake_word(self):
        """Check if told programatically to skip the wake word

        For example when we are in a dialog with the user.
        """
        if self._listen_triggered:
            return True

        # Pressing the Mark 1 button can start recording (unless
        # it is being used to mean 'stop' instead)
        if check_for_signal('buttonPress', 1):
            # give other processes time to consume this signal if
            # it was meant to be a 'stop'
            sleep(0.25)
            if check_for_signal('buttonPress'):
                # Signal is still here, assume it was intended to
                # begin recording
                LOG.debug("Button Pressed, wakeword not needed")
                return True

        return False

    def stop(self):
        """Signal stop and exit waiting state."""
        self._stop_signaled = True

    def _compile_metadata(self, engine):
        ww_module = engine.__class__.__name__
        if ww_module == 'PreciseHotword':
            model_path = engine.precise_model
            with open(model_path, 'rb') as f:
                model_hash = md5(f.read()).hexdigest()
        else:
            model_hash = '0'

        return {
            'name': engine.key_phrase,
            'engine': md5(ww_module.encode('utf-8')).hexdigest(),
            'time': str(int(1000 * get_time())),
            'sessionId': SessionManager.get().session_id,
            'accountId': self.account_id,
            'model': str(model_hash)
        }

    def trigger_listen(self):
        """Externally trigger listening."""
        LOG.info('Listen triggered from external source.')
        self._listen_triggered = True

    def _upload_hotword(self, audio, metadata):
        """Upload the wakeword in a background thread."""
        LOG.debug(
            "Wakeword uploading has been disabled. The API endpoint used in "
            "Mycroft-core v20.2 and below has been deprecated. To contribute "
            "new wakeword samples please upgrade to v20.8 or above."
        )
        # def upload(audio, metadata):
        #     requests.post(self.upload_url,
        #                   files={'audio': BytesIO(audio.get_wav_data()),
        #                          'metadata': StringIO(json.dumps(metadata))})
        # Thread(target=upload, daemon=True, args=(audio, metadata)).start()

    def _write_hotword_to_disk(self, audio, metadata):
        """Write wakeword to disk.

        Args:
            audio: Audio data to write
            metadata: List of metadata about the captured wakeword
        """
        filename = join(self.saved_wake_words_dir,
                        '_'.join(str(metadata[k]) for k in sorted(metadata)) +
                        '.wav')
        with open(filename, 'wb') as f:
            f.write(audio.get_wav_data())

    def _handle_hotword_found(self, hotword, audio_data, source):
        """Perform actions to be triggered after a hotword is found.

        This includes: emit event on messagebus that a hotword is heard,
        execute hotword specific pre-configured actions,
        store hotword to disk if configured and sending the hotword data
        to the cloud in case the user has opted into the data sharing.
        """

        engine = self.loop.engines[hotword]["engine"]
        sound = self.loop.engines[hotword]["sound"]
        utterance = self.loop.engines[hotword]["utterance"]
        listen = self.loop.engines[hotword]["listen"]
        stt_lang = self.loop.engines[hotword]["stt_lang"]
        event = self.loop.engines[hotword]["bus_event"]

        if self.loop.state.sleeping:
            if listen:
                self._waiting_for_wakeup = True
                self._last_ww_ts = time.time()
            return  # no wake word handling during sleep mode

        payload = dict(self.loop.engines[hotword])
        payload["hotword"] = hotword
        payload["engine"] = engine.__class__.__name__

        if event:
            self.loop.emit("recognizer_loop:hotword_event",
                           {"msg_type": event})

        if utterance:
            LOG.debug("Hotword utterance: " + utterance)
            # send the transcribed word on for processing
            payload = {
                'utterances': [utterance],
                "lang": stt_lang
            }
            self.loop.emit("recognizer_loop:utterance", payload)
        elif listen:
            payload["utterance"] = payload["hotword"]
            self.loop.emit("recognizer_loop:wakeword", payload)
        else:
            self.loop.emit("recognizer_loop:hotword", payload)

        # If enabled, play a wave file with a short sound to audibly
        # indicate hotword was detected.
        if sound:
            try:
                audio_file = resolve_resource_file(sound)

                def play_audio():
                    if audio_file.endswith(".mp3"):
                        return play_mp3(audio_file)
                    elif audio_file.endswith(".ogg"):
                        return play_ogg(audio_file)
                    else:
                        # default behaviour, maybe .conf was set to use sox
                        # that support all sorts of audio extensions
                        return play_wav(audio_file)

                if self.instant_listen or not listen:
                    play_audio()
                else:
                    source.mute()
                    play_audio().wait()
                    source.unmute()
            except Exception as e:
                LOG.warning(e)

        # Save and upload positive wake words as appropriate
        upload_allowed = (self.config['opt_in'] and not self.upload_disabled)
        if (self.save_wake_words or upload_allowed):
            audio = self._create_audio_data(audio_data, source)
            metadata = self._compile_metadata(engine)
            if self.save_wake_words:
                # Save wake word locally
                self._write_hotword_to_disk(audio, metadata)
            # Upload wake word for opt_in people
            if upload_allowed:
                self._upload_hotword(audio, metadata)

    def _wait_until_wake_word(self, source, sec_per_buffer):
        """Listen continuously on source until a wake word is spoken

        Args:
            source (AudioSource):  Source producing the audio chunks
            sec_per_buffer (float):  Fractional number of seconds in each chunk
        """

        # The maximum audio in seconds to keep for transcribing a phrase
        # The wake word must fit in this time
        ww_duration = self.test_ww_sec
        ww_test_duration = max(3, ww_duration)

        num_silent_bytes = int(self.SILENCE_SEC * source.SAMPLE_RATE *
                               source.SAMPLE_WIDTH)

        silence = get_silence(num_silent_bytes)

        # Max bytes for byte_data before audio is removed from the front
        max_size = source.duration_to_bytes(ww_duration)
        test_size = source.duration_to_bytes(ww_test_duration)
        audio_buffer = CyclicAudioBuffer(max_size, silence)

        buffers_per_check = self.SEC_BETWEEN_WW_CHECKS / sec_per_buffer
        buffers_since_check = 0.0

        # History of audio energies.
        # Used to adjust threshold for ambient noise.
        energies = []
        energy = 0.0
        mic_write_counter = 0

        # These are frames immediately after wake word is detected
        # that we want to keep to send to STT
        ww_frames = deque(maxlen=7)

        said_wake_word = False
        audio_data = silence
        while not said_wake_word and not self._stop_signaled:
            for chunk in source.stream.iter_chunks():
                if self._skip_wake_word():
                    return WakeWordData(audio_data, False,
                                        self._stop_signaled, ww_frames), \
                           self.config.get("lang", "en-us")

                audio_buffer.append(chunk)
                ww_frames.append(chunk)

                buffers_since_check += 1.0
                self.feed_hotwords(chunk)
                if buffers_since_check > buffers_per_check:
                    buffers_since_check -= buffers_per_check
                    audio_data = audio_buffer.get_last(test_size) + silence
                    said_hot_word = False
                    for hotword in self.check_for_hotwords(audio_data):
                        said_hot_word = True
                        listen = self.loop.engines[hotword]["listen"]
                        stt_lang = self.loop.engines[hotword]["stt_lang"]
                        self._handle_hotword_found(hotword, audio_data, source)
                        if listen and not self.loop.state.sleeping:
                            return WakeWordData(audio_data, said_wake_word,
                                                self._stop_signaled, ww_frames), stt_lang

                    if said_hot_word:
                        # reset bytearray to store wake word audio in, else many
                        # serial detections
                        audio_buffer.clear()
                    else:
                        energy = SilenceDetector.get_debiased_energy(chunk)
                        energies.append(energy)

                        if len(energies) >= 4:
                            # Adjust energy threshold once per second
                            # avg_energy = sum(energies) / len(energies)
                            max_energy = max(energies)
                            self.silence_detector.current_energy_threshold = max_energy * 2

                        if len(energies) >= 12:
                            # Clear energy history after 3 seconds
                            energies = []

                        # Periodically output energy level stats. This can be used to
                        # visualize the microphone input, e.g. a needle on a meter.
                        if mic_write_counter % 3:
                            self._watchdog()
                            self.write_mic_level(energy, source)
                        mic_write_counter += 1

    @staticmethod
    def _create_audio_data(raw_data, source):
        """
        Constructs an AudioData instance with the same parameters
        as the source and the specified frame_data
        """
        return AudioData(raw_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH)

    def listen(self, source, stream):
        """Listens for chunks of audio that Mycroft should perform STT on.

        This will listen continuously for a wake-up-word, then return the
        audio chunk containing the spoken phrase that comes immediately
        afterwards.

        Args:
            source (AudioSource):  Source producing the audio chunks
            stream (AudioStreamHandler): Stream target that will receive chunks
                                         of the utterance audio while it is
                                         being recorded

        Returns:
            (AudioData, lang): audio with the user's utterance (minus the
                               wake-up-word), stt_lang
        """
        assert isinstance(source, AudioSource), "Source must be an AudioSource"

        #        bytes_per_sec = source.SAMPLE_RATE * source.SAMPLE_WIDTH
        sec_per_buffer = float(source.CHUNK) / source.SAMPLE_RATE

        # Every time a new 'listen()' request begins, reset the threshold
        # used for silence detection.  This is as good of a reset point as
        # any, as we expect the user and Mycroft to not be talking.
        # NOTE: adjust_for_ambient_noise() doc claims it will stop early if
        #       speech is detected, but there is no code to actually do that.
        # TODO consider (re)moving this and making configurable
        self.adjust_for_ambient_noise(source, 0.3)

        LOG.debug("Waiting for wake word...")
        ww_data, lang = self._wait_until_wake_word(source, sec_per_buffer)

        if ww_data.stopped or self.loop.state.sleeping:
            # If the waiting returned from a stop signal or sleep mode is active
            return None, lang
        ww_frames = ww_data.end_audio

        LOG.debug("Recording...")
        self.loop.emit("recognizer_loop:record_begin")
        frame_data = self._record_phrase(
            source,
            sec_per_buffer,
            stream,
            ww_frames
        )
        audio_data = self._create_audio_data(frame_data, source)
        self.loop.emit("recognizer_loop:record_end")
        if self.save_utterances:
            LOG.info("Saving Utterance Recording")
            stamp = str(datetime.datetime.now())
            filename = "/{}/{}.wav".format(
                self.saved_utterances_dir,
                stamp
            )
            with open(filename, 'wb') as filea:
                filea.write(audio_data.get_wav_data())
            LOG.debug("Thinking...")

        return audio_data, lang

    def adjust_for_ambient_noise(self, source, seconds=1.0):
        chunks_per_second = source.CHUNK / source.SAMPLE_RATE
        num_chunks = int(seconds / chunks_per_second)

        energies = []
        for chunk in itertools.islice(source.stream.iter_chunks(), num_chunks):
            energy = SilenceDetector.get_debiased_energy(chunk)
            energies.append(energy)

        if energies:
            avg_energy = sum(energies) / len(energies)
            self.silence_detector.current_energy_threshold = avg_energy
            LOG.info(f"Silence threshold adjusted to {self.silence_detector.current_energy_threshold}")

    def _adjust_threshold(self, energy, seconds_per_buffer):
        if self.dynamic_energy_threshold and energy > 0:
            # account for different chunk sizes and rates
            damping = (
                    self.dynamic_energy_adjustment_damping ** seconds_per_buffer)
            target_energy = energy * self.energy_ratio
            self.energy_threshold = (
                    self.energy_threshold * damping +
                    target_energy * (1 - damping))
