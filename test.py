import streamlit as st
from groq import Groq

def analyze_text_with_groq(text, prompt):
    api_key = "oats&biscuits"  # Replace with your actual API key
    
    client = Groq(api_key=api_key)
    
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

        # Extracting response content correctly
        response_content = completion.choices[0].message.content if completion.choices else "No response generated."

        return response_content

    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("Text File Analysis with Groq AI")

    uploaded_file = st.file_uploader("Choose a text file", type=["txt"])
    prompt = st.text_input("Enter your prompt for the AI (e.g., Extract names)")

    if uploaded_file is not None and prompt:
        string_data = uploaded_file.read().decode("utf-8")
        st.text_area("File Content", string_data, height=200)

        if st.button("Analyze Text"):
            analysis_result = analyze_text_with_groq(string_data, prompt)
            st.subheader("AI Output:")
            st.text_area("Analysis Result", analysis_result, height=300)  # Display in text area

if __name__ == "__main__":
    main()
