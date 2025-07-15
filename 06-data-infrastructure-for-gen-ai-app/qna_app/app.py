import os
import json

import pandas as pd
import streamlit as st
from google import genai
from google.genai import types
from google.cloud import bigquery
from google.oauth2 import service_account


GCP_PROJECT_ID = "YOUR_GCP_PROJECT_ID"
DATASET_ID = "YOUR_DATASET_ID"
TABLE_ID = "YOUR_TABLE_ID"
KEYFILE = "YOUR_KEYFILE"
# api_key = os.environ.get("GEMINI_API_KEY")
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"


def get_embedding(client, model: str = "gemini-embedding-exp-03-07", text: str = ""):
    result = client.models.embed_content(
        model=model,
        contents=text,
    )
    return result.embeddings[0]


def ask_gemini(client, model: str = "gemini-2.0-flash-001", prompt: str = ""):
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=[
                "You are a course recommender.",
                "Your mission is to recommend courses for people who want to upskill and switch careers."
            ]
        ),
    )
    return response.text


def search_similar_texts(client, vec):
    query = f"""
        SELECT
            base.text,
            distance
        FROM
        VECTOR_SEARCH(
            TABLE `{DATASET_ID}.{TABLE_ID}`,
            'embedding',
            (select {vec} as embedding),
            top_k => 3,
            distance_type => 'EUCLIDEAN'
        )
    """

    # Run the query
    query_job = client.query(query)

    # Get the results
    results = query_job.result()

    # Print the results
    similar_texts = []
    for row in results:
        similar_texts.append(row.text)

    return similar_texts


def main():
    st.title("Q&A App")

    user_question = st.text_input("Ask a question:")
    if user_question:
        with st.spinner("Cooking up a response... 🍳", show_time=True):
            # Example
            # user_question = "อยากทำสาย Data Engineer ควรเรียนคอร์สอะไรดี?"
            df = pd.DataFrame(data={
                "text": [
                    user_question,
                ]
            })

            # Set up a Gemini client
            genai_client = genai.Client(api_key=GEMINI_API_KEY)

            # Set up a BigQuery client
            service_account_info = json.load(open(KEYFILE))
            credentials = service_account.Credentials.from_service_account_info(service_account_info)
            bigquery_client = bigquery.Client(
                project=GCP_PROJECT_ID,
                credentials=credentials,
            )

            vec = get_embedding(genai_client, text=user_question).values
            similar_texts = search_similar_texts(bigquery_client, vec)

            # Create context by gathering results together
            context = " / ".join([each for each in similar_texts])

            prompt_with_context = f"""
            Context:
            {context}

            Question:
            {user_question}
            """
            response = ask_gemini(genai_client, prompt=prompt_with_context)

        st.subheader("AI Assistant:")
        st.write(response)


if __name__ == "__main__":
    main()