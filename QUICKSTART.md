# Minato Video Maker - Complete Setup Script

## Quick Installation

### Windows
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Clone and setup
git clone https://github.com/yourusername/Minato-Video-Maker.git
cd Minato-Video-Maker

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup configuration
copy .env.example .env
# Edit .env file with your API keys

# Run server
python web_integration.py
```

### Linux/macOS
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
# Edit .env file with your API keys

# Run server
python web_integration.py
```

## Docker Setup

```bash
# Build image
docker build -t minato-video-maker .

# Run with compose
docker-compose up -d

# Check logs
docker-compose logs -f minato
```

## Verify Installation

```bash
# Check server health
curl http://localhost:5000/api/health

# Should return:
# {"status": "healthy", "service": "Minato Video Maker", "version": "1.0.0"}
```

## Access Points

- 🌐 Web UI: http://localhost:5000
- 📊 Dashboard: http://localhost:5000/dashboard  
- 📡 API: http://localhost:5000/api
- 📖 Documentation: Check README.md

## Required API Keys

1. **OpenAI** - Script generation
2. **Pexels** - Background videos
3. **Muapi** - AI video generation (optional but recommended)

## Production Deployment

For production, use Docker Compose:

```bash
# Create .env file with production keys
cp .env.example .env
# Edit .env with your credentials

# Deploy
docker-compose -f docker-compose.yml up -d

# Setup reverse proxy (Nginx example)
# See NGINX_SETUP.md
```

## Troubleshooting

### FFmpeg not found
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows: Download from https://ffmpeg.org/download.html
```

### API key errors
- Verify keys in .env file
- Check API quotas and billing
- Ensure correct environment variable names

### Port already in use
```bash
# Change port in web_integration.py
# app.run(host='0.0.0.0', port=5001)  # Use different port
```

## Support

For issues or questions, check:
- README.md
- WEBSITE_INTEGRATION.md
- INSTALL.md
- GitHub Issues
