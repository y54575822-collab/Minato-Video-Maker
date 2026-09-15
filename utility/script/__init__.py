"""Script generation module using LLM"""
import os
from utility.config import get_config

def generate_script(topic: str, duration_minutes: int = 5) -> str:
    """Generate script using LLM based on topic and duration"""
    config = get_config()
    provider = config.LLM_PROVIDER.lower()
    
    # Estimate words based on duration (average 130-150 words per minute of speech)
    target_words = duration_minutes * 140
    
    prompt = f"""
You are a professional video script writer. Create an engaging, informative script for a video about: {topic}

Requirements:
- Target length: approximately {target_words} words (for {duration_minutes} minutes of voiceover)
- Make it engaging and conversational
- Include hook in first 10 seconds
- Add clear section breaks
- Make it suitable for YouTube/social media
- Ensure smooth flow and natural pauses

Write only the script, no additional commentary.
"""
    
    if provider == 'openai':
        return _generate_with_openai(prompt, config)
    elif provider == 'groq':
        return _generate_with_groq(prompt, config)
    elif provider == 'gemini':
        return _generate_with_gemini(prompt, config)
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")

def _generate_with_openai(prompt: str, config) -> str:
    """Generate script using OpenAI"""
    from openai import OpenAI
    
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000
    )
    return response.choices[0].message.content

def _generate_with_groq(prompt: str, config) -> str:
    """Generate script using Groq"""
    from groq import Groq
    
    client = Groq(api_key=config.GROQ_API_KEY)
    response = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000
    )
    return response.choices[0].message.content

def _generate_with_gemini(prompt: str, config) -> str:
    """Generate script using Google Gemini"""
    import google.generativeai as genai
    
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel(config.GEMINI_MODEL)
    response = model.generate_content(prompt)
    return response.text
