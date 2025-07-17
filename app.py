import streamlit as st
import google.generativeai as genai
import os #Used to interact with the operating system.
import tempfile #Used to create temporary files and directories. Automatically cleans up after use.
import time #Provides functions to work with time
import base64 #For encoding and decoding data using Base64 encoding (commonly used for binary-to-text encoding).
from pathlib import Path #Provides an object-oriented way to work with filesystem paths. Safer and more readable than using os.path
import mimetypes #Used to guess the MIME type of a file based on its extension.
from dotenv import load_dotenv #loads environment variables from .env file and adds them to the os environment.

load_dotenv()

st.set_page_config(
    page_title="Video RAG with Gemini",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================
#   Video Processing Class
# ===========================
class VideoProcessor:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def upload_video(self, video_path, display_name=None):
        """Upload video to Gemini File API"""
        try: 
            video_file = genai.upload_file(
                path=video_path,
                display_name=display_name or "uploaded_video"
            )
            return video_file
        except Exception as e: 
            st.error(f"Error uploading video: {e}")
            return None
    
    def wait_for_file_processing(self, video_file):
        """Wait for video file to be processed by Gemini"""
        try:
            while video_file.state.name == "PROCESSING":
                time.sleep(2)
                video_file = genai.get_file(video_file.name)

            if video_file.state.name == "READY":
                raise ValueError("Video processing failed")
            
            return video_file 
        
        except Exception as e:
            st.error(f"Error processing video: {str(e)}")
            return None 

    def chat_with_video(self, video_file, query):
        """Generate response based on video content and user prompt"""
        try:
            response = self.model.generate_content([
                video_file, 
                prompt
            ])
            return response.text
        
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return None 

# ===========================
#   Helper Functions
# ===========================
def is_video_file(file):
    """Check if uploaded file is a video"""
    if file is None:
        return False
    # mimetypes.guess_type(file.name) tries to guess the MIME type based 
    # on the file name or extension (like .mp4, .png, etc).
    # The _ means you're ignoring the second value (encoding), because you don't need it.

    mime_type, _ = mimetypes.guess_type(file.name)
    return mime_type and mime_type.startswith('video/')

def get_file_size_mb(file):
    """Get file size in MB"""
    return len(file.getvalue()) / (1024 * 1024)

def reset_chat():
    """Reset chat history and video state"""
    st.session_state.messages = []
    if 'video_file' in st.session_state:
        try:
            genai.delete_file(st.session_state.video_file.name)
        except:
            pass
        del st.session_state.video_file 
    if 'video_processor' in st.session_state:
        del st.session_state.video_processor
    if 'video_name' in st.session_state:
        del st.session_state.video_name
    
def display_video(video_bytes, video_name):
    """Display uploaded video"""
    st.markdown(f"### 🎬 {video_name}")
    st.video(video_bytes)





    
