import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
model = SentenceTransformer('all-MiniLM-L6-v2')
v1 = "Machine Learning is full of fun"
v2 = "Machine Learning is a fascinating field"
embedding1 = model.encode(v1)
embedding2 = model.encode(v2)
similarity = cosine_similarity(embedding1, embedding2)
print(similarity)