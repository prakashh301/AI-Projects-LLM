import streamlit as st
import pandas as pd
import PyPDF2
import docx
from groq import Groq

# Groq API Key
API_KEY = "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"  # Replace with your actual API key

# Function to analyze text using Groq AI
def analyze_text_with_groq(text, prompt):
    client = Groq(api_key=API_KEY)
    
    try:
        completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.6,
            top_p=0.95,
            stream=False,
            stop=None,
        )

        # Extract response content correctly
        response_content = completion.choices[0].message.content if completion.choices else "No response generated."

        return response_content

    except Exception as e:
        return f"Error: {str(e)}"

# Function to extract text from different file types
def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "txt":
        return uploaded_file.read().decode("utf-8")

    elif file_type == "pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        return text

    elif file_type == "docx":
        doc = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    elif file_type == "csv":
        df = pd.read_csv(uploaded_file)
        return df.to_string(index=False)  # Convert DataFrame to string

    else:
        return "Unsupported file format."

def main():
    st.title("Multi-File Analysis with Groq AI")
    
    # Prompt message for users
    st.markdown(
        "**📢 Note:** You are interacting with AI assistance from **Prakash, Aawesh, and Nilesh** – we are friends here to help! 😊"
    )

    # Allow multiple file types
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx", "csv"])
    prompt = st.text_input("Enter your prompt for the AI (e.g., Extract key insights)")

    if uploaded_file is not None and prompt:
        file_text = extract_text_from_file(uploaded_file)
        st.text_area("Extracted File Content", file_text, height=200)

        if st.button("Analyze Text"):
            analysis_result = analyze_text_with_groq(file_text, prompt)
            st.subheader("AI Output:")
            st.text_area("Analysis Result", analysis_result, height=300)

if __name__ == "__main__":
    main()
