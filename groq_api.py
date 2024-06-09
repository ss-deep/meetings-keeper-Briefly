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
                "content": f"Generate self-explanatory and concise summaries with html tags, each topic. Use html tag to to make bold instead of '**' and html tag to print on new line. Refer to people's names whenever appropriate, and avoid metioning 'HTML tags' and 'each topic on a new line' in your response at the start. {text}"
            }
        ],
        model="llama3-70b-8192",
    )
    return (chat_completion.choices[0].message.content)