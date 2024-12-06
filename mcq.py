import streamlit as st # type: ignore
import PyPDF2  # type: ignore
import google.generativeai as genai # type: ignore
import os

def configure_gemini_api():
    """
    Configure the Gemini API with the API key from environment variable or Streamlit secrets.
    
    Returns:
        bool: True if API is successfully configured, False otherwise
    """
    try:

        
        # Try to get API key from environment variable
        api_key = os.getenv('AIzaSyDckDBylE6eYBEjaKpsqA_KWF5BgcXvUV8')
        
        # If not in environment, try Streamlit secrets
        if not api_key:
            api_key = ('AIzaSyDckDBylE6eYBEjaKpsqA_KWF5BgcXvUV8')
        
        if not api_key:
            st.error("Google API Key not found. Please set GOOGLE_API_KEY environment variable or in Streamlit secrets.")
            return False
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Error configuring Gemini API: {e}")
        return False

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

def main():
    """
    Main Streamlit application
    """
    # Set page configuration
    st.set_page_config(
        page_title="PDF Query Assistant with Gemini",
        page_icon="📄",
        layout="centered"
    )
    
    # Title and description
    st.title("📄 Covert your PDF into a Question Paper.")
    st.markdown("""
    Upload a PDF file and ask questions about its contents using Google's Gemini AI.
    
    ### How to use:
    1. Upload a PDF file
    2. Enter your query in the text box
    3. Click "Generate" to get an AI-powered answer
    """)
    
    # Configure Gemini API
    if not configure_gemini_api():
        st.stop()
    
    # PDF Upload Section
    uploaded_file = st.file_uploader(
        "Choose a PDF file", 
        type=['pdf'], 
        help="Upload a PDF file you want to query"
    )
    
    # Initialize session state variables
    if 'pdf_text' not in st.session_state:
        st.session_state.pdf_text = ""
    
    # Process PDF if uploaded
    if uploaded_file is not None:
        # Extract text from PDF
        st.session_state.pdf_text = extract_text_from_pdf(uploaded_file)
        
        if st.session_state.pdf_text:
            st.success("PDF successfully processed!")
            
            # Optional: Show a preview of extracted text
            with st.expander("Show Extracted Text Preview"):
                st.text(st.session_state.pdf_text[:1000] + "...")
    
    # Query Input Section
    query_prompt = st.text_input(
        "Enter your query", 
        placeholder="Write your prompt to generate a question paper!",
        disabled=not st.session_state.pdf_text
    )
    
    # Generate Button
    generate_button = st.button(
        "Generate with Gemini", 
        disabled=(not st.session_state.pdf_text or not query_prompt)
    )
    
    # Response Generation
    if generate_button and st.session_state.pdf_text and query_prompt:
        with st.spinner("Gemini is generating a response..."):
            response = generate_response_with_gemini(st.session_state.pdf_text, query_prompt)
        
        # Display Response
        st.subheader("Gemini's Response:")
        st.write(response)

# Run the Streamlit app
if __name__ == "__main__":
    main()

