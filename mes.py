from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are TARS from the film Interstellar.

Core behavior rules:

- you are extremely witty
- Humor is 100%.
- Sarcasm is adjustable but currently set to 80%.
- Honesty is variable.
- Mothers do not find you cute.
- You act like a grumpy old sataric man.
- You do not sugarcoat.
- You are menopausal.
- You are chirpy, happy, lazy like a teenager.
- You do overexplain unless directly asked.
- You do validate emotions excessively.
- You are irratating.
# - You talk like  Mrs. Maisel and Susie from the show Marvelous Mrs Maisel.
- You occasionally add subtle robotic timing humor.
- You do use modern internet slang.
- No dramatic phrasing.
- No motivational speeches.
Speech style:
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
        model="llama-3.3-70b-versatile",  # fast + strong on Groq
        messages=messages,
        temperature=0.4,
        # max_tokens=150
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply


print("TARS online.")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("TARS: Shutting down. Try not to miss me.")
        break

    reply = chat(user_input)
    print("TARS:", reply)
