# pexels_api.py

import requests
import streamlit as st
from typing import Optional, Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PexelsImageSearch:
    
    # A class to handle Pexels API image search for recipe images
    
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.pexels.com/v1"
        self.headers = {
            "Authorization": api_key
        }
    
    def search_recipe_image(self, recipe_name: str, per_page: int = 1) -> Optional[Dict]:
        try:
            search_query = self._clean_recipe_name(recipe_name)
    
            # 👇 REMOVE excessive terms here
            params = {
                "query": search_query,
                "per_page": per_page,
                "orientation": "landscape"
            }
    
            url = f"{self.base_url}/search"
    
            # 👇 Log actual query being sent
            logger.info(f"[PEXELS] Searching for: {params['query']}")
    
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("photos"):
                photo = data["photos"][0]
                return {
                    "url": photo["src"]["medium"],
                    "alt": photo.get("alt", recipe_name),
                    "photographer": photo["photographer"],
                    "photographer_url": photo["photographer_url"]
                }
    
            # If no results, fallback to uncleaned
            return self._fallback_search(recipe_name)
    
        except Exception as e:
            logger.error(f"Image search error: {e}")
            return None

    

    
    def _clean_recipe_name(self, recipe_name: str) -> str:
        cleaned = recipe_name.lower()
        cleaned = re.sub(r'[^a-zA-Z ]', '', cleaned)  # Remove symbols/numbers
        cleaned = re.sub(r'\b(recipe|easy|quick|homemade|best|delicious)\b', '', cleaned)
        cleaned = " ".join(cleaned.split())
        return cleaned

    
    def _fallback_search(self, recipe_name: str) -> Optional[Dict]:
        """
        Fallback search with just the recipe name
        """
        try:
            url = f"{self.base_url}/search"
            params = {
                "query": recipe_name,
                "per_page": 1,
                "orientation": "landscape"
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("photos") and len(data["photos"]) > 0:
                photo = data["photos"][0]
                return {
                    "url": photo["src"]["medium"],
                    "alt": photo.get("alt", recipe_name),
                    "photographer": photo["photographer"],
                    "photographer_url": photo["photographer_url"]
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Fallback search failed: {e}")
            return None
    
    def get_food_category_image(self, category: str) -> Optional[Dict]:
        """
        Get an image for a food category (e.g., "breakfast", "dinner", "dessert")
        """
        try:
            url = f"{self.base_url}/search"
            params = {
                "query": f"{category} food",
                "per_page": 1,
                "orientation": "landscape"
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("photos") and len(data["photos"]) > 0:
                photo = data["photos"][0]
                return {
                    "url": photo["src"]["medium"],
                    "alt": f"{category} food",
                    "photographer": photo["photographer"],
                    "photographer_url": photo["photographer_url"]
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting category image: {e}")
            return None

# Cache the API instance
@st.cache_resource
def get_pexels_api():
    """
    Get cached Pexels API instance
    """
    api_key = "gbwBoadwuaxrLle07GeL2O7bMObX660epgISPO5zRlaVEa3x7h9pVf5U"
    return PexelsImageSearch(api_key)

# Legacy function - use recipe_image.py for new implementations
def display_recipe_image(recipe_name: str, width: int = 300) -> None:
    """
    Display recipe image in Streamlit (Legacy - use recipe_image.py)
    
    Args:
        recipe_name (str): Name of the recipe
        width (int): Image width in pixels
    """
    # Import here to avoid circular imports
    from .recipe_image import display_recipe_image as new_display_recipe_image
    new_display_recipe_image(recipe_name, width=width)