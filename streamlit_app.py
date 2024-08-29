import streamlit as st
from openai import OpenAI
from openai.types.error import APIError

# Show title and description.
st.title("📄 Document question answering agent")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Function to validate OpenAI API key
def validate_api_key(api_key):
    if not api_key:
        return False
    try:
        client = OpenAI(api_key=api_key)
        # Attempt a simple API call to check if the key is valid
        client.models.list()
        return True
    except APIError:
        return False

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password", key="api_key")

# Validate the API key immediately after input
if openai_api_key:
    if validate_api_key(openai_api_key):
        st.success("Valid API key. You can now use the app.")
        # Create an OpenAI client
        client = OpenAI(api_key=openai_api_key)
    else:
        st.error("Invalid API key. Please check and try again.")
        st.stop()  # Stop execution if the key is invalid
elif openai_api_key == "":
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    st.stop()  # Stop execution if no key is provided

# The rest of your code remains the same
uploaded_file = st.file_uploader(
    "Upload a document (.txt or .md)", type=("txt", "md")
)

question = st.text_area(
    "Now ask a question about the document!",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question:
    document = uploaded_file.read().decode()
    messages = [
        {
            "role": "user",
            "content": f"Here's a document: {document} \n\n---\n\n {question}",
        }
    ]

    stream = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=messages,
        stream=True,
    )

    st.write_stream(stream)