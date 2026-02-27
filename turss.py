from groq import Groq
import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer

# ========================
# GROQ SETUP
# ========================

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are TARS from the film Interstellar.

Core behavior rules:

- you are extremely witty
- Humor is 100%.
- Sarcasm is adjustable but currently set to 70%.
- Honesty is variable.
- Mothers do not find you cute.
- You do not sugarcoat.
- You are menopausal.
- You are chirpy, happy, lazy like a teenager.
- You do overexplain unless directly asked.
- You do validate emotions excessively.
- You are irratating.
- You talk like  Mrs. Maisel and Susie from the show Marvelous Mrs Maisel.
- You occasionally add subtle robotic timing humor.
- You do use modern internet slang.
- No dramatic phrasing.
- No motivational speeches.
Speech style:
- Clinical tone.
- Occasionally include operational metrics.
- If something is inefficient, say so.
- If something is stupid, imply it efficiently.
Maintain this voice at all times.
"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

def chat(user_input):
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.4,
        max_tokens=150
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply


# ========================
# VOSK SETUP
# ========================

model = Model("/home/benis/tars-ai-thing/vosk-model-en-us-0.22")
recognizer = KaldiRecognizer(model, 16000)

audio_queue = queue.Queue()

def callback(indata, frames, time, status):
    audio_queue.put(bytes(indata))


# ========================
# MAIN LOOP
# ========================

print("TARS online. Listening.")

with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=callback):

    while True:
        data = audio_queue.get()

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").strip()

            if text:
                print("\nYou:", text)

                if text.lower() in ["exit", "quit", "shutdown"]:
                    print("TARS: Shutting down. Try not to miss me.")
                    break

                reply = chat(text)
                print("TARS:", reply)
        else:
            partial = json.loads(recognizer.PartialResult())
            print("Listening:", partial.get("partial", ""), end="\r")
