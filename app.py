import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI

# ✅ Initialize OpenRouter client securely
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]
)

# 📝 Function to summarize the resume
def summarize_resume(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            resume_text = ""
            for page in reader.pages:
                resume_text += page.extract_text()
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

    # Prompts for the model
    messages = [
        {"role": "system", "content": "You are an AI assistant that summarizes resumes. Give the summary in a paragraph and mention the suitable domain for the resume."},
        {"role": "user", "content": f"Summarize the following resume:\n\n{resume_text}"}
    ]

    # Call the OpenRouter API
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-maverick:free",
            messages=messages
        )
        summary = completion.choices[0].message.content
        return summary
    except Exception as e:
        st.error(f"Error during completion: {e}")
        return None

# 🖥️ Streamlit UI
st.title("📝 Resume Summarizer with OpenRouter")
uploaded_file = st.file_uploader("Upload a PDF Resume", type="pdf")

if uploaded_file is not None:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())
    summary = summarize_resume("temp_resume.pdf")
    if summary:
        st.subheader("📄 Summary:")
        st.write(summary)
