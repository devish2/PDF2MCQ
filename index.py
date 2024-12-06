import streamlit as st
import PyPDF2
from transformers import pipeline

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

def generate_response(text, prompt):
    """
    Generate a response based on the PDF text and user prompt.
    
    Args:
        text (str): Text extracted from the PDF
        prompt (str): User's query prompt
    
    Returns:
        str: Generated response
    """
    try:
        # Use a question-answering pipeline
        qa_pipeline = pipeline("question-answering")
        
        # Generate response
        result = qa_pipeline(question=prompt, context=text)
        
        return result['answer']
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "Could not generate a response. Please try again."

def main():
    """
    Main Streamlit application
    """
    # Set page configuration
    st.set_page_config(
        page_title="PDF Query Assistant",
        page_icon="📄",
        layout="centered"
    )
    
    # Title and description
    st.title("📄 PDF Query Assistant")
    st.markdown("""
    Upload a PDF file and ask questions about its contents.
    
    ### How to use:
    1. Upload a PDF file
    2. Enter your query in the text box
    3. Click "Generate" to get an answer
    """)
    
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
            with st.expander("Show Extracted Text"):
                st.text(st.session_state.pdf_text[:1000] + "...")
    
    # Query Input Section
    query_prompt = st.text_input(
        "Enter your query", 
        placeholder="What information are you looking for in this PDF?",
        disabled=not st.session_state.pdf_text
    )
    
    # Generate Button
    generate_button = st.button(
        "Generate", 
        disabled=(not st.session_state.pdf_text or not query_prompt)
    )
    
    # Response Generation
    if generate_button and st.session_state.pdf_text and query_prompt:
        with st.spinner("Generating response..."):
            response = generate_response(st.session_state.pdf_text, query_prompt)
        
        # Display Response
        st.subheader("Response:")
        st.write(response)

# Run the Streamlit app
if __name__ == "__main__":
    main()

# Requirements for setup:
# pip install streamlit PyPDF2 transformers torch