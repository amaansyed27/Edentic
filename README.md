# 🎬 Edentic - Revolutionary AI Multimedia Creator

**"The story is yours. The edit is ours."**

Edentic is a cutting-edge AI-powered multimedia content creation platform that transforms any combination of media assets into professional videos. Upload videos, images, and audio files, describe your vision, and let our AI create, edit, and produce broadcast-quality content automatically.

## 🆕 Latest Updates

### ✅ **Smart Duration Management** 
- **Automatic Length Adjustment**: Optimizes video duration based on available content
- **Small File Support**: Works perfectly with short clips and images  
- **Duration Validation**: Prevents timeline errors with intelligent content analysis
- **User Feedback**: Provides insights about your content before processing

## 🚀 Revolutionary Features

### 🎨 **Complete Multimedia Support**
- **Videos**: Screen recordings, demos, tutorials, clips *(any length)*
- **Images**: Photos, screenshots, graphics, artwork  
- **Audio**: Voiceovers, music tracks, sound effects
- **AI Generation**: Creates missing content automatically

### 🧠 **Advanced AI Capabilities**
- **Content Analysis**: Understands your media and vision
- **Smart Generation**: Creates title cards, background music, voiceovers
- **Professional Editing**: Assembles content with perfect timing
- **Style Adaptation**: Matches your desired tone and audience
- **Duration Intelligence**: Automatically adjusts to optimize your content

### 🎬 **Professional Results**
- **Broadcast Quality**: Professional video production standards
- **Perfect Timing**: AI-optimized pacing and transitions
- **Audio Mixing**: Professional sound design and levels
- **Visual Effects**: Seamless transitions and styling

## 💡 Perfect For

- 🎓 **Educational Content**: Tutorials, courses, explanations
- 📱 **Product Demos**: App showcases, feature walkthroughs
- 🎨 **Creative Projects**: Social media content, artistic videos
- 🏢 **Business Content**: Presentations, marketing videos
- 🎉 **Personal Projects**: Wedding slideshows, family videos

## � Technology Stack

- **Frontend**: Streamlit (Interactive Web Interface)
- **Video Processing**: VideoDB SDK (Professional video editing)
- **AI Analysis**: Google GenAI Gemini 2.5 Flash (Content understanding)
- **Image Generation**: Google GenAI Gemini 2.0 Flash Preview (Visual content)
- **Audio Processing**: VideoDB Audio Generation (Voiceovers & music)

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
git clone <repository-url>
cd Edentic

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup API Keys
```bash
# Set your API keys as environment variables
export VIDEODB_API_KEY="your_videodb_api_key"
export GOOGLE_API_KEY="your_google_genai_api_key"
```

### 3. Run the Application
```bash
streamlit run app.py
```

### 4. Create Your First Video
1. **Describe Your Project**: Tell the AI what kind of video you want
2. **Upload Media Files**: Add any combination of videos, images, audio
3. **Describe Each Asset**: Help the AI understand how to use each file
4. **Generate**: Let the AI create your professional video!
## 🎯 Example Projects

### 📚 Tutorial Video
**Input**: 
- Screen recording clips of software demo
- Product logo image
- Audio narration (optional)

**AI Generates**:
- Professional title card with logo
- Background music track
- Enhanced voiceover (if needed)
- Perfect transitions and timing

**Output**: Complete tutorial video ready for YouTube/training

### 📱 Product Demo
**Input**:
- App screenshots
- Short demo video clips
- Company branding assets

**AI Generates**:
- Marketing copy and titles
- Professional voiceover
- Upbeat background music
- Call-to-action screens

**Output**: Professional product demo for marketing

### 🎨 Creative Slideshow
**Input**:
- Collection of photos
- Audio clips or music preferences
- Style description

**AI Generates**:
- Title and end cards
- Background music
- Smooth transitions
- Text overlays and effects

**Output**: Cinematic slideshow video

