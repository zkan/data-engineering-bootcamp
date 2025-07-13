import streamlit as st


def main():
    st.title("Q&A App")
    user_question = st.text_input("Ask a question:")
    if user_question:
        st.write(user_question)


if __name__ == "__main__":
    main()