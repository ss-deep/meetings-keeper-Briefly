import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
def summary_generator(text):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Summarize the text with key points, {text}",
            }
        ],
        model="llama3-70b-8192",
    )
    return (chat_completion.choices[0].message.content)