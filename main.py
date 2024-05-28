import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read the account ID and API token from environment variables
ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

# Function to interact with Cloudflare's AI
def run(model, input):
    response = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{model}",
        headers={"Authorization": f"Bearer {API_TOKEN}"},
        json=input
    )
    return response.json()

# Function to handle code conversion
def convert_code(prompt):
    input_payload = {
        "messages": [
            {"role": "system", "content": "You are a friendly assistant"},
            {"role": "user", "content": prompt}
        ]
    }
    # Replace '@cf/meta/llama-2-7b-chat-int8' with the appropriate model for code conversion
    output = run('@cf/meta/llama-2-7b-chat-int8', input_payload)
    return output.get("result")

# Streamlit app
st.set_page_config(page_title="Code Converter Web App")
st.title("Code Converter Web App")
st.write("Convert code from one programming language to another using Cloudflare AI.")

source_code = st.text_area("Enter the source code here:", placeholder="Enter your code here...", height=200)
source_language = st.selectbox("Source Language", ["Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Go", "PHP", "Swift", "TypeScript", "Kotlin", "Rust", "Scala", "Perl", "Haskell"])
target_language = st.selectbox("Target Language", ["Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Go", "PHP", "Swift", "TypeScript", "Kotlin", "Rust", "Scala", "Perl", "Haskell"])

if st.button("Convert"):
    if source_code:
        with st.spinner("Converting..."):
            prompt = f"Convert the following {source_language} code to {target_language}:\n\n{source_code}"
            converted_code = convert_code(prompt)
            st.code(converted_code.get("response"), target_language, line_numbers=True)
    else:
        st.error("Please enter the source code to convert.")
