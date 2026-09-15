# Installation Guide

## Linux / macOS

### Prerequisites

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv ffmpeg imagemagick git

# macOS (using Homebrew)
brew install python3 ffmpeg imagemagick
```

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/Minato-Video-Maker.git
cd Minato-Video-Maker

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup configuration
cp .env.example .env

# Edit .env with your API keys
nano .env  # or vim .env
```

## Quick Start

```bash
# Generate 5-minute video
python app.py "Your topic here"

# Generate 10-minute video  
python app.py "Your topic here" --duration 10

# Start API server
python api_server.py
```

## Docker (Optional)

```bash
docker build -t minato-video-maker .
docker run -p 5000:5000 -e OPENAI_API_KEY=your_key minato-video-maker
```
