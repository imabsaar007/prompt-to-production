import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize the model
model = SentenceTransformer('all-MiniLM-L6-v2')

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

client = Groq(api_key=my_api_key)
# Note: Ensure "openai/gpt-oss-120b" is a valid model ID or fallback to standard models like "llama3-8b-8192"
groq_model = "openai/gpt-oss-120b" 

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Split paragraph into a list of individual sentences
sentences = [
    "Morning runs in the local park offer a peaceful start to the quiet day.",
    "As the sun rises over the trees, the cool air fills my lungs with refreshing energy.",
    "My favorite path winds near the lake where small birds chirp in the branches.",
    "Moving at a steady pace helps clear my mind of any upcoming stress or worries.",
    "By the time I finish, my body feels strong and ready for the challenges ahead."
]

# Generate an array of embeddings (one for each sentence)
document_embeddings = model.encode(sentences)

def retrieve_info(qembedding, sentences, sentence_embeddings):
    scores = []
    for i, doc_emb in enumerate(sentence_embeddings):
        score = cosine_similarity(qembedding, doc_emb)
        scores.append((score, sentences[i]))
    
    # Sort by score in descending order
    scores.sort(reverse=True, key=lambda x: x[0])
    return scores[0]  # Return the top matching tuple: (score, text)

# --- ADDED: ask_llm Function ---
def ask_llm(query, context):
    """
    Sends the user query and the retrieved context to Groq to generate a final answer.
    """
    prompt = f"""You are a helpful assistant. Use the provided Context to answer the Question.
If the answer cannot be directly found in the Context, use it to infer the best response.

Context:
{context}

Question:
{query}

Answer:"""

    try:
        completion = client.chat.completions.create(
            model=groq_model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2, # Low temperature for accurate, fact-based answers
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred while calling the Groq API: {e}"


# --- Execution Flow ---
query = "At what time you should poop?"
query_embedding = model.encode(query)

# 1. Retrieve the single most relevant sentence
relevant_score, relevant_text = retrieve_info(query_embedding, sentences, document_embeddings)

print(f"--- Retrieval Step ---")
print(f"Highest Similarity Score: {relevant_score:.4f}")
print(f"Retrieved Context: \"{relevant_text}\"\n")

# 2. Pass query and retrieved context to the LLM
print(f"--- LLM Generation Step ---")
llm_answer = ask_llm(query, relevant_text)
print(f"LLM Answer: {llm_answer}")
