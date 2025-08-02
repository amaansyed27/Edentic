# 🎬 Edentic - Project Overview

## What is Edentic?

**Edentic** is an AI-powered video editing application that embodies the tagline **"The story is yours. The edit is ours."** It automatically creates professional videos from user-uploaded clips and scripts, perfect for hackathon demos, tutorials, and presentations.

## 🚀 Key Features

### AI Director Capabilities
- **Script Analysis**: Uses Google Gemini AI to break down scripts into visual scenes
- **Content Understanding**: VideoDB transcribes and indexes uploaded video clips
- **Smart Matching**: Semantic search finds the best clip for each script moment
- **Timeline Assembly**: Automatically stitches clips together in perfect sequence
- **Voice Generation**: Creates professional AI voiceover from the script

### User Experience
- **Drag & Drop Interface**: Simple Streamlit web app
- **Multi-format Support**: MP4, MOV, AVI, MKV, WMV
- **Real-time Progress**: Visual feedback during processing
- **Instant Preview**: Watch your generated video immediately

## 🔧 Technical Architecture

### Core Components

1. **Frontend**: Streamlit web application
2. **Video Processing**: VideoDB SDK for upload, transcription, search, and editing
3. **AI Analysis**: Google GenAI (Gemini 2.5 Flash) for script understanding
4. **Timeline Editing**: VideoDB's advanced video compilation features

### Data Flow

```
User Input (Clips + Script) 
    ↓
AI Script Analysis (Gemini)
    ↓
Video Upload & Transcription (VideoDB)
    ↓
Semantic Matching (VideoDB Search)
    ↓
Voice Generation (VideoDB TTS)
    ↓
Timeline Assembly (VideoDB)
    ↓
Final Video Output
```

## 📁 Project Structure

```
Edentic/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── setup.py              # Automated setup script
├── setup.bat             # Windows batch setup
├── test_setup.py         # Verify installation
├── demo.py               # Component testing script
├── README.md             # Comprehensive documentation
├── GETTING_STARTED.md    # Quick start guide
├── secrets_template.toml # API key template
└── .streamlit/
    ├── secrets_example.toml
    └── secrets.toml      # Your API keys (create this)
```

## 🎯 Target Use Cases

### Primary Users
- **Hackathon Participants**: Create professional demo videos quickly
- **Educators**: Turn screen recordings into polished tutorials
- **Developers**: Showcase products with automatic editing
- **Content Creators**: Rapid video production for social media

### Specific Scenarios
- Software demonstrations
- Tutorial video creation
- Product launch videos
- Educational content
- Marketing presentations
- Conference submissions

## 🛠️ Technology Stack

### APIs and Services
- **VideoDB**: Video database, transcription, search, editing, voice generation
- **Google GenAI**: Gemini 2.5 Flash for script analysis and scene understanding
- **Streamlit**: Web application framework and UI

### Python Libraries
- `streamlit`: Web app framework
- `videodb`: Video processing SDK
- `google-genai`: Google's AI client library
- Built-in: `json`, `os`, `tempfile`, `time`

## 🚦 Getting Started (Quick)

### One-Line Setup (Windows)
```bash
setup.bat
```

### Manual Setup
```bash
pip install -r requirements.txt
python setup.py
streamlit run app.py
```

### API Keys Required
- **VideoDB**: Free tier (50 uploads) at https://console.videodb.io/
- **Google GenAI**: Free tier at https://aistudio.google.com/app/apikey

## 💡 How It Works (AI Director Process)

### Step 1: Script Understanding
- User provides a narrative script
- Gemini AI breaks it into distinct visual scenes
- Each scene represents a specific moment to be shown

### Step 2: Content Analysis
- Video clips are uploaded to VideoDB
- Automatic transcription creates "spoken index"
- Visual content is analyzed and indexed

### Step 3: Intelligent Matching
- Semantic search matches script scenes to video clips
- AI finds the most relevant footage for each script moment
- Creates an ordered "edit decision list"

### Step 4: Professional Assembly
- VideoDB Timeline Editor stitches clips together
- AI-generated voiceover is added as audio overlay
- Final video is rendered and streamed

### Step 5: Instant Delivery
- User gets professional video immediately
- No video editing skills required
- Ready to share or download

## 🔮 Future Enhancements

### Planned Features
- **Custom voice cloning** for personalized narration
- **Automatic subtitle generation** with styling options
- **Brand element insertion** (logos, intros, outros)
- **Multiple voice options** and languages
- **Advanced timeline editing** with transitions
- **Batch processing** for multiple videos

### Potential Integrations
- YouTube direct upload
- Social media optimization
- Cloud storage integration
- Collaboration features
- Analytics and insights

## 🎖️ Competitive Advantages

### Unique Value Propositions
1. **Zero Learning Curve**: No video editing expertise required
2. **AI-Powered**: Intelligent content matching and assembly
3. **Speed**: Minutes instead of hours for video creation
4. **Quality**: Professional results with minimal input
5. **Accessibility**: Web-based, works on any device
6. **Cost-Effective**: Leverages free tiers of powerful APIs

### Market Differentiation
- First AI video editor specifically for screen recordings
- Semantic understanding of both script and visual content
- Fully automated timeline assembly
- Perfect for technical demonstrations and tutorials

## 📊 Success Metrics

### User Experience
- Time to create video: < 10 minutes
- User satisfaction: High-quality output
- Learning curve: < 5 minutes to first video

### Technical Performance
- Upload success rate: > 95%
- Processing speed: Real-time progress updates
- Output quality: Professional-grade videos

## 🤝 Contributing

The project is open for contributions in:
- UI/UX improvements
- Additional AI model integrations
- Performance optimizations
- Feature enhancements
- Documentation improvements

---

**🎬 Edentic - Where AI meets creativity, and stories become videos!**

*Built with ❤️ for creators, developers, and storytellers everywhere.*
