import openai
from io import BytesIO
from PyPDF2 import PdfReader
import streamlit as st
import pandas as pd

# OpenAI API key setup
openai.api_key = 'your_openai_api_key_here'

# Streamlit app setup
st.title("Board Deck Analyzer")
st.write("Upload a board deck to analyze key information and compare performance.")

# File upload
uploaded_file = st.file_uploader("Upload a PDF file of the board deck", type=["pdf"])

def extract_text_from_pdf(file):
    """Extracts text from a PDF file."""
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"
    return text

def analyze_text_with_openai(text):
    """Analyzes text using OpenAI API to extract key information."""
    prompt = f"Analyze the following board deck and extract the key insights, metrics, and business highlights:\n{text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1500
    )
    return response.choices[0].text.strip()

def generate_comparison_table(company_data):
    """Generates a comparison table of company performance vs. similar companies."""
    # Example data: Replace with actual data source or API
    comparison_data = {
        "Metric": ["Revenue", "Growth Rate", "Profit Margin", "Customer Retention"],
        "Uploaded Company": company_data,
        "Similar Company A": [5000000, "20%", "15%", "85%"],
        "Similar Company B": [4500000, "18%", "12%", "80%"],
        "Similar Company C": [5200000, "22%", "18%", "87%"],
    }
    return pd.DataFrame(comparison_data)

if uploaded_file is not None:
    # Extract text from uploaded PDF
    text = extract_text_from_pdf(uploaded_file)
    st.write("Board Deck Text Extracted")
    
    # Analyze text using OpenAI API
    with st.spinner("Analyzing the board deck..."):
        analysis = analyze_text_with_openai(text)
        st.write("Key Information Extracted:")
        st.text(analysis)

    # Mock data for uploaded company for comparison
    # Replace with actual extracted data when integrating with a more advanced parser
    uploaded_company_data = [4800000, "19%", "14%", "83%"]

    # Generate comparison table
    comparison_table = generate_comparison_table(uploaded_company_data)
    st.write("Performance Comparison:")
    st.dataframe(comparison_table)
