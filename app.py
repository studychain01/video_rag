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

    def chat_with_video(self, video_file, prompt):
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

# ===========================
#   Session State Initialization
# ===========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "video_file" not in st.session_state:
    st.session_state.video_file = None

if "video_processor" not in st.session_state:
    st.session_state.video_processor = None

if "video_name" not in st.session_state:
    st.session_state.video_name = None 

# ===========================
#   Sidebar Configuration
# ===========================
with st.sidebar:
    st.header(" API Configuration")

    default_api_key = os.getenv("GEMINI_API_KEY")

    api_key = st.text_input("GEMINI API Key", value=default_api_key, type="password", help="Get your API key from https://aistudio.google.com/app/apikey")

    if api_key:
        if st.session_state.video_processor is None: 
            st.session_state.video_processor = VideoProcessor(api_key)
        
    st.markdown("---")
    
    st.header("Upload Video")

    uploaded_file = st.file_uploader(
        "Choose a video file", 
        type=['mp4', 'avi', 'mov', 'mkv', 'webm'],
        help="Supported formats: MP4, AVI, MOV, MKV, WEBM"
    )

    if uploaded_file is not None:
        if not is_video_file(uploaded_file):
            st.error("Please upload a valid video file.")
        else:
            file_size = get_file_size_mb(uploaded_file)
            st.info(f"File size: {file_size:.2f} MB")

            if file_size > 100:
                st.warning("Large files may take longer to process or may fail. Consider compressing your video.")

            #Process video if not already processed 
            if (st.session_state.video_file is None or 
                st.session_state.video_name != uploaded_file.name):
                
                if st.session_state.video_processor is None:
                    st.error("Please enter your Gemini API key:")
                else:
                    with st.spinner("Uploading and processing video..."):
                        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_file_path = tmp_file.name

                        try:
                            video_file = st.session_state.video_processor.upload_video(
                                tmp_file_path,
                                uploaded_file.name
                            )

                            if video_file:
                                processed_file = st.session_state.video_processor.wait_for_file_processing(video_file)

                                if processed_file:
                                    st.session_state.video_file = processed_file
                                    st.session_state.video_name = uploaded_file.name
                                    st.success("Video processed successfully!")

                                    st.session_state.messages = []
                        
                        finally:
                            try:
                                os.unlink(tmp_file_path)

                            except:
                                pass

        if st.session_state.video_file:
            display_video(uploaded_file.getvalue(), uploaded_file.name)
        
    st.markdown("---")

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
    with col2:
        if st.button("Reset All"):
            reset_chat()
            st.rerun()
        

# ===========================
#   Main Chat Interface
# =========================== 
st.title("Video RAG with Gemini")
st.markdown("Upload a video and chat with it using Google's Gemini AI!")

# Check if ready to chat
if not api_key:
    st.info("Please enter your Gemini API key in the sidebar to get started.")
elif st.session_state.video_file is None:
    st.info("Please upload a video file in the sidebar to start chatting")
else:
    st.success(f"Ready to chat about: **{st.session_state.video_name}**")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
 
    if len(st.session_state.messages) == 0:
        st.markdown("### Try these example questions:")
        example_prompts = [
            "What is happening in this video?",
            "Summarize the main events",
            "Describe the people and objects you see",
            "What is the setting or environment?",
            "What actions are taking place?"
        ]

        cols = st.columns(2)
        for i, example in enumerate(example_prompts):
            with cols[i % 2]:
                if st.button(f" {example}", key=f"example_{i}"):

                    st.session_state.messages.append({"role": "user", "content": example})
                    st.rerun()

    # Chat Input 

    if prompt := st.chat_input("Ask a question about your video..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            with st.spinner("Analyzing video and generating response..."):
                response = st.session_state.video_processor.chat_with_video(
                    st.session_state.video_file, 
                    prompt
                )
            
            if response:
                full_response = ""
                for chunk in response.split():
                    full_response += chunk + " "
                    message_placeholder.markdown(full_response + " ")
                    time.sleep(0.05)

                message_placeholder.markdown(response)

                st.session_state.messages.append({"role": "assistant", "content": response})

            else:
                st.error("Failed to generate response. Please try again.")

# ===========================
#   Footer
# ===========================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Built with ❤️ using Gemini API and Streamlit | 
    <a href='https://ai.google.dev/gemini-api/docs/video-understanding' target='_blank'>Learn more about Gemini Video API</a></p>
</div>
""", unsafe_allow_html=True)



        








    
