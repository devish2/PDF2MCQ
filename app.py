import streamlit as st
import pypdf
import io

def main():
    # Set the page title and favicon
    st.set_page_config(
        page_title="PDF File Uploader",
        page_icon=":page_facing_up:",
        layout="centered"
    )

    # Page Title
    st.title("📄 PDF File Uploader")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a PDF file", 
        type=['pdf'], 
        help="Upload a PDF file to get started"
    )
    
    # Display file details and basic information when a file is uploaded
    if uploaded_file is not None:
        # Read the uploaded PDF
        try:
            # Create a PDF reader object
            pdf_reader = pypdf.PdfReader(io.BytesIO(uploaded_file.getvalue()))
            
            # Display basic PDF information
            st.subheader("PDF File Details")
            
            # Number of pages
            num_pages = len(pdf_reader.pages)
            st.write(f"**Number of Pages:** {num_pages}")
            
            # Try to get metadata
            try:
                metadata = pdf_reader.metadata
                if metadata:
                    st.subheader("Metadata")
                    for key, value in metadata.items():
                        st.write(f"**{key.replace('/', '')}:** {value}")
            except Exception as e:
                st.write("No additional metadata available.")
            
            # Preview first page text (if text is extractable)
            try:
                first_page = pdf_reader.pages[0]
                first_page_text = first_page.extract_text()
                
                st.subheader("First Page Preview")
                st.text_area(
                    "First Page Text (first 500 characters)", 
                    value=first_page_text[:500], 
                    height=200,
                    disabled=True
                )
            except Exception as e:
                st.warning("Could not extract text from the first page.")
            
            # File size and type confirmation
            st.write(f"**File Size:** {uploaded_file.size} bytes")
            st.write(f"**File Type:** {uploaded_file.type}")
            
        except Exception as e:
            st.error(f"Error processing PDF: {e}")
    else:
        # Guidance when no file is uploaded
        st.info("""
        ### How to Use
        1. Click on the "Browse files" button
        2. Select a PDF file from your computer
        3. View file details and preview
        
        **Supported File Type:** PDF
        """)

    # Footer
    st.markdown("---")
    st.markdown("*Simple PDF Uploader powered by Streamlit*")

if __name__ == "__main__":
    main()

