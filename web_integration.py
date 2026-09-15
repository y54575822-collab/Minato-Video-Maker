"""Complete integrated solution for embedding Minato in websites"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import uuid
import threading
from datetime import datetime
from app import generate_video_from_topic

app = Flask(__name__)
CORS(app)

# Store job status in memory (use database for production)
jobs_db = {}

@app.route('/', methods=['GET'])
def home():
    """Serve main application"""
    return send_file('web/index.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Serve dashboard"""
    return send_file('web/dashboard.html')

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'Minato Video Maker',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/generate', methods=['POST'])
def generate_video():
    """Generate video endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'topic' not in data:
            return jsonify({'error': 'Topic is required'}), 400
        
        topic = data.get('topic')
        duration = min(int(data.get('duration_minutes', 5)), 24)
        
        if not (1 <= duration <= 24):
            return jsonify({'error': 'Duration must be 1-24 minutes'}), 400
        
        # Create job
        job_id = str(uuid.uuid4())
        jobs_db[job_id] = {
            'id': job_id,
            'status': 'processing',
            'topic': topic,
            'duration': duration,
            'progress': 10,
            'video_path': None,
            'error': None,
            'created_at': datetime.now().isoformat()
        }
        
        # Run in background
        def run_generation():
            try:
                jobs_db[job_id]['progress'] = 20
                video_path = generate_video_from_topic(topic, duration)
                jobs_db[job_id]['status'] = 'completed'
                jobs_db[job_id]['progress'] = 100
                jobs_db[job_id]['video_path'] = video_path
            except Exception as e:
                jobs_db[job_id]['status'] = 'failed'
                jobs_db[job_id]['error'] = str(e)
        
        thread = threading.Thread(target=run_generation, daemon=True)
        thread.start()
        
        return jsonify({
            'job_id': job_id,
            'status': 'queued',
            'message': 'Video generation started'
        }), 202
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status/<job_id>', methods=['GET'])
def get_status(job_id):
    """Get job status"""
    if job_id not in jobs_db:
        return jsonify({'error': 'Job not found'}), 404
    return jsonify(jobs_db[job_id])

@app.route('/api/download/<job_id>', methods=['GET'])
def download_video(job_id):
    """Download generated video"""
    if job_id not in jobs_db:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs_db[job_id]
    if job['status'] != 'completed':
        return jsonify({'error': 'Video not ready'}), 400
    
    video_path = job['video_path']
    if not video_path or not os.path.exists(video_path):
        return jsonify({'error': 'Video not found'}), 404
    
    return send_file(video_path, mimetype='video/mp4', as_attachment=True, download_name='minato_video.mp4')

@app.route('/api/videos', methods=['GET'])
def list_videos():
    """List all generated videos"""
    videos = list(jobs_db.values())
    return jsonify(videos)

@app.route('/api/videos/<job_id>', methods=['DELETE'])
def delete_video(job_id):
    """Delete video job"""
    if job_id in jobs_db:
        job = jobs_db[job_id]
        if job['video_path'] and os.path.exists(job['video_path']):
            try:
                os.remove(job['video_path'])
            except:
                pass
        del jobs_db[job_id]
        return jsonify({'message': 'Video deleted'})
    return jsonify({'error': 'Job not found'}), 404

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available models"""
    return jsonify({
        'ai_models': [
            {'id': 'veo3-fast-text-to-video', 'name': 'Google Veo 3 (Fast)', 'speed': 'fast', 'quality': 'high'},
            {'id': 'kling-v3.0-pro-text-to-video', 'name': 'Kling v3 Pro', 'speed': 'normal', 'quality': 'cinematic'},
            {'id': 'openai-sora-2-pro-text-to-video', 'name': 'OpenAI Sora 2 Pro', 'speed': 'slow', 'quality': 'premium'},
            {'id': 'seedance-pro-t2v', 'name': 'ByteDance Seedance', 'speed': 'normal', 'quality': 'high'},
        ],
        'durations': [1, 2, 3, 5, 10, 15, 20, 24],
        'orientations': ['portrait', 'landscape'],
        'tts_providers': ['edgetts', 'elevenlabs'],
        'stt_providers': ['whisper', 'deepgram'],
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎬 MINATO VIDEO MAKER - PRODUCTION SERVER")
    print("="*60)
    print(f"\n✅ Server starting at http://0.0.0.0:5000")
    print(f"\n📌 Access URLs:")
    print(f"   - Web UI: http://localhost:5000")
    print(f"   - Dashboard: http://localhost:5000/dashboard")
    print(f"   - API: http://localhost:5000/api")
    print(f"\n📚 API Endpoints:")
    print(f"   POST /api/generate - Create video")
    print(f"   GET /api/status/<job_id> - Check status")
    print(f"   GET /api/download/<job_id> - Download video")
    print(f"   GET /api/models - List available models")
    print(f"\n" + "="*60 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000)
