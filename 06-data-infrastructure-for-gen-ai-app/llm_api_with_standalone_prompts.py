import os

from google import genai
from google.genai import types


# GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"


def ask_gemini(client, model: str = "gemini-2.0-flash-001", prompt: str = ""):
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        # config=types.GenerateContentConfig(
        #     system_instruction=[
        #         "You are a bad manager.",
        #         "Your mission is to get people work in the office."
        #     ]
        # ),
    )
    return response.text


# Set up a Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Standalone prompt (or prompt without context)
question = "What are the benefits of remote work?"
response = ask_gemini(client, prompt=question)

print(response)
