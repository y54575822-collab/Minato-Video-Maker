"""Flask API server for Minato Video Maker"""
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from app import generate_video_from_topic
import threading

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}

# Store job status
jobs = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Minato Video Maker API',
        'version': '1.0.0'
    }), 200

@app.route('/api/generate', methods=['POST'])
def generate():
    """Generate video from text
    
    Request JSON:
    {
        "topic": "Your video topic",
        "duration_minutes": 5,
        "orientation": "portrait"  # or "landscape"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'topic' not in data:
            return jsonify({'error': 'Topic is required'}), 400
        
        topic = data.get('topic')
        duration = data.get('duration_minutes', 5)
        
        # Validate duration
        if not (1 <= duration <= 24):
            return jsonify({'error': 'Duration must be between 1-24 minutes'}), 400
        
        # Generate unique job ID
        import uuid
        job_id = str(uuid.uuid4())
        
        # Store job status
        jobs[job_id] = {
            'status': 'processing',
            'topic': topic,
            'duration': duration,
            'progress': 0,
            'video_path': None,
            'error': None
        }
        
        # Run generation in background thread
        def run_generation():
            try:
                generate_video_from_topic(topic, duration)
                jobs[job_id]['status'] = 'completed'
                jobs[job_id]['progress'] = 100
                jobs[job_id]['video_path'] = 'rendered_video.mp4'
            except Exception as e:
                jobs[job_id]['status'] = 'failed'
                jobs[job_id]['error'] = str(e)
        
        thread = threading.Thread(target=run_generation)
        thread.daemon = True
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
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(jobs[job_id]), 200

@app.route('/api/download/<job_id>', methods=['GET'])
def download_video(job_id):
    """Download generated video"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    if job['status'] != 'completed':
        return jsonify({'error': 'Video not ready'}), 400
    
    video_path = job['video_path']
    if not os.path.exists(video_path):
        return jsonify({'error': 'Video file not found'}), 404
    
    from flask import send_file
    return send_file(
        video_path,
        mimetype='video/mp4',
        as_attachment=True,
        download_name='minato_video.mp4'
    )

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available video generation models"""
    models = {
        'ai_models': [
            {'id': 'veo3-fast-text-to-video', 'name': 'Google Veo 3 (Fast)', 'speed': 'fast'},
            {'id': 'veo3-text-to-video', 'name': 'Google Veo 3', 'speed': 'normal'},
            {'id': 'kling-v3.0-pro-text-to-video', 'name': 'Kling v3 Pro', 'speed': 'normal'},
            {'id': 'seedance-pro-t2v', 'name': 'ByteDance Seedance Pro', 'speed': 'normal'},
            {'id': 'openai-sora-2-pro-text-to-video', 'name': 'OpenAI Sora 2', 'speed': 'slow'},
        ],
        'tts_providers': ['edgetts', 'elevenlabs'],
        'stt_providers': ['whisper', 'deepgram'],
        'durations': [1, 2, 3, 5, 10, 15, 20, 24]
    }
    return jsonify(models), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Minato Video Maker API Server...")
    print("API Documentation: http://localhost:5000/api/health")
    app.run(debug=os.getenv('DEBUG', 'false').lower() == 'true', host='0.0.0.0', port=5000)
