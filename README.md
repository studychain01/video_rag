# Video RAG Conversations

A Streamlit application that allows you to chat with videos using Google's Gemini AI. Upload a video file and ask questions about its content - the AI will analyze the video and provide intelligent responses.

## Features

- 🎬 **Video Upload**: Support for MP4, AVI, MOV, MKV, and WEBM formats
- 🤖 **AI-Powered Analysis**: Uses Google's Gemini 1.5 Pro model for video understanding
- 💬 **Interactive Chat**: Ask questions about video content and get detailed responses
- 📱 **User-Friendly Interface**: Clean Streamlit interface with sidebar controls
- 🔄 **Session Management**: Clear chat history and reset functionality

## Prerequisites

- Python 3.7 or higher
- Google Gemini API key (get it from [Google AI Studio](https://aistudio.google.com/app/apikey))

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Video-RAG-Conversations
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your API key**:
   Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to get your Gemini API key

## Getting Video Content

### Option 1: Download YouTube Videos/Shorts

To analyze YouTube content, you'll need to download videos first:

1. **Install yt-dlp** (if not already installed):
   ```bash
   pip install yt-dlp
   ```

2. **Download a YouTube video/short**:
   ```bash
   yt-dlp -f mp4 "https://www.youtube.com/shorts/GPK6-gkJIqc"
   ```

3. **Download with specific quality** (optional):
   ```bash
   # Download best quality
   yt-dlp -f "best[ext=mp4]" "YOUR_VIDEO_URL"
   
   # Download specific resolution
   yt-dlp -f "best[height<=720][ext=mp4]" "YOUR_VIDEO_URL"
   ```

### Option 2: Use Your Own Videos

You can also use any video file you have locally in the supported formats:
- MP4
- AVI
- MOV
- MKV
- WEBM

## Usage

1. **Run the application**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and navigate to `http://localhost:8501`

3. **Enter your API key** in the sidebar

4. **Upload a video file** using the file uploader in the sidebar

5. **Start chatting**! Ask questions like:
   - "What is happening in this video?"
   - "Summarize the main events"
   - "Describe the people and objects you see"
   - "What is the setting or environment?"
   - "What actions are taking place?"

## Example Workflow

1. **Download a YouTube short**:
   ```bash
   yt-dlp -f mp4 "https://www.youtube.com/shorts/k_ZfKQH6Fmw"
   ```

2. **Start the app**:
   ```bash
   streamlit run app.py
   ```

3. **Upload the downloaded video** and start asking questions!

## File Size Limits

- **Recommended**: Keep videos under 100MB for optimal performance
- **Maximum**: The app will warn you for files over 100MB
- **Processing time**: Larger files may take longer to process

## Troubleshooting

### Common Issues

1. **"API key not found"**: Make sure you've entered your API key correctly in the sidebar
2. **"Video processing failed"**: Try with a smaller video file or different format
3. **"Upload failed"**: Check your internet connection and API key validity

### Performance Tips

- Use MP4 format for best compatibility
- Compress large videos before uploading
- Ensure stable internet connection for video processing

## Dependencies

- `streamlit>=1.28.0` - Web application framework
- `google-generativeai>=0.8.0` - Google Gemini AI API
- `python-dotenv>=1.0.0` - Environment variable management
- `pillow>=10.0.0` - Image processing (for video thumbnails)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the [MIT License](LICENSE).

---

**Built with ❤️ using Gemini API and Streamlit**

For more information about Gemini Video API, visit: [Gemini Video Understanding Documentation](https://ai.google.dev/gemini-api/docs/video-understanding) 