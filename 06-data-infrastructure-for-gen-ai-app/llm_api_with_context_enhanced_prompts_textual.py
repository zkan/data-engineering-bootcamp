import os

from google import genai
from google.genai import types


# GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"


def ask_gemini(client, model: str = "gemini-2.0-flash-001", prompt: str = ""):
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return response.text


# Set up a Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

context = """
Skooldio offers a full refund within 14 days of booking, provided no services have been consumed.
After 14 days, a 50% refund is possible upon review. Skooldio has a remote work policy but it has to
review on a case by case basis. Let's day if no meeting on that day, the employee can work from home.
"""

question = "What are the benefits of remote work?"

prompt_with_context = f"""
You are a helpful assistant. Use the following context to answer the question.

Context:
{context}

Question:
{question}
"""
response = ask_gemini(client, prompt=prompt_with_context)

print(response)
