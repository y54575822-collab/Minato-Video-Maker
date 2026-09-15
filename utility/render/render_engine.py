"""Video rendering engine using MoviePy"""
import os
import tempfile
from pathlib import Path
from typing import List, Dict, Optional
from moviepy.editor import (
    VideoFileClip, AudioFileClip, CompositeVideoClip, 
    CompositeAudioClip, TextClip, concatenate_videoclips
)
from utility.config import get_config

def get_output_media(
    audio_file_path: str,
    timed_captions: List[Dict],
    background_video_data: List,
    video_server: str = "pexel",
    background_music_path: Optional[str] = None
) -> str:
    """Render final composite video with audio, captions, and background"""
    config = get_config()
    output_file = "rendered_video.mp4"
    
    print("[Render] Loading assets...")
    
    # Load audio
    voiceover = AudioFileClip(audio_file_path)
    duration = voiceover.duration
    
    # Get video dimensions
    orientation_landscape = config.get_video_orientation()
    if orientation_landscape:
        width, height = 1920, 1080
    else:
        width, height = 1080, 1920
    
    # Download and prepare background videos
    print("[Render] Downloading background videos...")
    background_clips = _prepare_background_clips(background_video_data, duration, width, height)
    
    # Create base video
    print("[Render] Compositing background videos...")
    if background_clips:
        background_video = _composite_background(background_clips, width, height, duration)
    else:
        # Create blank video if no background
        from moviepy.video.io.VideoFileClip import VideoFileClip
        from moviepy.video.VideoClip import ColorClip
        background_video = ColorClip(size=(width, height), color=(0, 0, 0)).set_duration(duration)
    
    # Add captions
    print("[Render] Adding captions...")
    if config.CAPTIONS_ENABLED and timed_captions:
        caption_clips = _create_caption_clips(timed_captions, width, height, config)
        if caption_clips:
            composite_clips = [background_video] + caption_clips
            final_video = CompositeVideoClip(composite_clips)
        else:
            final_video = background_video
    else:
        final_video = background_video
    
    # Prepare audio
    print("[Render] Mixing audio...")
    audio_clips = [voiceover]
    if background_music_path and os.path.exists(background_music_path):
        try:
            music = AudioFileClip(background_music_path)
            # Volume down background music
            music = music.volumex(0.3)
            audio_clips.append(music)
        except Exception as e:
            print(f"Warning: Could not load background music: {e}")
    
    # Composite audio
    if len(audio_clips) > 1:
        final_audio = CompositeAudioClip(audio_clips)
    else:
        final_audio = voiceover
    
    final_video = final_video.set_audio(final_audio)
    
    # Render video
    print(f"[Render] Writing to {output_file}...")
    final_video.write_videofile(
        output_file,
        fps=30,
        codec='libx264',
        audio_codec='aac',
        verbose=False,
        logger=None
    )
    
    # Cleanup
    voiceover.close()
    background_video.close()
    final_video.close()
    
    print(f"[Render] Video rendering complete: {output_file}")
    return output_file

def _prepare_background_clips(video_data: List, total_duration: float, width: int, height: int) -> List:
    """Download and prepare background video clips"""
    clips = []
    
    for time_range, video_url in video_data:
        start_time, end_time = time_range
        clip_duration = end_time - start_time
        
        try:
            # Download video
            temp_file = _download_video(video_url)
            
            # Load and resize
            clip = VideoFileClip(temp_file)
            clip = clip.resize((width, height))
            clip = clip.set_start(start_time).set_duration(clip_duration)
            clips.append(clip)
            print(f"Loaded clip for {start_time}s-{end_time}s")
        except Exception as e:
            print(f"Error loading video from {video_url}: {e}")
    
    return clips

def _composite_background(clips: List, width: int, height: int, duration: float) -> 'CompositeVideoClip':
    """Composite multiple background clips"""
    from moviepy.video.VideoClip import ColorClip
    
    # Create blank base
    base = ColorClip(size=(width, height), color=(0, 0, 0)).set_duration(duration)
    
    # Composite all clips
    if clips:
        all_clips = [base] + clips
        return CompositeVideoClip(all_clips)
    else:
        return base

def _create_caption_clips(captions: List[Dict], width: int, height: int, config) -> List:
    """Create text clips for captions"""
    caption_clips = []
    
    for caption in captions:
        start = caption['start']
        end = caption['end']
        text = caption['text']
        
        try:
            # Create text clip
            txt_clip = TextClip(
                text,
                fontsize=config.CAPTION_FONT_SIZE,
                font=config.CAPTION_FONT_FACE,
                color=config.CAPTION_FONT_COLOR,
                stroke_color=config.CAPTION_STROKE_COLOR,
                stroke_width=config.CAPTION_STROKE_WIDTH,
                method='caption',
                size=(width - 100, None)
            )
            
            # Position caption
            position = _get_caption_position(config.CAPTION_POSITION, width, height, txt_clip)
            txt_clip = txt_clip.set_position(position).set_start(start).set_duration(end - start)
            caption_clips.append(txt_clip)
        except Exception as e:
            print(f"Error creating caption: {e}")
    
    return caption_clips

def _get_caption_position(position: str, width: int, height: int, txt_clip):
    """Get caption position based on config"""
    positions = {
        'center': 'center',
        'top': ('center', 50),
        'bottom': ('center', height - 150),
        'bottom_center': ('center', height - 150),
        'bottom_left': (50, height - 150),
        'bottom_right': (width - 50, height - 150)
    }
    return positions.get(position, 'center')

def _download_video(url: str) -> str:
    """Download video from URL"""
    import requests
    import tempfile
    
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    # Save to temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    for chunk in response.iter_content(chunk_size=8192):
        temp_file.write(chunk)
    temp_file.close()
    
    return temp_file.name
