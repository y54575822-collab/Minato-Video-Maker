"""Pipeline state management for video generation"""
import json
import os
from datetime import datetime

class PipelineManager:
    """Manages pipeline state and checkpoints"""
    
    CHECKPOINT_FILE = 'pipeline_checkpoint.json'
    
    def __init__(self, topic: str, duration_minutes: int = 5):
        self.topic = topic
        self.duration_minutes = duration_minutes
        self.checkpoint_data = self._load_checkpoint()
    
    def _load_checkpoint(self) -> dict:
        """Load checkpoint from file"""
        if os.path.exists(self.CHECKPOINT_FILE):
            with open(self.CHECKPOINT_FILE, 'r') as f:
                return json.load(f)
        return {
            'topic': self.topic,
            'duration_minutes': self.duration_minutes,
            'stage': '1_script',
            'data': {}
        }
    
    def _save_checkpoint(self):
        """Save checkpoint to file"""
        with open(self.CHECKPOINT_FILE, 'w') as f:
            json.dump(self.checkpoint_data, f, indent=2)
    
    def get_stage(self) -> str:
        """Get current pipeline stage"""
        return self.checkpoint_data.get('stage', '1_script')
    
    def set_stage(self, stage: str):
        """Set pipeline stage"""
        self.checkpoint_data['stage'] = stage
        self.checkpoint_data['updated_at'] = datetime.now().isoformat()
        self._save_checkpoint()
        print(f"[Pipeline] Stage updated to: {stage}")
    
    def get_data(self, key: str):
        """Get data from checkpoint"""
        return self.checkpoint_data.get('data', {}).get(key)
    
    def update_data(self, key: str, value):
        """Update checkpoint data"""
        if 'data' not in self.checkpoint_data:
            self.checkpoint_data['data'] = {}
        self.checkpoint_data['data'][key] = value
        self._save_checkpoint()
    
    def get_all_data(self) -> dict:
        """Get all checkpoint data"""
        return self.checkpoint_data
