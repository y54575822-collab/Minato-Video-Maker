"""Video search query generator"""
import re
from typing import List, Tuple, Dict
from utility.config import get_config

def getVideoSearchQueriesTimed(script: str, timed_captions: List[Dict]) -> List[Tuple]:
    """Generate search queries for each caption segment"""
    search_queries = []
    
    for caption in timed_captions:
        start = caption['start']
        end = caption['end']
        text = caption['text']
        
        # Extract key nouns and important words
        queries = _extract_keywords(text)
        search_queries.append(((start, end), queries))
    
    return search_queries

def _extract_keywords(text: str) -> List[str]:
    """Extract relevant keywords from text"""
    # Remove common words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
    }
    
    # Split and clean
    words = text.lower().split()
    keywords = []
    
    for word in words:
        # Remove punctuation
        clean_word = re.sub(r'[^\w\s]', '', word)
        if clean_word and clean_word not in stop_words and len(clean_word) > 2:
            keywords.append(clean_word)
    
    # If no keywords, use first few words
    if not keywords:
        keywords = [w for w in text.split()[:3] if w.lower() not in stop_words]
    
    return keywords[:3]  # Return top 3 keywords

def merge_empty_intervals(video_urls: List) -> List:
    """Merge empty intervals and clean up video list"""
    if not video_urls:
        return []
    
    # Remove duplicates and sort by start time
    unique_videos = {}
    for time_range, url in video_urls:
        key = (time_range[0], time_range[1])
        if key not in unique_videos:
            unique_videos[key] = url
    
    # Convert back to list format
    result = [[[k[0], k[1]], v] for k, v in sorted(unique_videos.items())]
    return result
