"""Muapi API Client for video and music generation"""
import os
import time
import requests
from typing import List

class MuapiClient:
    """Client for Muapi API interactions"""
    
    def __init__(self):
        self.base_url = os.getenv('MUAPI_BASE_URL', 'https://api.muapi.ai')
        self.api_key = os.getenv('MUAPI_API_KEY')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def trigger_video_generation(self, model: str, prompt: str, aspect_ratio: str = '9:16') -> str:
        """Trigger video generation and return request ID"""
        endpoint = f"{self.base_url}/v1/video-generation"
        payload = {
            'model': model,
            'prompt': prompt,
            'aspect_ratio': aspect_ratio
        }
        
        response = requests.post(endpoint, json=payload, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data.get('request_id')
    
    def trigger_suno_music(self, prompt: str, style: str = 'instrumental') -> str:
        """Trigger Suno music generation"""
        endpoint = f"{self.base_url}/v1/music-generation"
        payload = {
            'model': 'suno-v4',
            'prompt': prompt,
            'style': style
        }
        
        response = requests.post(endpoint, json=payload, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data.get('request_id')
    
    def poll_prediction(self, request_id: str, max_wait: int = 3600) -> List[str]:
        """Poll prediction status and return URLs when complete"""
        endpoint = f"{self.base_url}/v1/prediction/{request_id}"
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            status = data.get('status')
            if status == 'completed':
                return data.get('outputs', [])
            elif status == 'failed':
                raise Exception(f"Generation failed: {data.get('error')}")
            
            time.sleep(5)  # Poll every 5 seconds
        
        raise Exception(f"Generation timeout after {max_wait} seconds")
