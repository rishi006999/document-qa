import streamlit as st
from openai import OpenAI
import openai

# Function to validate the API key
def validate_api_key(key):
    try:
        openai.api_key = key
        openai.Engine.list()  # Test the key by making a simple request
        return True
    except Exception as e:
        st.error(f"Invalid API key: {e}")
        return False

# Show title and description
st.title("📄 Document question answering agent")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
)

# Ask user for their OpenAI API key via `st.text_input`
openai_api_key = st.text_input("OpenAI API Key", type="password")

# Validate the key immediately
if openai_api_key:
    if validate_api_key(openai_api_key):
        st.success("API key is valid!")
        
        # Create an OpenAI client
        client = OpenAI(api_key=openai_api_key)

        # Let the user upload a file via `st.file_uploader`
        uploaded_file = st.file_uploader(
            "Upload a document (.txt or .md)", type=("txt", "md")
        )

        # Ask the user for a question via `st.text_area`
        question = st.text_area(
            "Now ask a question about the document!",
            placeholder="Can you give me a short summary?",
            disabled=not uploaded_file,
        )

        if uploaded_file and question:

            # Process the uploaded file and question
            document = uploaded_file.read().decode()
            messages = [
                {
                    "role": "user",
                    "content": f"Here's a document: {document} \n\n---\n\n {question}",
                }
            ]

            # Generate an answer using the OpenAI API
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=True,
            )

            # Stream the response to the app using `st.write_stream`
            st.write_stream(stream)
    else:
        st.stop()  # Stop the app if the key is invalid
else:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")