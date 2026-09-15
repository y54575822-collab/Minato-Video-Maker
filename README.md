# 🎬 Minato Video Maker

**AI-Powered Text-to-Video Generator** - Create stunning videos from 1 to 24 minutes automatically!

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

## ✨ Features

✅ **AI Script Generation** - Automatically generates engaging scripts from topics  
✅ **Multiple LLM Support** - OpenAI, Groq, Google Gemini  
✅ **Text-to-Speech** - EdgeTTS (Free) or ElevenLabs (Premium)  
✅ **Speech-to-Text** - Whisper or Deepgram for accurate captions  
✅ **AI Video Generation** - Google Veo, OpenAI Sora, Kling, and more  
✅ **Auto B-Roll** - Intelligent background video fetching  
✅ **Customizable Captions** - Font, color, position control  
✅ **Multiple Durations** - 1 min to 24 min videos  
✅ **Background Music** - Suno AI music generation  
✅ **Web API** - Flask API for website integration  
✅ **Production Ready** - Checkpoint-based resumable pipeline  

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- FFmpeg
- Node.js (for web frontend - optional)

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/Minato-Video-Maker.git
cd Minato-Video-Maker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup configuration
cp .env.example .env
# Edit .env with your API keys
```

### 🎯 Usage

#### Command Line
```bash
# Generate 5-minute video
python app.py "Your video topic here"

# Generate 10-minute video
python app.py "Your video topic here" --duration 10
```

#### Web API
```bash
# Start API server
python api_server.py

# API will be available at http://localhost:5000
```

## 📡 Web Integration

### Option 1: Flask API (Recommended for Websites)

**Start Server:**
```bash
python api_server.py
```

**API Endpoints:**

#### Generate Video
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Benefits of AI in 2025",
    "duration_minutes": 5,
    "orientation": "portrait"
  }'
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "message": "Video generation started"
}
```

#### Check Status
```bash
curl http://localhost:5000/api/status/550e8400-e29b-41d4-a716-446655440000
```

**Response:**
```json
{
  "status": "processing",
  "topic": "Benefits of AI in 2025",
  "duration": 5,
  "progress": 45
}
```

#### Download Video
```bash
curl http://localhost:5000/api/download/550e8400-e29b-41d4-a716-446655440000 \
  -o video.mp4
```

#### Available Models
```bash
curl http://localhost:5000/api/models
```

### Option 2: HTML/JavaScript Integration

```html
<!DOCTYPE html>
<html>
<head>
    <title>Minato Video Maker</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 600px; margin: 0 auto; }
        input, select { padding: 10px; margin: 10px 0; width: 100%; }
        button { background: #007bff; color: white; padding: 10px 20px; cursor: pointer; }
        #status { margin-top: 20px; padding: 10px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 Minato Video Maker</h1>
        
        <input type="text" id="topic" placeholder="Enter video topic..." />
        <select id="duration">
            <option value="1">1 minute</option>
            <option value="5" selected>5 minutes</option>
            <option value="10">10 minutes</option>
            <option value="24">24 minutes</option>
        </select>
        <button onclick="generateVideo()">Generate Video</button>
        
        <div id="status"></div>
    </div>

    <script>
        const API_URL = 'http://localhost:5000/api';
        let currentJobId = null;

        async function generateVideo() {
            const topic = document.getElementById('topic').value;
            const duration = document.getElementById('duration').value;
            
            if (!topic) {
                alert('Please enter a topic');
                return;
            }

            document.getElementById('status').innerHTML = '⏳ Starting video generation...';

            try {
                const response = await fetch(`${API_URL}/generate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        topic: topic,
                        duration_minutes: parseInt(duration),
                        orientation: 'portrait'
                    })
                });

                const data = await response.json();
                currentJobId = data.job_id;
                
                document.getElementById('status').innerHTML = `✅ Generation started (Job: ${data.job_id})`;
                
                // Poll status
                pollStatus();
            } catch (error) {
                document.getElementById('status').innerHTML = `❌ Error: ${error.message}`;
            }
        }

        async function pollStatus() {
            if (!currentJobId) return;

            try {
                const response = await fetch(`${API_URL}/status/${currentJobId}`);
                const data = await response.json();

                let statusHtml = `
                    <strong>Status:</strong> ${data.status.toUpperCase()}<br>
                    <strong>Topic:</strong> ${data.topic}<br>
                    <strong>Duration:</strong> ${data.duration} minutes<br>
                    <strong>Progress:</strong> ${data.progress}%
                `;

                if (data.status === 'completed') {
                    statusHtml += `<br><br>
                        <a href="${API_URL}/download/${currentJobId}" download>
                            ✅ Download Video
                        </a>`;
                } else if (data.status === 'failed') {
                    statusHtml += `<br><span style="color:red;">Error: ${data.error}</span>`;
                } else {
                    // Poll again in 5 seconds
                    setTimeout(pollStatus, 5000);
                }

                document.getElementById('status').innerHTML = statusHtml;
            } catch (error) {
                document.getElementById('status').innerHTML = `❌ Error: ${error.message}`;
            }
        }
    </script>
