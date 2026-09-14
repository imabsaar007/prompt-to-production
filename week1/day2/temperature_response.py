import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    temperature=0.1, 
    messages=[
        {
            "role": "system",
            "content": " Names with description."
        },
        {
            "role": "user",
            "content": "Name me what should i name my startups"
        }
    ]
)
print(response.choices[0].message.content)