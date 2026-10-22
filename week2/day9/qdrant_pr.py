import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

# 1. Setup and Initialization
load_dotenv()
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
my_api_key = os.getenv("GROQ_API_KEY")  

if not my_api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

# Initialize all clients
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
groq_client = Groq(api_key=my_api_key)
embed_model = SentenceTransformer("all-MiniLM-L6-v2") # 384 dimensions

COLLECTION_NAME = "corporate_knowledge"
EMBEDDING_DIM = 384  # Dimension size for all-MiniLM-L6-v2

# 2. Recreate Qdrant Collection
if client.collection_exists(collection_name=COLLECTION_NAME):
    client.delete_collection(collection_name=COLLECTION_NAME)

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
)

# 3. Read and Process knowledge.txt
kb_path = Path("knowledge.txt")
if not kb_path.exists():
    raise FileNotFoundError("Please create a 'knowledge.txt' file in this directory.")

# Read text and split by sentences/lines (Fixed file mode to "r")
with open(kb_path, "r", encoding="utf-8") as f:
    raw_text = f.read().strip()
    documents = [sent.strip() for sent in raw_text.split(".") if sent.strip()]

# 4. Generate Embeddings & Upsert to Vector DB
points = []
for idx, doc in enumerate(documents):
    # Re-append the period stripped during split for cleaner output
    full_sentence = doc + "." 
    embedding = embed_model.encode(full_sentence).tolist()
    
    points.append(
        PointStruct(
            id=idx,
            vector=embedding,
            payload={"text": full_sentence}
        )
    )

client.upsert(collection_name=COLLECTION_NAME, points=points)
print(f"Successfully indexed {len(points)} sentences from knowledge.txt.")

# 5. RAG Retrieval Step (Updated to query_points)
query = "How do corporations protect their proprietary innovations?"
query_vector = embed_model.encode(query).tolist()

search_results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=2  # Top 2 most relevant sentences
)

# Extract retrieved text segments from points array
context_str = " ".join([hit.payload["text"] for hit in search_results.points])
print(f"\n[Retrieved Context]: {context_str}\n")

# 6. Generation Step via Groq
system_prompt = (
    "You are a helpful corporate assistant. Answer the user's question "
    "using ONLY the provided context. If the answer cannot be found in the context, "
    "say 'I do not know'."
)

user_prompt = f"Context: {context_str}\n\nQuestion: {query}"

chat_completion = groq_client.chat.completions.create(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    model="openai/gpt-oss-20b",  # Standard fast Groq model
    temperature=0.0,
)

print("[Groq LLM Response]:")
print(chat_completion.choices[0].message.content)