2. **Optional: Specify Content Type** 🎯 
   - Help AI understand better (Software Demo, Hackathon Project, etc.)
   - Or let AI auto-detect - it's very smart!

3. **Click "Create My Video with AI"** 🤖
   - Sit back and relax - AI does everything automatically!

4. **Watch the AI Magic** ✨
   - **Analyzes** your content (transcription + visual analysis)
   - **Understands** what you're demonstrating 
   - **Creates** a professional story structure
   - **Generates** compelling voiceover narration
   - **Assembles** final video with perfect timing

5. **Get Your Professional Video** 🎬
   - Ready to share, submit, or present
   - Professional quality with zero effort from you!

## 🎯 Perfect For

- **🏆 Hackathon Demos**: Upload screen recordings → Get professional demo video
- **📚 Tutorials**: AI creates perfect educational flow automatically
- **💼 Product Demos**: Professional presentations without editing skills
- **🎓 Educational Content**: AI understands and explains your material
- **📱 Social Media**: Quick professional content creation

## 🔧 How The AI Works

### Fully Automated Process

1. **🧠 Content Analysis**
   - AI transcribes all spoken content
   - Computer vision analyzes visual elements
   - Understands software interfaces, user actions, key features

2. **📖 Story Understanding** 
   - AI determines what you're trying to demonstrate
   - Identifies target audience and key messages
   - Creates logical narrative flow

3. **🎤 Professional Narration**
   - Generates compelling voiceover script
   - Professional tone and pacing
   - Explains features clearly and engagingly

4. **🎬 Intelligent Editing**
   - Matches video clips to narrative moments
   - Optimal timing and transitions
   - Professional video assembly

5. **⚡ Instant Delivery**
   - Professional video ready in minutes
   - No editing skills required
   - Ready to share immediately

## 🎨 Example Use Cases

### Hackathon Demo
```
Input: 3 screen recordings of your app
Output: "Welcome to our innovative solution! First, let me show you 
        the intuitive login process..." [Professional demo video]
```

### Tutorial Creation  
```
Input: Raw screen recordings of software usage
Output: "In this tutorial, we'll explore the key features. Let's 
        start with the dashboard..." [Polished tutorial]
```

### Product Presentation
```
Input: Multiple clips showing different features  
Output: "Our product revolutionizes workflow with these capabilities..." 
        [Marketing-ready video]
```

## 🛡️ Error Handling

The application includes comprehensive error handling for:
- API key validation and initialization
- Video upload and processing failures  
- AI service timeouts and rate limits
- Content analysis edge cases
- Network connectivity issues
- Fallback options for all critical functions

## 📊 Performance & Limits

- **Processing Speed**: Typically 5-10 minutes for complete automation
- **Video Length**: Works best with clips under 10 minutes each
- **File Formats**: MP4, MOV, AVI, MKV, WMV supported
- **API Limits**: Free tiers available for both VideoDB and Google GenAI
- **Quality**: Professional broadcast-quality output

## 🔮 What Makes This Special

### Revolutionary Approach
- **First fully automated video editor** for screen recordings
- **No script required** - AI understands your intent
- **Professional results** without any editing knowledge
- **Perfect for non-editors** who need great videos

### AI-Powered Intelligence
- **Content comprehension** beyond simple transcription
- **Context awareness** of software demos and tutorials
- **Professional storytelling** automatically generated
- **Optimal pacing and flow** determined by AI

## 📁 Project Structure

```
Edentic/
├── app.py                 # Main Streamlit application (fully automated)
├── requirements.txt       # Python dependencies
├── setup.py              # Automated setup script
├── setup.bat             # Windows one-click setup
├── test_setup.py         # Installation verification
├── README.md             # This file
├── GETTING_STARTED.md    # Quick start guide  
├── PROJECT_OVERVIEW.md   # Technical details
└── .streamlit/
    ├── secrets_example.toml
    └── secrets.toml      # Your API keys (create this)
```

