import os
from dotenv import load_dotenv
from groq import Groq

# Load variables from .env
load_dotenv()

# Create Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Make LLM call
response = client.chat.completions.create(
    model="llama-3.3-70b-instant",
    messages=[
        {
            "role": "user",
            "content": "Hello! Tell me a short joke."
        }
    ]
)

# Print response
print(response.choices[0].message.content)