@echo off
echo 🎬 Edentic AI Video Editor - Windows Setup
echo ==========================================

echo.
echo 📦 Installing Python packages...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Package installation failed
    pause
    exit /b 1
)

echo.
echo ✅ Packages installed successfully!

echo.
echo 🔑 Setting up API keys...
echo You need to get API keys from:
echo - VideoDB: https://console.videodb.io/
echo - Google GenAI: https://aistudio.google.com/app/apikey

if not exist ".streamlit" mkdir .streamlit

echo.
set /p VIDEODB_KEY="Enter your VideoDB API Key: "
set /p GOOGLE_KEY="Enter your Google GenAI API Key: "

echo VIDEODB_API_KEY = "%VIDEODB_KEY%" > .streamlit\secrets.toml
echo GOOGLE_API_KEY = "%GOOGLE_KEY%" >> .streamlit\secrets.toml

echo.
echo ✅ Configuration complete!

echo.
echo 🧪 Testing setup...
python test_setup.py

if %errorlevel% neq 0 (
    echo ❌ Setup test failed
    pause
    exit /b 1
)

echo.
echo 🎉 Setup successful! 
echo.
echo 🚀 Starting Edentic...
echo The app will open in your browser at http://localhost:8501
echo.
pause
streamlit run app.py
