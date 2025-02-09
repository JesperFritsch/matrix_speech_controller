import pyaudio
import json
import logging
import time
import sys

from pathlib import Path
from threading import Thread
from queue import Queue
from importlib import resources
from vosk import Model, KaldiRecognizer

log = logging.getLogger(Path(__file__).stem)

# Load the Vosk model
model_file = resources.files("mtx_ctl.speech_models").joinpath("vosk-model-small-en-us-0.15")
print(model_file)

class CommandListener:
    def __init__(self, activation_phrases, deactivation_phrases, model_file=model_file, active_timeout_sec=20):
        self._is_activated = False
        self._active_timeout_sec = active_timeout_sec
        self._activation_phrases = activation_phrases
        self._deactivation_phrases = deactivation_phrases
        self._last_active = 0
        self._cmd_queue: Queue = Queue()
        self._listen_thread: Thread = None
        self._model = Model(str(model_file))
        self._recognizer = KaldiRecognizer(self._model, 16000)
        self._recognizer.SetMaxAlternatives(1)  # Optional: Can increase alternatives if needed
        self._recognizer.SetWords(True)  # Enables word-level timestamps (optional)
        self._mic = pyaudio.PyAudio()
        print("Listening on mic", self._mic.get_default_input_device_info())
        self._is_running = True
        self._audio_stream = self._mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

    def _activate(self):
        log.info("Activating")
        self._keep_active()
        self._is_activated = True

    def _deactivate(self):
        log.info("Deactivating")
        self._is_activated = False
        self._register_command("reset_history")

    def _keep_active(self):
        self._last_active = time.time()

    def _is_active(self):
        if self._is_activated and self._active_timeout_sec:
            if time.time() - self._last_active > self._active_timeout_sec:
                self._deactivate()
        return self._is_activated

    def _register_command(self, cmd):
        log.info("registered: '%s'" % cmd)
        self._keep_active()
        self._cmd_queue.put(cmd)

    def start(self, queue):
        self._audio_stream.start_stream()
        self._listen_thread = Thread(target=self.listen, args=(queue,))
        self._listen_thread.daemon = True
        self._listen_thread.start()

    def stop(self):
        self._is_running = False
        self._listen_thread.join()

    def listen(self, queue):
        self._cmd_queue = queue
        self._is_running = True
        try:
            while self._is_running:
                data = self._audio_stream.read(8192, exception_on_overflow=False)

                if self._recognizer.AcceptWaveform(data):
                    # Get the full recognized phrase
                    result = json.loads(self._recognizer.Result())
                    cmd_text = result.get("text", "") or result.get("alternatives", [{}])[0].get("text", "")
                    if self._is_active() and cmd_text:
                        self._register_command(cmd_text)
                    if self._is_active() and any(x in cmd_text for x in self._deactivation_phrases):
                        self._deactivate()
                else:
                    # Get real-time streaming transcription
                    partial_result = json.loads(self._recognizer.PartialResult())
                    partial_cmd = partial_result.get('partial', '')
                    if not self._is_active() and any(x in partial_cmd for x in self._activation_phrases):
                        self._activate()
                    print(f"Partial: {partial_cmd}                                                              ", end="\r")
                    sys.stdout.flush()
        except KeyboardInterrupt:
            print("keyboard interrupt")
        except Exception as e:
            log.error(e, exc_info=True)

