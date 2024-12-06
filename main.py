import os
import time
import logging
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GeminiFileUploader:
    def __init__(self, api_key=None):
        """
        Initialize Gemini API client with optional API key.
        
        :param api_key: Google Gemini API key (optional, will use env variable if not provided)
        """
        # Securely retrieve API key
        if not api_key:
            api_key = ('AIzaSyDckDBylE6eYBEjaKpsqA_KWF5BgcXvUV8')
        
        if not api_key:
            raise ValueError("No API key provided. Set GOOGLE_GEMINI_API_KEY in environment variables.")
        
        # Configure API with secure key handling
        genai.configure(api_key=api_key)
        
        # Default generation configuration
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        
        # Initialize model
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=self.generation_config,
        )

    def upload_file(self, file_path, mime_type=None):
        """
        Upload a file to Gemini API with error handling.
        
        :param file_path: Path to the file to upload
        :param mime_type: MIME type of the file (optional)
        :return: Uploaded file object
        """
        try:
            # Validate file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Detect MIME type if not provided
            if not mime_type:
                mime_type = self._detect_mime_type(file_path)
            
            # Upload file
            uploaded_file = genai.upload_file(file_path, mime_type=mime_type)
            logger.info(f"Uploaded file '{uploaded_file.display_name}' as: {uploaded_file.uri}")
            
            return uploaded_file
        
        except Exception as e:
            logger.error(f"File upload error: {e}")
            raise

    def wait_for_files_active(self, files, timeout=300):
        """
        Wait for uploaded files to be processed, with timeout.
        
        :param files: List of file objects to check
        :param timeout: Maximum wait time in seconds
        :return: List of processed files
        """
        logger.info("Waiting for file processing...")
        
        start_time = time.time()
        processed_files = []
        
        for file in files:
            try:
                while True:
                    # Check file status
                    current_file = genai.get_file(file.name)
                    
                    # Check processing state
                    if current_file.state.name == "ACTIVE":
                        processed_files.append(current_file)
                        logger.info(f"File {file.name} is ready.")
                        break
                    
                    if current_file.state.name == "FAILED":
                        raise Exception(f"File {file.name} processing failed")
                    
                    # Check timeout
                    if time.time() - start_time > timeout:
                        raise TimeoutError(f"File {file.name} processing timed out")
                    
                    # Wait before next check
                    time.sleep(10)
                    logger.debug(".", end="", flush=True)
            
            except Exception as e:
                logger.error(f"Error processing file {file.name}: {e}")
                raise
        
        logger.info("All files processed successfully.")
        return processed_files

    def _detect_mime_type(self, file_path):
        """
        Detect MIME type based on file extension.
        
        :param file_path: Path to the file
        :return: Detected MIME type
        """
        ext = os.path.splitext(file_path)[1].lower()
        mime_types = {
            '.pdf': 'application/pdf',
            '.txt': 'text/plain',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.jpg': 'image/jpeg',
            '.png': 'image/png',
        }
        return mime_types.get(ext, 'application/octet-stream')

    def create_chat_session(self, files, prompt):
        """
        Create a chat session with uploaded files and a prompt.
        
        :param files: List of processed files
        :param prompt: Prompt to send with the files
        :return: Chat session response
        """
        try:
            # Ensure files are processed
            processed_files = self.wait_for_files_active(files)
            
            # Start chat session
            chat_session = self.model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": processed_files + [prompt],
                    }
                ]
            )
            
            # Send message and get response
            response = chat_session.send_message(prompt)
            return response.text
        
        except Exception as e:
            logger.error(f"Chat session error: {e}")
            raise

def main():
    """
    Example usage of the Gemini File Uploader
    """
    try:
        # Initialize uploader
        uploader = GeminiFileUploader()
        
        # Upload files
        files = [
            uploader.upload_file("", mime_type="application/pdf")
        ]
        
        # Create chat session and send prompt
        prompt = "Read this chapter thoroughly and create 20 MCQs for this chapter. Each question should have 4 options and 1 option should be correct."
        response = uploader.create_chat_session(files, prompt)
        
        # Print or process response
        print(response)
    
    except Exception as e:
        logger.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
