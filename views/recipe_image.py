# recipe_image.py
import streamlit as st
import requests
from typing import Optional, Dict, List
import logging
from PIL import Image
import io
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecipeImageHandler:
    """
    Handle recipe image operations including fetching, caching, and displaying
    """
    
    def __init__(self, pexels_api_key: str):
        self.api_key = pexels_api_key
        self.base_url = "https://api.pexels.com/v1"
        self.headers = {"Authorization": pexels_api_key}
        
        # Initialize session state for image caching
        if "recipe_image_cache" not in st.session_state:
            st.session_state.recipe_image_cache = {}
        if "image_loading_states" not in st.session_state:
            st.session_state.image_loading_states = {}
    
    def get_recipe_image(self, recipe_name: str, size: str = "medium") -> Optional[Dict]:
        """
        Get static image only if recipe exists in predefined dummy list.
        """
        static_images = {
            "Pasta Carbonara": {
                "url": "https://images.pexels.com/photos/1279330/pexels-photo-1279330.jpeg",
                "alt": "Pasta Carbonara",
                "photographer": "Engin Akyurt",
                "photographer_url": "https://www.pexels.com/@enginakyurt",
                "pexels_url": "https://www.pexels.com/photo/pasta-on-white-ceramic-plate-1279330/"
            },
            "Grilled Chicken Salad": {
                "url": "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg",
                "alt": "Grilled Chicken Salad",
                "photographer": "Ella Olsson",
                "photographer_url": "https://www.pexels.com/@ella-olsson-572949",
                "pexels_url": "https://www.pexels.com/photo/vegetable-salad-on-white-ceramic-plate-1640777/"
            },
            "Avocado Toast": {
                "url": "https://images.pexels.com/photos/1640772/pexels-photo-1640772.jpeg",
                "alt": "Avocado Toast",
                "photographer": "Ella Olsson",
                "photographer_url": "https://www.pexels.com/@ella-olsson-572949",
                "pexels_url": "https://www.pexels.com/photo/avocado-toast-on-plate-1640772/"
            }
        }
    
        # Match case-insensitively
        normalized_title = recipe_name.strip().lower()
        static_lookup = {k.lower(): v for k, v in static_images.items()}
        result = static_lookup.get(normalized_title)
    
        if result:
            st.session_state.recipe_image_cache[f"{recipe_name}_{size}"] = result
            return result
        else:
            return None  # ❌ no fallback


    
    def _generate_search_terms(self, recipe_name: str) -> List[str]:
        """
        Generate search terms for better image results
        """
        # Remove common recipe words that don't help with image search
        stop_words = ["recipe", "easy", "quick", "best", "homemade", "delicious", "classic", "traditional"]
        
        # Clean the recipe name
        cleaned_name = recipe_name.lower()
        for word in stop_words:
            cleaned_name = cleaned_name.replace(word, "")
        
        # Generate search terms in order of preference
        search_terms = [
            f"{cleaned_name} food dish",
            f"{cleaned_name} recipe",
            f"{cleaned_name} cooking",
            cleaned_name.strip(),
            f"{recipe_name} food"
        ]
        
        # Remove empty terms
        return [term.strip() for term in search_terms if term.strip()]


    
    def _search_pexels(self, search_term: str, size: str) -> Optional[Dict]:
        """
        Search Pexels API for images
        """
        try:
            url = f"{self.base_url}/search"
            params = {
                "query": search_term,
                "per_page": 1,
                "orientation": "landscape"
            }

            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"🔍 Searching Pexels for: {search_term}")

            
            if data.get("photos") and len(data["photos"]) > 0:
                photo = data["photos"][0]
                
                # Select appropriate image size
                image_url = self._get_image_url_by_size(photo["src"], size)
                
                return {
                    "url": image_url,
                    "alt": photo.get("alt", search_term),
                    "photographer": photo["photographer"],
                    "photographer_url": photo["photographer_url"],
                    "pexels_url": photo["url"]
                }
            
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Pexels API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Error searching Pexels: {e}")
            return None
    
    def _get_image_url_by_size(self, src_dict: Dict, size: str) -> str:
        """
        Get image URL based on requested size
        """
        size_mapping = {
            "small": "small",
            "medium": "medium",
            "large": "large",
            "original": "original"
        }
        
        requested_size = size_mapping.get(size, "medium")
        return src_dict.get(requested_size, src_dict.get("medium"))
    
    def _get_placeholder_image(self, recipe_name: str, size: str) -> Dict:
        """
        Generate placeholder image data
        """
        # Different placeholder sizes
        size_dimensions = {
            "small": "200x150",
            "medium": "400x300",
            "large": "600x450",
            "original": "800x600"
        }
        
        dimensions = size_dimensions.get(size, "400x300")
        placeholder_url = f"https://via.placeholder.com/{dimensions}/f8f9fa/6c757d?text={recipe_name.replace(' ', '+')}"
        
        return {
            "url": placeholder_url,
            "alt": f"Placeholder for {recipe_name}",
            "photographer": "Placeholder",
            "photographer_url": "#",
            "pexels_url": "#"
        }
    
    def display_recipe_image(self, recipe_name: str, width: Optional[int] = None, 
                           show_attribution: bool = True, use_container_width: bool = False) -> None:
        """
        Display recipe image in Streamlit with loading state
        """
        # Set loading state
        if recipe_name not in st.session_state.image_loading_states:
            st.session_state.image_loading_states[recipe_name] = False
        
        # Create placeholder for loading
        image_placeholder = st.empty()
        
        if not st.session_state.image_loading_states[recipe_name]:
            with image_placeholder:
                with st.spinner(f"Loading image for {recipe_name}..."):
                    st.session_state.image_loading_states[recipe_name] = True
                    image_data = self.get_recipe_image(recipe_name)
        else:
            image_data = self.get_recipe_image(recipe_name)
        
        if image_data:
            with image_placeholder:
                # Display image
                st.image(
                    image_data["url"],
                    width=width,
                    use_container_width=use_container_width,
                    caption=image_data["alt"] if not show_attribution else None
                )
                
                # Show attribution if requested
                if show_attribution and image_data["photographer"] != "Placeholder":
                    st.caption(f"📷 Photo by [{image_data['photographer']}]({image_data['photographer_url']}) on [Pexels]({image_data['pexels_url']})")
        else:
            with image_placeholder:
                st.error("Failed to load image")
    
    def get_multiple_recipe_images(self, recipe_names: List[str], size: str = "medium") -> Dict[str, Dict]:
        """
        Get images for multiple recipes efficiently
        """
        images = {}
        
        # Show progress bar for multiple images
        if len(recipe_names) > 3:
            progress_bar = st.progress(0)
            
            for i, recipe_name in enumerate(recipe_names):
                images[recipe_name] = self.get_recipe_image(recipe_name, size)
                progress_bar.progress((i + 1) / len(recipe_names))
            
            progress_bar.empty()
        else:
            for recipe_name in recipe_names:
                images[recipe_name] = self.get_recipe_image(recipe_name, size)
        
        return images
    
    def preload_images(self, recipe_names: List[str], size: str = "medium") -> None:
        """
        Preload images for better performance
        """
        with st.spinner("Preloading recipe images..."):
            for recipe_name in recipe_names:
                self.get_recipe_image(recipe_name, size)
    
    def clear_image_cache(self) -> None:
        """
        Clear the image cache
        """
        st.session_state.recipe_image_cache = {}
        st.session_state.image_loading_states = {}
        st.success("Image cache cleared!")
    
    def get_cache_stats(self) -> Dict:
        """
        Get cache statistics
        """
        cache_size = len(st.session_state.recipe_image_cache)
        loading_states = len(st.session_state.image_loading_states)
        
        return {
            "cached_images": cache_size,
            "loading_states": loading_states
        }
    
    def display_image_gallery(self, recipe_images: Dict[str, Dict], columns: int = 3) -> None:
        """
        Display a gallery of recipe images
        """
        if not recipe_images:
            st.info("No images to display")
            return
        
        # Create columns
        cols = st.columns(columns)
        
        for i, (recipe_name, image_data) in enumerate(recipe_images.items()):
            with cols[i % columns]:
                if image_data:
                    st.image(
                        image_data["url"],
                        caption=recipe_name,
                        use_container_width=True
                    )
                    
                    if image_data["photographer"] != "Placeholder":
                        st.caption(f"📷 {image_data['photographer']}")
                else:
                    st.error(f"Failed to load image for {recipe_name}")

# Global instance with API key
@st.cache_resource
def get_recipe_image_handler():
    """
    Get cached recipe image handler instance
    """
    api_key = "gbwBoadwuaxrLle07GeL2O7bMObX660epgISPO5zRlaVEa3x7h9pVf5U"
    return RecipeImageHandler(api_key)

# Convenience functions
def display_recipe_image(recipe_name: str, width: Optional[int] = None, 
                        show_attribution: bool = True, use_container_width: bool = False) -> None:
    """
    Convenience function to display recipe image
    """
    handler = get_recipe_image_handler()
    handler.display_recipe_image(recipe_name, width, show_attribution, use_container_width)

def get_recipe_image_data(recipe_name: str, size: str = "medium") -> Optional[Dict]:
    """
    Convenience function to get recipe image data
    """
    handler = get_recipe_image_handler()
    return handler.get_recipe_image(recipe_name, size)

def preload_recipe_images(recipe_names: List[str], size: str = "medium") -> None:
    """
    Convenience function to preload recipe images
    """
    handler = get_recipe_image_handler()
    handler.preload_images(recipe_names, size)

def clear_recipe_image_cache() -> None:
    """
    Convenience function to clear image cache
    """
    handler = get_recipe_image_handler()
    handler.clear_image_cache()