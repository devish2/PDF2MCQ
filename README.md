Generating PDFs for Question Papers and MCQs
Introduction
For teachers, educational hubs, and exam preparation platforms, creating high-quality question papers and Multiple-Choice Question (MCQ) assessments is crucial yet time-consuming. Fortunately, several tools and techniques can streamline this process, allowing educators to focus on content creation rather than tedious formatting. This article explores how to effectively generate PDFs for question papers and MCQs, catering to various needs, from classroom tests to large-scale mock exams like the JEE.
Overview
This Streamlit application allows users to upload a PDF file and ask questions about its contents using Google's Gemini AI.
Why Digital Question Paper Generation Matters
Benefits of Digital Question Paper Creation
Consistency: Ensure uniform formatting and quality
Randomization: Create multiple unique test versions
Efficiency: Save time in exam preparation
Accessibility: Easy to distribute and store digitally
Customization: Quickly customize your question paper as per your format.

Features
PDF file upload
Text extraction from PDF
AI-powered question answering with Gemini
User-friendly interface

Prerequisites
Python 3.8+
pip (Python package manager)
Google Cloud Account and Credits
Google Gemini API Key
Google AI Studio
Streamlit

High-Level architecture:
Step-by-step Instructions
Create a Google Cloud account and activate your credits.

Install Python and ensure it's added to your PATH.
Install Streamlit for the front end.

Install all pip (required package)
Integrate Gemini

Tune prompt with Google AI Studio

Installation and Running
To set up and run the application:
Install dependencies: 
 pip install -r requirements.txt 
 pip install pyPDF2 
 pip install streamlit pdfplumber google-generativeai
Run the app: 
streamlit run mcq.py

Setting Up Gemini
Access the Gemini Platform: Log in to your Google Cloud Console and enable Gemini APIs in your project.
Install Required SDKs: Install the necessary Google Cloud libraries using pip install google-cloud. These libraries allow seamless interaction with Gemini APIs.
Authenticate: Download your Google Cloud credentials and authenticate your project using

Tune Model for Prompts:
To fine-tune the model, I utilized Google AI Studio to extract question papers from PDF documents. Subsequently, I employed Gen AI Prompts to further refine the model's capabilities.
Navigating Dashboard to New Tuned Model
Following the selection of the tune model, a structured prompt was crafted to facilitate user-like queries during the fine-tuning process.
Leveraging provided input prompts, the model was fine-tuned and trained to generate the desired output.
Some samples of tune input.
Code Sample:
Import all dependencies

import streamlit as st 
import PyPDF2  
import google.generativeai as genai
import os
2. Configure the Gemini API with the API key from the environment variable.
def configure_gemini_api():
    """
    Configure the Gemini API with the API key from environment variable or Streamlit secrets.
    
    Returns:
        bool: True if API is successfully configured, False otherwise
    """
    try:

        
        # Try to get API key from environment variable
        api_key = os.getenv('GOOGLE_API_KEY')
        
        # If not in environment, try Streamlit secrets
        if not api_key:
            api_key = ('GOOGLE_API_KEY')
        
        if not api_key:
            st.error("Google API Key not found. Please set GOOGLE_API_KEY environment variable or in Streamlit secrets.")
            return False
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Error configuring Gemini API: {e}")
        return False
Extract text from the uploaded PDF file.
def extract_text_from_pdf(uploaded_file):
    """
    Extract text from an uploaded PDF file.
    
    Args:
        uploaded_file (UploadedFile): The uploaded PDF file
    
    Returns:
        str: Extracted text from the PDF
    """
    try:
        # Read the PDF file
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""
Generate a response with the help of Google Gemini AI
def generate_response_with_gemini(text, prompt):
    """
    Generate a response using Google's Gemini model.
    
    Args:
        text (str): Text extracted from the PDF
        prompt (str): User's query prompt
    
    Returns:
        str: Generated response from Gemini
    """
    try:
        # Choose a Gemini model
        model = genai.GenerativeModel('gemini-pro')
        
        # Construct the full prompt with context
        full_prompt = f"""
        Context from PDF:
        {text[:10000]}  # Limit context to first 10000 characters to avoid token limits

        User Query: {prompt}

        Please provide a detailed and accurate response based on the context and query.
        """
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        return response.text
    except Exception as e:
        st.error(f"Error generating response with Gemini: {e}")
        return "Could not generate a response. Please try again."
Output / Demo:
PDF2MCQ.mov
Edit descriptiondrive.google.com
At the end of this project, the user can
The user can upload a pdf and extract text from a pdf.
Can generate a subjective question paper and MCQ for assessments.
Question Paper patterns can be like JEE exams and Mock Tests.

What's next?
The app can be expanded to include:
Generate a new question paper based on the previous year's exam.
Can generate exam papers according to specific patterns.
Generate an answer key according to the paper.

Resources:
Streamlit documentation
GitHub Repository

Call to action
To learn more about Google Cloud services and to create an impact for the work you do, get around to these steps right away:
Register for Code Vipassana sessions
Join the meetup group Datapreneur Social
Sign up to become a Google Cloud Innovator
