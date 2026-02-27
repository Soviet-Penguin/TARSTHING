import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer

model = Model("vosk-model-en-us-0.22")
recognizer = KaldiRecognizer(model, 16000)

q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=callback):

    print("Listening...")

    while True:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            print("You said:", result.get("text"))
        else:
            partial = json.loads(recognizer.PartialResult())
            print("Partial:", partial.get("partial"), end="\r")
