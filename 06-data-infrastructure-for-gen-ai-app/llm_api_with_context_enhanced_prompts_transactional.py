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
{
  "user_id": "12345",
  "current_account_balance": 850.25,
  "recent_transactions": [
    {
      "date": "2025-07-12",
      "amount": -150.00,
      "description": "Grocery Store - SuperMart",
      "type": "debit"
    },
    {
      "date": "2025-07-10",
      "amount": 2000.00,
      "description": "Salary - Acme Corp",
      "type": "credit"
    },
    {
      "date": "2025-07-08",
      "amount": -75.50,
      "description": "Electricity Bill",
      "type": "debit"
    }
  ],
  "active_credit_card": true,
  "credit_card_balance": 320.75,
  "upcoming_bills": [
    {
      "payee": "Internet Provider",
      "amount_due": 55.00,
      "due_date": "2025-07-15"
    }
  ]
}
"""

question = """
Based on the user's recent activity, what budget advice would you give them for the next 2 weeks?
Also, remind them of any upcoming bills."
"""

prompt_with_context = f"""
You are a helpful assistant. Use the following context to answer the question.

Context:
{context}

Question:
{question}
"""
response = ask_gemini(client, prompt=prompt_with_context)

print(response)
