import os
import asyncio
import argparse
import requests
import imageio_ffmpeg
from pathlib import Path

# Automatically register imageio-ffmpeg binary
ffmpeg_exe_src = imageio_ffmpeg.get_ffmpeg_exe()
bin_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
os.makedirs(bin_dir, exist_ok=True)
ffmpeg_exe_dest = os.path.join(bin_dir, "ffmpeg.exe")

if not os.path.exists(ffmpeg_exe_dest):
    print(f"[Minato] Copying bundled ffmpeg to local bin: {ffmpeg_exe_src} -> {ffmpeg_exe_dest}")
    import shutil
    shutil.copy2(ffmpeg_exe_src, ffmpeg_exe_dest)

if bin_dir not in os.environ["PATH"]:
    os.environ["PATH"] = bin_dir + os.pathsep + os.environ["PATH"]

from utility.script.script_generator import generate_script
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.render.render_engine import get_output_media
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals
from utility.config import get_config
from utility.pipeline_manager import PipelineManager
from utility.muapi_client import MuapiClient

def download_file(url, filename):
    """Download file from URL"""
    print(f"[Minato] Downloading: {url} -> {filename}")
    with open(filename, 'wb') as f:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        f.write(response.content)

def generate_video_from_topic(topic, duration_minutes=5):
    """Main video generation pipeline"""
    print(f"\n{'='*60}")
    print(f"🎬 MINATO VIDEO MAKER - Text to Video Generator")
    print(f"{'='*60}")
    print(f"Topic: {topic}")
    print(f"Duration: {duration_minutes} minutes")
    print(f"{'='*60}\n")
    
    config = get_config()
    orientation_landscape = config.get_video_orientation()
    aspect_ratio = "16:9" if orientation_landscape else "9:16"
    
    # Initialize PipelineManager
    manager = PipelineManager(topic, duration_minutes)
    topic = manager.get_data("topic")
    
    muapi_api_key = os.getenv("MUAPI_API_KEY")
    use_muapi = bool(muapi_api_key)
    
    # Stage 1: Generate Script
    if manager.get_stage() == "1_script":
        print("\n[Stage 1/6] 📝 Generating Script...")
        script = generate_script(topic, duration_minutes)
        print(f"✅ Script generated: {len(script.split())} words")
        manager.update_data("script", script)
        manager.set_stage("2_voiceover")
    
    # Stage 2: Generate Voiceover
    if manager.get_stage() == "2_voiceover":
        print("\n[Stage 2/6] 🎙️ Generating Voiceover...")
        script = manager.get_data("script")
        voiceover_filename = "audio_tts.wav"
        asyncio.run(generate_audio(script, voiceover_filename))
        print(f"✅ Voiceover generated: {voiceover_filename}")
        manager.update_data("voiceover_path", voiceover_filename)
        manager.set_stage("3_timed_captions")
    
    # Stage 3: Generate Timed Captions
    if manager.get_stage() == "3_timed_captions":
        print("\n[Stage 3/6] 📝 Generating Timed Captions...")
        voiceover_filename = manager.get_data("voiceover_path")
        timed_captions = generate_timed_captions(voiceover_filename)
        print(f"✅ Captions generated: {len(timed_captions)} segments")
        manager.update_data("timed_captions", timed_captions)
        manager.set_stage("4_background_music")
    
    # Stage 4: Generate Background Music
    if manager.get_stage() == "4_background_music":
        print("\n[Stage 4/6] 🎵 Generating Background Music...")
        if use_muapi:
            try:
                client = MuapiClient()
                music_style = "instrumental upbeat corporate synth" if orientation_landscape else "instrumental emotional cinematic"
                request_id = client.trigger_suno_music(prompt=topic, style=music_style)
                urls = client.poll_prediction(request_id)
                music_url = urls[0]
                local_music_path = "suno_music.mp3"
                download_file(music_url, local_music_path)
                manager.update_data("background_music_url", music_url)
                manager.update_data("background_music_path", local_music_path)
                print(f"✅ Background music generated: {local_music_path}")
            except Exception as e:
                print(f"⚠️ Music generation failed: {e}. Continuing without music.")
        else:
            print("⚠️ MUAPI_API_KEY not set. Skipping background music.")
        manager.set_stage("5_ai_video_broll")
    
    # Stage 5: Generate B-roll Videos
    if manager.get_stage() == "5_ai_video_broll":
        print("\n[Stage 5/6] 🎥 Generating B-Roll Videos...")
        script = manager.get_data("script")
        timed_captions = manager.get_data("timed_captions")
        search_terms = getVideoSearchQueriesTimed(script, timed_captions)
        
        background_video_urls = manager.get_data("background_video_urls") or []
        model_name = os.getenv("MUAPI_VIDEO_MODEL", "veo3-fast-text-to-video")
        
        if use_muapi:
            client = MuapiClient()
            print(f"Using AI model: {model_name}")
            
            start_index = len(background_video_urls)
            for i, ((t1, t2), queries) in enumerate(search_terms):
                if i < start_index:
                    print(f"Clip {i+1}/{len(search_terms)} already generated. Skipping.")
                    continue
                
                prompt = queries[0] if queries else topic
                print(f"Generating Clip {i+1}/{len(search_terms)} ({t1}s-{t2}s): {prompt}")
                
                try:
                    request_id = client.trigger_video_generation(model_name, prompt, aspect_ratio=aspect_ratio)
                    urls = client.poll_prediction(request_id)
                    video_url = urls[0]
                    background_video_urls.append([[t1, t2], video_url])
                    manager.update_data("background_video_urls", background_video_urls)
                    print(f"✅ Clip {i+1} generated")
                except Exception as e:
                    print(f"⚠️ Clip {i+1} failed: {e}. Using Pexels fallback.")
                    fallback_urls = generate_video_url([[[t1, t2], queries]], "pexel", orientation_landscape=orientation_landscape)
                    if fallback_urls and fallback_urls[0][1]:
                        background_video_urls.append(fallback_urls[0])
                        manager.update_data("background_video_urls", background_video_urls)
        else:
            print("Using Pexels for B-roll (MUAPI not configured)")
            background_video_urls = generate_video_url(search_terms, "pexel", orientation_landscape=orientation_landscape)
            manager.update_data("background_video_urls", background_video_urls)
        
        print(f"✅ B-roll generation complete: {len(background_video_urls)} clips")
        manager.set_stage("6_render")
    
    # Stage 6: Render Final Video
    if manager.get_stage() == "6_render":
        print("\n[Stage 6/6] 🎬 Rendering Final Video...")
        voiceover_path = manager.get_data("voiceover_path")
        timed_captions = manager.get_data("timed_captions")
        background_video_urls = manager.get_data("background_video_urls")
        background_music_path = manager.get_data("background_music_path")
        
        background_video_urls = merge_empty_intervals(background_video_urls)
        
        if background_video_urls:
            print("Compiling media files...")
            video_output = get_output_media(
                audio_file_path=voiceover_path,
                timed_captions=timed_captions,
                background_video_data=background_video_urls,
                video_server="pexel",
                background_music_path=background_music_path
            )
            print(f"\n{'='*60}")
            print(f"✅ SUCCESS! Video created: {video_output}")
            print(f"{'='*60}\n")
            manager.update_data("video_path", video_output)
            manager.set_stage("completed")
        else:
            print("❌ Error: No background video clips found.")
    
    if manager.get_stage() == "completed":
        print("Cleaning up checkpoint...")
        if os.path.exists("pipeline_checkpoint.json"):
            try:
                os.remove("pipeline_checkpoint.json")
            except Exception as e:
                print(f"Cleanup warning: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate videos from text using Minato")
    parser.add_argument("topic", type=str, help="Topic for the video")
    parser.add_argument("--duration", type=int, default=5, help="Duration in minutes (1-24)")
    args = parser.parse_args()
    
    generate_video_from_topic(args.topic, args.duration)