</body>
</html>
```

### Option 3: Python Integration

```python
import requests
import time

API_URL = 'http://localhost:5000/api'

def create_video(topic, duration=5):
    # Start generation
    response = requests.post(f'{API_URL}/generate', json={
        'topic': topic,
        'duration_minutes': duration,
        'orientation': 'portrait'
    })
    
    data = response.json()
    job_id = data['job_id']
    print(f"Job started: {job_id}")
    
    # Poll status
    while True:
        status_response = requests.get(f'{API_URL}/status/{job_id}')
        status_data = status_response.json()
        
        print(f"Status: {status_data['status']} ({status_data['progress']}%)")
        
        if status_data['status'] == 'completed':
            # Download video
            video_response = requests.get(f'{API_URL}/download/{job_id}')
            with open('output.mp4', 'wb') as f:
                f.write(video_response.content)
            print("Video saved as output.mp4")
            break
        elif status_data['status'] == 'failed':
            print(f"Error: {status_data['error']}")
            break
        
        time.sleep(5)  # Check every 5 seconds

# Create video
create_video('How to use AI tools in 2025', duration=10)
```

## 🔑 API Keys Required

| Service | Purpose | Get Key |
|---------|---------|----------|
| **OpenAI** | Script Generation | [platform.openai.com](https://platform.openai.com/api-keys) |
| **Groq** | Fast Script Generation | [console.groq.com](https://console.groq.com/keys) |
| **Google Gemini** | Alternative Script Gen | [makersuite.google.com](https://makersuite.google.com/app/apikey) |
| **Pexels** | Background Videos | [pexels.com/api](https://www.pexels.com/api/new/) |
| **Muapi** | AI Video Generation | [muapi.ai](https://muapi.ai) |
| **ElevenLabs** | Premium TTS | [elevenlabs.io](https://elevenlabs.io/) |
| **Deepgram** | Premium STT | [console.deepgram.com](https://console.deepgram.com/) |

## ⚙️ Configuration

Edit `.env` file:

```env
# LLM Provider
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here

# Video Settings
VIDEO_ORIENTATION=portrait  # or landscape
VIDEO_DURATION_MINUTES=5    # 1-24

# Audio Settings
TTS_PROVIDER=edgetts  # Free option
STT_PROVIDER=whisper  # Free option

# AI Video Generation
MUAPI_API_KEY=your_key_here
MUAPI_VIDEO_MODEL=veo3-fast-text-to-video

# Captions
CAPTIONS_ENABLED=true
CAPTION_FONT_SIZE=100
CAPTION_POSITION=bottom_center
```

## 🎨 Supported Video Models

- **Google Veo 3** (Fast & Quality)
- **OpenAI Sora 2** (Cinematic)
- **Kling v3** (Professional)
- **ByteDance Seedance** (Fast)
- **xAI Grok** (Creative)
- **Alibaba Happy Horse** (1080p)
- And more via Muapi!

## 📊 Pipeline Stages

1. **Script Generation** - AI creates engaging script
2. **Voiceover** - Text-to-Speech audio generation
3. **Captions** - Speech-to-Text timing
4. **Background Music** - AI music generation (optional)
5. **B-Roll Videos** - AI or stock video fetching
6. **Final Render** - Composite all media into video

## 🐛 Troubleshooting

**FFmpeg not found:**
```bash
# Install FFmpeg
# Ubuntu/Debian: sudo apt-get install ffmpeg
# Mac: brew install ffmpeg
# Windows: Download from https://ffmpeg.org/download.html
```

**API Key errors:**
- Verify all required API keys in `.env`
- Check API quotas and billing

**Video generation fails:**
- Increase `max_wait` in `muapi_client.py`
- Check internet connection
- Verify Muapi API status

## 📄 License

MIT License - Free for personal and commercial use

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## 📞 Support

For issues and questions:
- Open GitHub Issues
- Check Documentation
- Review Examples

---

**Made with ❤️ by Minato Team**

[⭐ Star us on GitHub](https://github.com/yourusername/Minato-Video-Maker)
