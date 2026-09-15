# Windows Installation Guide

## Prerequisites

### 1. Install Python
- Download Python 3.10+ from [python.org](https://www.python.org/downloads/)
- **Important:** Check "Add Python to PATH" during installation

### 2. Install FFmpeg

**Option A: Using Chocolatey (Recommended)**
```powershell
# Open PowerShell as Administrator
choco install ffmpeg
```

**Option B: Manual Installation**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to System PATH

### 3. Install Git
- Download from [git-scm.com](https://git-scm.com/)
- Use default installation settings

## Setup Steps

```powershell
# Open Command Prompt or PowerShell

# Navigate to desired directory
cd C:\Users\YourUsername\Documents

# Clone repository
git clone https://github.com/yourusername/Minato-Video-Maker.git
cd Minato-Video-Maker

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Edit .env with your API keys (use Notepad)
notepadsrc\.env
```

## Running the Application

```powershell
# Activate venv (if not already activated)
.\venv\Scripts\activate

# Run command line
python app.py "Your video topic"

# Or run API server
python api_server.py
```

## Common Issues

### "Python not found"
- Add Python to PATH: https://docs.python.org/3/using/windows.html#finding-the-python-executable

### "FFmpeg not found"
```powershell
# Verify FFmpeg installation
ffmpeg -version

# If not found, reinstall and check PATH
```

### "Module not found"
```powershell
# Make sure venv is activated and reinstall
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Port 5000 already in use
```powershell
# Edit api_server.py, change port:
app.run(host='0.0.0.0', port=5001)  # Use 5001 instead
```
