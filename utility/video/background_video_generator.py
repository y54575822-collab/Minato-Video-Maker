"""Video background/B-roll generation module"""
import requests
from typing import List, Tuple
from utility.config import get_config

def generate_video_url(search_terms: List[Tuple], server: str = "pexel", orientation_landscape: bool = False) -> List:
    """Generate video URLs from search terms"""
    if server.lower() == "pexel":
        return _search_pexels(search_terms, orientation_landscape)
    else:
        raise ValueError(f"Unknown video server: {server}")

def _search_pexels(search_terms: List[Tuple], orientation_landscape: bool = False) -> List:
    """Search Pexels for video background"""
    config = get_config()
    api_key = config.PEXELS_API_KEY
    base_url = "https://api.pexels.com/videos/search"
    
    headers = {"Authorization": api_key}
    results = []
    
    for time_range, queries in search_terms:
        start_time, end_time = time_range
        query = queries[0] if queries else "background"
        
        params = {
            "query": query,
            "per_page": 1,
            "page": 1,
            "orientation": "landscape" if orientation_landscape else "portrait"
        }
        
        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('videos'):
                video_url = data['videos'][0]['video_files'][0]['link']
                results.append([
                    [start_time, end_time],
                    video_url
                ])
                print(f"Found video for '{query}': {video_url}")
            else:
                print(f"No video found for '{query}'")
        except Exception as e:
            print(f"Error searching Pexels for '{query}': {e}")
    
    return results
