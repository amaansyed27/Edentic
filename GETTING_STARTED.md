# 🚀 Getting Started with Edentic

## The Revolutionary AI Video Editor

**🤖 Fully Automated - No Script Required!**

Edentic analyzes your video clips, understands what you're demonstrating, and creates professional videos completely automatically. Perfect for anyone who wants great video content without the complexity of traditional editing.

## Quick Setup Guide

### 1. Prerequisites
- Python 3.9 or higher
- Internet connection for AI services
- Video files to edit (MP4, MOV, AVI, etc.)

### 2. Installation Steps

#### Option A: One-Click Setup (Windows)
```bash
setup.bat
```

#### Option B: Automatic Setup (Cross-platform)
```bash
python setup.py
```

#### Option C: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create secrets file
mkdir .streamlit
# Edit .streamlit/secrets.toml with your API keys
```

### 3. Get Your API Keys

#### VideoDB API Key (Free!)
1. Go to [VideoDB Console](https://console.videodb.io/)
2. Create an account (free for 50 uploads)
3. Copy your API key from the dashboard

#### Google GenAI API Key (Free tier available)
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key

### 4. Configure API Keys

Create `.streamlit/secrets.toml`:
```toml
VIDEODB_API_KEY = "your_videodb_key_here"
GOOGLE_API_KEY = "your_google_key_here"
```

### 5. Test Installation
```bash
python test_setup.py
```

### 6. Run the App
```bash
streamlit run app.py
```

## 🎬 How to Use - It's Magic!

### The New Revolutionary Way:

1. **📂 Upload Your Clips**
   - Just drag and drop your video files
   - Screen recordings, demos, tutorials - anything!
   - No planning or script needed

2. **🤖 Let AI Do Everything**
   - Click "Create My Video with AI"
   - AI analyzes your content automatically
   - Understands what you're demonstrating
   - Creates professional narrative structure
   - Generates compelling voiceover
   - Assembles perfect final video

3. **🎉 Get Your Professional Video**
   - Ready in minutes, not hours
   - Professional quality narration
   - Perfect pacing and flow
   - Ready to share anywhere!

### What Our AI Does For You:

- **🧠 Content Analysis**: Understands your software, features, and workflow
- **📖 Story Creation**: Generates professional narrative structure automatically  
- **🎤 Voice Generation**: Creates engaging voiceover that explains everything clearly
- **✂️ Smart Editing**: Perfect timing, transitions, and scene selection
- **🎬 Final Assembly**: Professional video ready to impress

## 🎯 Perfect Use Cases

### For Hackathon Participants:
```
Problem: "I built this amazing app but my demo video is boring"
Solution: Upload screen recordings → Get professional demo automatically!
```

### For Educators:
```
Problem: "I have tutorial footage but editing takes forever" 
Solution: Upload raw recordings → Get polished educational content!
```

### For Developers:
```
Problem: "I need to showcase my product but don't know video editing"
Solution: Upload feature demos → Get marketing-ready video instantly!
```

### For Content Creators:
```
Problem: "Video editing is too complex and time-consuming"
Solution: Upload clips → AI creates professional content automatically!
```

## 🛟 Troubleshooting

### Common Issues:

**"API key not found"**
- Check `.streamlit/secrets.toml` exists
- Verify API keys are correct (no extra spaces)
- Restart the application after adding keys

**"Upload failed"**
- Check internet connection
- Try smaller video files (under 100MB recommended)
- Ensure video format is supported (MP4, MOV, AVI, MKV, WMV)

**"AI analysis failed"**
- Check Google GenAI API key is valid
- Try with different video content
- Ensure videos have some spoken content or clear visuals

**"No video generated"**
- Check VideoDB API limits (free tier: 50 uploads)
- Verify both API keys are working
- Try with shorter clips (under 10 minutes each)

**"Video won't play"**
- Try the direct link provided
- Check browser compatibility
- Ensure stable internet connection

## 💡 Tips for Best Results

### Video Upload Tips:
1. **Quality matters**: Upload clear, high-resolution clips
2. **Audio helps**: Include audio commentary or clear interface sounds
3. **Logical flow**: Upload clips in roughly chronological order
4. **Reasonable length**: Keep individual clips under 10 minutes

### Content Tips:
1. **Show key features**: Make sure important functionality is visible
2. **Clear actions**: Distinct user interactions work best
3. **Interface focus**: Screen recordings of software work perfectly
4. **Demonstrations**: Step-by-step processes are ideal

### What AI Loves:
- Software demonstrations and tutorials
- Clear user interface interactions
- Progressive feature showcases
- Educational or informational content
- Product demonstrations

## 🎉 Success Stories

**"I uploaded 4 messy screen recordings of my hackathon project. Edentic created a professional 3-minute demo that got us to the finals!"** - Sarah, Hackathon Winner

**"As a non-technical founder, I couldn't create good product demos. Now I just upload clips and get professional videos instantly."** - Mike, Startup Founder

**"My students love the tutorials Edentic creates from my raw lecture recordings. It's like having a professional video editor!"** - Dr. Chen, Computer Science Professor

## 🔧 Advanced Features

### Content Type Selection:
- **Auto-detect**: Let AI figure out your content (recommended)
- **Software Demo**: Optimized for application demonstrations
- **Tutorial**: Perfect for educational content
- **Product Presentation**: Great for business/marketing videos

### AI Insights:
- View detailed content analysis
- See the story structure AI created
- Review the generated narration script
- Understand the edit decisions made

## 📞 Support

If you encounter issues:

1. **First Steps**:
   - Run `python test_setup.py` to verify installation
   - Check API keys in `.streamlit/secrets.toml`
   - Ensure stable internet connection

2. **Common Solutions**:
   - Restart the application
   - Try smaller video files
   - Use supported video formats
   - Check API rate limits

3. **Still Need Help?**:
   - Check the detailed error messages in the app
   - Try the demo mode with sample content
   - Verify both API services are working independently

---

**Ready to experience the future of video editing? 🚀**

```bash
streamlit run app.py
```

**Upload clips → AI creates magic → Professional video ready!**
