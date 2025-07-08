
Recipie_Managr.py

import streamlit as st
from typing import Dict, List, Optional
import json
from .recipe_image import get_recipe_image_handler, display_recipe_image
import logging

logger = logging.getLogger(__name__)

class RecipeManager:
    """
    Enhanced recipe manager with image support
    """
    
    def __init__(self):
        self.image_handler = get_recipe_image_handler()
        
    def display_recipe_card(self, recipe: Dict, show_ingredients: bool = True) -> None:
        """
        Display a recipe card with image, ingredients, and order button
        
        Args:
            recipe (Dict): Recipe data
            show_ingredients (bool): Whether to show ingredients list
        """
        recipe_name = recipe.get("name", "Unknown Recipe")
        
        # Create columns for layout
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Display recipe image with better handling
            display_recipe_image(recipe_name, width=250, show_attribution=True)
            
        with col2:
            # Recipe title
            st.subheader(recipe_name)
            
            # Recipe details
            if "prep_time" in recipe:
                st.write(f"⏱️ **Prep Time:** {recipe['prep_time']}")
            if "cook_time" in recipe:
                st.write(f"🔥 **Cook Time:** {recipe['cook_time']}")
            if "servings" in recipe:
                st.write(f"👥 **Servings:** {recipe['servings']}")
            if "difficulty" in recipe:
                st.write(f"📊 **Difficulty:** {recipe['difficulty']}")
            
            # Description
            if "description" in recipe:
                st.write(recipe["description"])
        
        # Ingredients section
        if show_ingredients and "ingredients" in recipe:
            st.subheader("🛒 Ingredients")
            
            # Create columns for ingredients and order button
            ing_col1, ing_col2 = st.columns([3, 1])
            
            with ing_col1:
                self._display_ingredients_list(recipe["ingredients"])
            
            with ing_col2:
                # Order ingredients button
                if st.button(f"🛒 Order Ingredients", key=f"order_{recipe_name}", type="primary"):
                    self._handle_ingredient_order(recipe)
        
        # Instructions section
        if "instructions" in recipe:
            st.subheader("👨‍🍳 Instructions")
            for i, instruction in enumerate(recipe["instructions"], 1):
                st.write(f"{i}. {instruction}")
        
        st.divider()
    
    def _display_ingredients_list(self, ingredients: List[str]) -> None:
        """
        Display ingredients list with checkboxes
        """
        for ingredient in ingredients:
            st.checkbox(ingredient, key=f"ingredient_{ingredient}")
    
    def _handle_ingredient_order(self, recipe: Dict) -> None:
        """
        Handle ingredient ordering
        """
        recipe_name = recipe.get("name", "Unknown Recipe")
        ingredients = recipe.get("ingredients", [])
        
        if not ingredients:
            st.warning("No ingredients found for this recipe!")
            return
        
        # Store order in session state
        if "ingredient_orders" not in st.session_state:
            st.session_state.ingredient_orders = []
        
        order = {
            "recipe_name": recipe_name,
            "ingredients": ingredients,
            "timestamp": str(st.session_state.get("current_time", "now"))
        }
        
        st.session_state.ingredient_orders.append(order)
        
        # Success message
        st.success(f"✅ Ingredients for '{recipe_name}' added to your order!")
        
        # Show order summary
        with st.expander("Order Summary", expanded=True):
            st.write(f"**Recipe:** {recipe_name}")
            st.write("**Ingredients:**")
            for ingredient in ingredients:
                st.write(f"• {ingredient}")
            
            # Simulate order processing
            st.info("🚚 Your ingredients will be delivered within 2-3 hours!")
    
    def display_recipe_gallery(self, recipes: List[Dict], columns: int = 3) -> None:
        """
        Display recipes in a gallery layout
        
        Args:
            recipes (List[Dict]): List of recipes
            columns (int): Number of columns in gallery
        """
        if not recipes:
            st.info("No recipes found!")
            return
        
        # Create columns
        cols = st.columns(columns)
        
        for i, recipe in enumerate(recipes):
            with cols[i % columns]:
                self._display_recipe_thumbnail(recipe)
    
    def _display_recipe_thumbnail(self, recipe: Dict) -> None:
        """
        Display recipe thumbnail card
        """
        recipe_name = recipe.get("name", "Unknown Recipe")
        
        with st.container():
            # Recipe image with container width
            display_recipe_image(recipe_name, use_container_width=True, show_attribution=False)
            
            # Recipe info
            st.write(f"**{recipe_name}**")
            
            if "prep_time" in recipe:
                st.write(f"⏱️ {recipe['prep_time']}")
            
            if "difficulty" in recipe:
                st.write(f"📊 {recipe['difficulty']}")
            
            # View recipe button
            if st.button("View Recipe", key=f"view_{recipe_name}"):
                st.session_state.selected_recipe = recipe
                st.rerun()
    
    def get_shopping_list(self) -> List[str]:
        """
        Get combined shopping list from all orders
        """
        if "ingredient_orders" not in st.session_state:
            return []
        
        all_ingredients = []
        for order in st.session_state.ingredient_orders:
            all_ingredients.extend(order["ingredients"])
        
        # Remove duplicates while preserving order
        unique_ingredients = []
        seen = set()
        for ingredient in all_ingredients:
            if ingredient not in seen:
                unique_ingredients.append(ingredient)
                seen.add(ingredient)
        
        return unique_ingredients
    
    def display_shopping_list(self) -> None:
        """
        Display the current shopping list
        """
        shopping_list = self.get_shopping_list()
        
        if not shopping_list:
            st.info("Your shopping list is empty. Add some recipes to get started!")
            return
        
        st.subheader("🛒 Your Shopping List")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            for ingredient in shopping_list:
                st.checkbox(ingredient, key=f"shop_{ingredient}")
        
        with col2:
            if st.button("Clear List", type="secondary"):
                st.session_state.ingredient_orders = []
                st.rerun()
            
            if st.button("Place Order", type="primary"):
                st.success("🎉 Order placed successfully!")
                st.balloons()
                # Clear the list after ordering
                st.session_state.ingredient_orders = []
    
    def search_recipes(self, query: str, recipes: List[Dict]) -> List[Dict]:
        """
        Search recipes by name or ingredients
        
        Args:
            query (str): Search query
            recipes (List[Dict]): List of recipes to search in
            
        Returns:
            List[Dict]: Filtered recipes
        """
        if not query:
            return recipes
        
        query = query.lower()
        filtered_recipes = []
        
        for recipe in recipes:
            # Search in recipe name
            if query in recipe.get("name", "").lower():
                filtered_recipes.append(recipe)
                continue
            
            # Search in ingredients
            ingredients = recipe.get("ingredients", [])
            if any(query in ingredient.lower() for ingredient in ingredients):
                filtered_recipes.append(recipe)
                continue
            
            # Search in description
            description = recipe.get("description", "")
            if query in description.lower():
                filtered_recipes.append(recipe)
        
        return filtered_recipes
    
    def get_recipe_categories(self, recipes: List[Dict]) -> List[str]:
        """
        Get unique categories from recipes
        """
        categories = set()
        for recipe in recipes:
            if "category" in recipe:
                categories.add(recipe["category"])
        return sorted(list(categories))
    
    def filter_by_category(self, category: str, recipes: List[Dict]) -> List[Dict]:
        """
        Filter recipes by category
        """
        if not category or category == "All":
            return recipes
        
        return [recipe for recipe in recipes if recipe.get("category") == category]

# Global instance
recipe_manager = RecipeManager()