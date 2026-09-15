"""Caption generation module"""
import subprocess
import json
from utility.config import get_config

def generate_timed_captions(audio_file_path: str) -> list:
    """Generate timed captions from audio using STT"""
    config = get_config()
    provider = config.STT_PROVIDER.lower()
    
    if provider == 'whisper':
        return _generate_with_whisper(audio_file_path, config)
    elif provider == 'deepgram':
        return _generate_with_deepgram(audio_file_path, config)
    else:
        raise ValueError(f"Unknown STT provider: {provider}")

def _generate_with_whisper(audio_file_path: str, config) -> list:
    """Generate captions using Whisper"""
    import whisper
    from whisper_timestamped import transcribe_timestamped
    
    print(f"Loading Whisper model...")
    result = transcribe_timestamped(audio_file_path, language="en", device="cpu")
    
    captions = []
    for segment in result['segments']:
        start = segment['start']
        end = segment['end']
        text = segment['text'].strip()
        
        if text:
            captions.append({
                'start': start,
                'end': end,
                'text': text
            })
    
    return captions

def _generate_with_deepgram(audio_file_path: str, config) -> list:
    """Generate captions using Deepgram"""
    from deepgram import DeepgramClient, PrerecordedOptions
    
    client = DeepgramClient(api_key=config.DEEPGRAM_API_KEY)
    
    with open(audio_file_path, 'rb') as f:
        audio_data = f.read()
    
    options = PrerecordedOptions(
        model="nova-2",
        language="en",
        smart_format=True,
        utterances=True
    )
    
    response = client.listen.prerecorded.transcribe_file(
        audio_data,
        options
    )
    
    captions = []
    if response.results and response.results.utterances:
        for utterance in response.results.utterances:
            if hasattr(utterance, 'words') and utterance.words:
                start = utterance.words[0].start
                end = utterance.words[-1].end
                text = ' '.join([w.word for w in utterance.words])
                
                captions.append({
                    'start': start,
                    'end': end,
                    'text': text
                })
    
    return captions
