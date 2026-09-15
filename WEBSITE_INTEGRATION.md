# WEBSITE INTEGRATION GUIDE

## 🚀 Complete Setup for Your Website

### Option 1: Quick Setup (Recommended)

#### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/Minato-Video-Maker.git
cd Minato-Video-Maker
```

#### Step 2: Setup Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your keys
```

#### Step 3: Run Web Integration Server
```bash
python web_integration.py
```

**Server will be available at:**
- 🌐 Web UI: `http://localhost:5000`
- 📊 Dashboard: `http://localhost:5000/dashboard`
- 📡 API: `http://localhost:5000/api`

---

## 📝 Complete Website Integration Code

### Single HTML File for Your Website

Save this as `video-generator.html` in your website:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Generator - Your Website</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        header h1 { font-size: 2em; margin-bottom: 10px; }
        .content { padding: 40px; }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            margin-bottom: 10px;
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .status {
            background: #f5f5f5;
            border-left: 4px solid #667eea;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            display: none;
        }
        .status.show { display: block; }
        .status.success { border-left-color: #4CAF50; background: #d4edda; }
        .status.error { border-left-color: #f44336; background: #f8d7da; }
        .status.processing { border-left-color: #2196F3; background: #d1ecf1; }
        .progress {
            width: 100%;
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 10px;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s;
        }
        .download-btn {
            display: none;
            width: 100%;
            padding: 14px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            margin-top: 10px;
        }
        .download-btn.show { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎬 Video Generator</h1>
            <p>Create professional videos with AI</p>
        </header>
        <div class="content">
            <form id="videoForm" onsubmit="handleSubmit(event)">
                <div class="form-group">
                    <label for="topic">📝 Video Topic</label>
                    <input 
                        type="text" 
                        id="topic" 
                        placeholder="e.g., How to learn AI, Benefits of Machine Learning..."
                        required
                    />
                </div>
                <div class="form-group">
                    <label for="duration">⏱️ Duration</label>
                    <select id="duration">
                        <option value="1">1 Minute</option>
                        <option value="2">2 Minutes</option>
                        <option value="3">3 Minutes</option>
                        <option value="5" selected>5 Minutes</option>
                        <option value="10">10 Minutes</option>
                        <option value="15">15 Minutes</option>
                        <option value="20">20 Minutes</option>
                        <option value="24">24 Minutes</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="orientation">📱 Format</label>
                    <select id="orientation">
                        <option value="portrait">Portrait (Shorts)</option>
                        <option value="landscape">Landscape (Traditional)</option>
                    </select>
                </div>
                <button type="submit" id="generateBtn">✨ Generate Video</button>
            </form>
            <div id="status" class="status">
                <div id="statusText"></div>
                <div class="progress"><div class="progress-fill" id="progressFill"></div></div>
            </div>
            <button class="download-btn" id="downloadBtn" onclick="downloadVideo()">⬇️ Download Video</button>
        </div>
    </div>

    <script>
        const API_URL = 'http://localhost:5000/api';
        let currentJobId = null;
        let pollInterval = null;

        async function handleSubmit(event) {
            event.preventDefault();
            
            const topic = document.getElementById('topic').value;
            const duration = document.getElementById('duration').value;
            const orientation = document.getElementById('orientation').value;
            
            const generateBtn = document.getElementById('generateBtn');
            generateBtn.disabled = true;
            generateBtn.textContent = '⏳ Starting...';
            
            document.getElementById('downloadBtn').classList.remove('show');
            showStatus('processing', '⏳ Initializing video generation...');
            
            try {
                const response = await fetch(`${API_URL}/generate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        topic: topic,
                        duration_minutes: parseInt(duration),
                        orientation: orientation
                    })
                });
                
                const data = await response.json();
                currentJobId = data.job_id;
                showStatus('processing', `✅ Generation started! Job ID: ${data.job_id}`);
                
                startPolling();
            } catch (error) {
                generateBtn.disabled = false;
                generateBtn.textContent = '✨ Generate Video';
                showStatus('error', `❌ Error: ${error.message}`);
            }
        }
        
        function showStatus(type, message) {
            const statusDiv = document.getElementById('status');
            statusDiv.classList.add('show');
            statusDiv.classList.remove('success', 'error', 'processing');
            statusDiv.classList.add(type);
            document.getElementById('statusText').innerHTML = message;
        }
        
        function startPolling() {
            if (pollInterval) clearInterval(pollInterval);
            pollInterval = setInterval(pollStatus, 3000);
        }
        
        async function pollStatus() {
            if (!currentJobId) return;
            
            try {
                const response = await fetch(`${API_URL}/status/${currentJobId}`);
                const data = await response.json();
                
                const progressFill = document.getElementById('progressFill');
                progressFill.style.width = `${data.progress}%`;
                
                if (data.status === 'completed') {
                    clearInterval(pollInterval);
                    document.getElementById('generateBtn').disabled = false;
                    document.getElementById('generateBtn').textContent = '✨ Generate Video';
                    document.getElementById('downloadBtn').classList.add('show');
                    showStatus('success', '🎉 Video ready! Click download below.');
                } else if (data.status === 'failed') {
                    clearInterval(pollInterval);
                    document.getElementById('generateBtn').disabled = false;
                    document.getElementById('generateBtn').textContent = '✨ Generate Video';
                    showStatus('error', `❌ Error: ${data.error || 'Unknown error'}`);
                } else {
                    showStatus('processing', `⏳ Processing... ${data.progress}%`);
                }
            } catch (error) {
                console.error('Poll error:', error);
            }
        }
        
        function downloadVideo() {
            if (currentJobId) {
                window.location.href = `${API_URL}/download/${currentJobId}`;
            }
        }
    </script>
</body>
</html>
```

---

## 🔧 Integration Methods

### Method 1: Embed in Your Website (HTML)

```html
<!-- Add to your website HTML -->
<iframe src="http://your-server.com:5000" width="100%" height="600"></iframe>
```

### Method 2: JavaScript API Call

```javascript
// In your website's JavaScript
async function generateVideo(topic, duration) {
    const response = await fetch('http://your-server.com:5000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            topic: topic,
            duration_minutes: duration,
            orientation: 'portrait'
        })
    });
    
    const data = await response.json();
    return data.job_id;
}

// Check status
async function checkStatus(jobId) {
    const response = await fetch(`http://your-server.com:5000/api/status/${jobId}`);
    return await response.json();
}

// Download video
function downloadVideo(jobId) {
    window.location.href = `http://your-server.com:5000/api/download/${jobId}`;
}
```

### Method 3: Backend Integration (Node.js/Express)

```javascript
const express = require('express');
const axios = require('axios');
const app = express();

const MINATO_API = 'http://localhost:5000/api';

app.post('/api/create-video', async (req, res) => {
    try {
        const { topic, duration } = req.body;
        
        const response = await axios.post(`${MINATO_API}/generate`, {
            topic: topic,
            duration_minutes: duration,
            orientation: 'portrait'
        });
        
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/video-status/:jobId', async (req, res) => {
    try {
        const response = await axios.get(`${MINATO_API}/status/${req.params.jobId}`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});
```

### Method 4: Backend Integration (PHP)

```php
<?php
define('MINATO_API', 'http://localhost:5000/api');

function generateVideo($topic, $duration) {
    $data = [
        'topic' => $topic,
        'duration_minutes' => (int)$duration,
        'orientation' => 'portrait'
    ];
    
    $ch = curl_init(MINATO_API . '/generate');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    
    $response = curl_exec($ch);
    curl_close($ch);
    
    return json_decode($response, true);
}

function getVideoStatus($jobId) {
    $ch = curl_init(MINATO_API . '/status/' . $jobId);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);
    return json_decode($response, true);
}

// Usage
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $result = generateVideo($_POST['topic'], $_POST['duration']);
    header('Content-Type: application/json');
    echo json_encode($result);
}
?>
```

### Method 5: Backend Integration (Python/Django)

```python
import requests
from django.http import JsonResponse

MINATO_API = 'http://localhost:5000/api'

def generate_video(request):
    if request.method == 'POST':
        data = {
            'topic': request.POST.get('topic'),
            'duration_minutes': int(request.POST.get('duration', 5)),
            'orientation': request.POST.get('orientation', 'portrait')
        }
        
        response = requests.post(f'{MINATO_API}/generate', json=data)
        return JsonResponse(response.json())

def video_status(request, job_id):
    response = requests.get(f'{MINATO_API}/status/{job_id}')
    return JsonResponse(response.json())
```

---

## 🐳 Docker Deployment

Save as `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 5000

# Run server
CMD ["python", "web_integration.py"]
```

**Build and Run:**

```bash
# Build image
docker build -t minato-video-maker .

# Run container
docker run -p 5000:5000 \
  -e OPENAI_API_KEY=your_key \
  -e PEXELS_API_KEY=your_key \
  -e MUAPI_API_KEY=your_key \
  minato-video-maker
```

---

## 🔌 API Reference

### Generate Video
**POST** `/api/generate`

```json
{
  "topic": "How to use AI",
  "duration_minutes": 5,
  "orientation": "portrait"
}
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "message": "Video generation started"
}
```

### Check Status
**GET** `/api/status/{job_id}`

**Response:**
```json
{
  "status": "processing",
  "progress": 45,
  "topic": "How to use AI",
  "duration": 5
}
```

### Download Video
**GET** `/api/download/{job_id}`

Returns: MP4 video file

### List Videos
**GET** `/api/videos`

**Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "topic": "How to use AI",
    "duration": 5,
    "status": "completed",
    "created_at": "2025-09-15T10:00:00"
  }
]
```

### Get Available Models
**GET** `/api/models`

---

## ⚙️ Environment Configuration

Create `.env` file:

```env
# LLM
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...

# Video
PEXELS_API_KEY=your_key
VIDEO_DURATION_MINUTES=5
VIDEO_ORIENTATION=portrait

# AI Video Generation
MUAPI_API_KEY=your_key
MUAPI_VIDEO_MODEL=veo3-fast-text-to-video

# TTS/STT
TTS_PROVIDER=edgetts
STT_PROVIDER=whisper

# Server
FLASK_ENV=production
DEBUG=false
SECRET_KEY=your_secret_key
```

---

## 🚀 Deployment Checklist

- [ ] All API keys configured
- [ ] FFmpeg installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Test video generation: `python app.py "Test topic"`
- [ ] Start web server: `python web_integration.py`
- [ ] Access at: `http://localhost:5000`
- [ ] Set up reverse proxy (Nginx/Apache) for production
- [ ] Enable HTTPS
- [ ] Setup database for job persistence
- [ ] Configure automated backups
- [ ] Monitor server logs

---

## 📞 Support

For issues:
1. Check `.env` configuration
2. Verify API keys
3. Check server logs
4. See GitHub Issues

**Made with ❤️ by Minato Team**