## 🤝 Contributing

We welcome contributions to make Edentic even more intelligent:
- Enhanced content analysis algorithms
- Additional video format support
- UI/UX improvements
- Performance optimizations
- Multi-language support

## 🙏 Acknowledgments

- **VideoDB**: Powerful video database and editing capabilities
- **Google GenAI**: Advanced AI for content understanding and analysis
- **Streamlit**: Beautiful and intuitive web app framework

## � Resources

- [VideoDB Documentation](https://docs.videodb.io/)
- [Google GenAI Documentation](https://ai.google.dev/gemini-api/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**� Edentic - Where AI meets creativity, and clips become stories!**

*The future of video editing is here - fully automated, completely intelligent.*

Made with ❤️ for creators who want professional results without the complexity.

## 🔧 How It Works

### The AI Director Process

1. **Script Analysis**: Gemini AI breaks down your script into distinct visual scenes
2. **Content Understanding**: VideoDB transcribes and indexes your video clips
3. **Semantic Matching**: AI matches each script scene to the most relevant video clip
4. **Timeline Assembly**: VideoDB's timeline editor combines clips in sequence
5. **Voiceover Integration**: Generated speech is overlaid on the final video

### Key Technologies

- **VideoDB Timeline Editing**: Advanced video compilation with VideoAsset and AudioAsset objects
- **Semantic Search**: Find the perfect clip for each script moment
- **Voice Generation**: Professional TTS with customizable voices
- **Real-time Processing**: Efficient video processing and streaming

## 📁 Project Structure

```
Edentic/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── secrets_template.toml  # API key configuration template
├── README.md             # This file
└── .streamlit/
    └── secrets.toml      # Your API keys (create this)
```

## 🔒 Environment Variables

The application uses Streamlit secrets for secure API key management:

- `VIDEODB_API_KEY`: Your VideoDB API key
- `GOOGLE_API_KEY`: Your Google GenAI API key

**⚠️ Never commit your actual API keys to version control!**

## 🛡️ Error Handling

The application includes comprehensive error handling for:
- API key validation
- File upload issues
- Video processing failures
- AI service timeouts
- Network connectivity problems

## 🎨 Customization Options

### Modify Voice Settings
```python
voiceover_audio = collection.generate_voice(
    text=script_text,
    voice_name='Default',  # Change voice type
    config={
        'stability': 0.5,      # Emotional variation
        'similarity_boost': 1.0, # Voice matching
        'style': 0.2          # Speaking style
    }
)
```

### Adjust Video Timeline
```python
video_asset = VideoAsset(
    asset_id=video.id,
    start=start_time,
    end=end_time
)
```

## 📊 Performance Tips

1. **Video Length**: Keep individual clips under 5 minutes for faster processing
2. **Script Quality**: Write clear, descriptive scripts for better matching
3. **File Formats**: Use MP4 for best compatibility
4. **Internet Connection**: Ensure stable connection for API calls

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**:
   - Check that secrets.toml exists in .streamlit/ folder
   - Verify API keys are correct and active

2. **Upload Failures**:
   - Check file formats are supported
   - Ensure files aren't corrupted
   - Try smaller file sizes

3. **Video Processing Timeouts**:
   - Wait for indexing to complete
   - Try shorter video clips
   - Check internet connection

4. **No Voice Generation**:
   - Application continues without voiceover
   - Check VideoDB API limits
   - Verify script text isn't empty

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check the license file for details.

## 🙏 Acknowledgments

- **VideoDB**: Powerful video database and editing capabilities
- **Google GenAI**: Advanced AI for script analysis
- **Streamlit**: Beautiful and simple web app framework

## 🔗 Resources

- [VideoDB Documentation](https://docs.videodb.io/)
- [Google GenAI Documentation](https://ai.google.dev/gemini-api/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**🎬 Edentic - Where your story meets AI editing magic!**

Made with ❤️ for creators, developers, and storytellers.
