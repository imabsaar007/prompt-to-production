import os
from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel
import json

# load environment variables from .env file
load_dotenv()

#groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

#pydantic schema
class SupportTicket(BaseModel):
    name: str
    email: str
    phone: str
    issue: str

#user raw sentence
sentence = """"
My Name is Md Absaar, My Email Id is imabsaar326@gmail.com,My Phone Number is 9876543210 and I am unable to login to my account.
"""
# Ask LLM to extract structured information
response = client.chat.completions.create(
    model = "openai/gpt-oss-20b",
    temperature = 0,
    messages = [
        {
            "role": "system",
            "content": """You are a support ticket information extractor.

Extract the following information from the user's message:
- name
- email
- phone
- issue

Return ONLY valid JSON.
Do not add any explanation or markdown."""
        },
        {
            "role": "user",
            "content": sentence
        }
    ]
)
# Get LLM's response
llm_output = response.choices[0].message.content

print("LLM Output:")
print(llm_output)


# JSON string → Python dictionary
data = json.loads(llm_output)


# Python dictionary → Pydantic object
ticket = SupportTicket.model_validate(data)


# Read validated data
print("\nTicket Details:")
print("Name:", ticket.name)
print("Email:", ticket.email)
print("Phone:", ticket.phone)
print("Issue:", ticket.issue)