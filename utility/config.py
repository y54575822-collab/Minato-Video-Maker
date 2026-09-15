"""Configuration management for Minato"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for Minato Video Maker"""
    
    # LLM Configuration
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama3-70b-8192')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
    
    # Video Configuration
    PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
    VIDEO_ORIENTATION = os.getenv('VIDEO_ORIENTATION', 'portrait')
    VIDEO_DURATION_MINUTES = int(os.getenv('VIDEO_DURATION_MINUTES', 5))
    
    # Audio Configuration
    TTS_PROVIDER = os.getenv('TTS_PROVIDER', 'edgetts')
    STT_PROVIDER = os.getenv('STT_PROVIDER', 'whisper')
    EDGETTS_VOICE = os.getenv('EDGETTS_VOICE', 'en-AU-WilliamNeural')
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    ELEVENLABS_VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID')
    DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
    
    # Caption Configuration
    CAPTIONS_ENABLED = os.getenv('CAPTIONS_ENABLED', 'true').lower() == 'true'
    CAPTION_FONT_SIZE = int(os.getenv('CAPTION_FONT_SIZE', 100))
    CAPTION_FONT_COLOR = os.getenv('CAPTION_FONT_COLOR', 'white')
    CAPTION_FONT_FACE = os.getenv('CAPTION_FONT_FACE', 'Arial-Bold')
    CAPTION_STROKE_WIDTH = int(os.getenv('CAPTION_STROKE_WIDTH', 3))
    CAPTION_STROKE_COLOR = os.getenv('CAPTION_STROKE_COLOR', 'black')
    CAPTION_POSITION = os.getenv('CAPTION_POSITION', 'bottom_center')
    
    # Muapi Configuration
    MUAPI_BASE_URL = os.getenv('MUAPI_BASE_URL', 'https://api.muapi.ai')
    MUAPI_API_KEY = os.getenv('MUAPI_API_KEY')
    MUAPI_VIDEO_MODEL = os.getenv('MUAPI_VIDEO_MODEL', 'veo3-fast-text-to-video')
    
    # Render Engine
    RENDER_ENGINE = os.getenv('RENDER_ENGINE', 'moviepy')
    REMOTION_THEME = os.getenv('REMOTION_THEME', 'flat-motion-graphics')
    
    # Flask Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'minato-secret-key-change-in-production')
    
    def get_video_orientation(self):
        """Get video orientation (True for landscape, False for portrait)"""
        return self.VIDEO_ORIENTATION.lower() == 'landscape'

def get_config():
    """Get configuration instance"""
    return Config()
