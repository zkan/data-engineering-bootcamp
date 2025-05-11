import os

import google.genai as genai
import numpy as np


def ask_gemini(client, prompt: str):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt,
    )
    return response.text


def get_embedding(client, text: str):
    result = client.models.embed_content(
        model="gemini-embedding-exp-03-07",
        contents=text,
    )
    return result.embeddings[0]


def cosine_similarity(vec1, vec2):
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
print(ask_gemini(client, "What are the benefits of remote work?"))

embedding = get_embedding(client, "Remote work allows employees to be more flexible and productive.")
print(embedding.values)

vec_q = get_embedding(client, "Hello").values
vec_c = get_embedding(client, "Hey").values

print("Similarity score:", cosine_similarity(vec_q, vec_c))