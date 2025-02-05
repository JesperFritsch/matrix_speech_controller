import pyaudio
import json
from importlib import resources
from vosk import Model, KaldiRecognizer

# Load the Vosk model
with resources.path("mtx_ctl.speech_models", "vosk-model-small-en-us-0.15") as model_path:
    model_file = str(model_path)

model = Model(model_file)
recognizer = KaldiRecognizer(model, 16000)
recognizer.SetMaxAlternatives(1)  # Optional: Can increase alternatives if needed
recognizer.SetWords(True)  # Enables word-level timestamps (optional)

# Initialize PyAudio
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

print("Listening...")

while True:
    data = stream.read(4096, exception_on_overflow=False)

    if recognizer.AcceptWaveform(data):
        # Get the full recognized phrase
        result = json.loads(recognizer.Result())
        print(f"Final: {result.get('text', '')}")
    else:
        # Get real-time streaming transcription
        partial_result = json.loads(recognizer.PartialResult())
        print(f"Partial: {partial_result.get('partial', '')}", end="\r")
