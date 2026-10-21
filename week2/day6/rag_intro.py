import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=my_api_key)
if not my_api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")
client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"
knowledge_base = {
    "context" : "Md Absaar is a software engineer and data scientist known for his work in machine learning and artificial intelligence. He has contributed to various open-source projects and has a strong presence in the tech community.",
    "age" : "Md Absaar is 30 years old.",
    "education" : "Md Absaar holds a Master's degree in Computer Science from XYZ University."
}
def retrieve_info(question):
    question = question.lower()
    if "who is Md Absaar" in question:
        return knowledge_base["context"]
    elif "age" in question:
        return knowledge_base["age"]
    elif "education" in question:
        return knowledge_base["education"]
    else:
        return "I don't have information on that topic."
def ask_llm(question):
    context_info = retrieve_info(question)
    sys_prompt = f"""Only answer in one line, answer based on this context and do not hallucinate: {context_info}"""
    system_message = {
        "role": "system",
        "content": sys_prompt
    }
    message = {
        "role": "user",
        "content": question
    }
    messages = [system_message, message]
    response = client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    return answer
question = "What is Md Absaar's age"
print(ask_llm(question))