import os

import google.genai as genai
import numpy as np


def ask_gemini(client, model: str = "gemini-2.0-flash-001", prompt: str = ""):
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return response.text


def get_embedding(client, model: str = "gemini-embedding-exp-03-07", text: str = ""):
    result = client.models.embed_content(
        model=model,
        contents=text,
    )
    return result.embeddings[0]


def cosine_similarity(vec1, vec2):
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Prompt without context
question = "What are the benefits of remote work?"
print(ask_gemini(client, prompt=question))

print("-" * 30)

# Prompt with naive context injection
context = """
BearCamp offers a full refund within 14 days of booking, provided no services have been consumed.
After 14 days, a 50% refund is possible upon review. BearCamp has no remote work policy.
"""

prompt_with_context = f"""
You are a helpful assistant. Use the following context to answer the question.

Context:
{context}

Question:
{question}
"""

print(ask_gemini(client, prompt=prompt_with_context))

print("-" * 30)

# Get embeddings
embedding = get_embedding(client, text="Remote work allows employees to be more flexible and productive.")
print(embedding.values)

vec_q = get_embedding(client, text="Hello").values
vec_c = get_embedding(client, text="Hey").values

print("Similarity score:", cosine_similarity(vec_q, vec_c))
