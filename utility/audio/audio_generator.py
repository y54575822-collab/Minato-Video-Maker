"""Audio generation module (TTS - Text to Speech)"""
import asyncio
from utility.config import get_config

async def generate_audio(script: str, output_filename: str = 'audio_tts.wav'):
    """Generate audio from script using TTS"""
    config = get_config()
    provider = config.TTS_PROVIDER.lower()
    
    if provider == 'edgetts':
        await _generate_with_edgetts(script, output_filename, config)
    elif provider == 'elevenlabs':
        await _generate_with_elevenlabs(script, output_filename, config)
    else:
        raise ValueError(f"Unknown TTS provider: {provider}")
    
    print(f"Audio saved to {output_filename}")

async def _generate_with_edgetts(script: str, output_filename: str, config):
    """Generate audio using EdgeTTS (free)"""
    import edge_tts
    
    voice = config.EDGETTS_VOICE
    communicate = edge_tts.Communicate(text=script, voice=voice, rate="+0%")
    await communicate.save(output_filename)
    print(f"EdgeTTS generated audio with voice: {voice}")

async def _generate_with_elevenlabs(script: str, output_filename: str, config):
    """Generate audio using ElevenLabs"""
    from elevenlabs.client import ElevenLabs
    
    client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)
    audio = client.generate(
        text=script,
        voice=config.ELEVENLABS_VOICE_ID,
        model="eleven_monolingual_v1"
    )
    
    with open(output_filename, 'wb') as f:
        for chunk in audio:
            f.write(chunk)
    print(f"ElevenLabs generated audio")
