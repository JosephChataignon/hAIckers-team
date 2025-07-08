import json
import urllib.request
import webbrowser
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import openai
import time

@dataclass
class Ingredient:
    name: str
    quantity: float
    alternatives: List[str] = None
    
    def __post_init__(self):
        if self.alternatives is None:
            self.alternatives = []

@dataclass
class CartItem:
    name: str
    quantity: int
    price: float
    store_id: str = None

class FoodPlatform(ABC):
    """Abstract base class for food delivery platforms"""
    
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.driver = None
        
    @abstractmethod
    def search_ingredients(self, ingredients: List[Ingredient]) -> List[CartItem]:
        """Search for ingredients on the platform"""
        pass
    
    @abstractmethod
    def add_to_cart(self, items: List[CartItem]) -> bool:
        """Add items to cart"""
        pass
    
    @abstractmethod
    def navigate_to_cart(self) -> str:
        """Navigate to cart and return cart URL"""
        pass
    
    def setup_driver(self):
        """Setup Selenium WebDriver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def close_driver(self):
        """Close WebDriver"""
        if self.driver:
            self.driver.quit()

class IFoodPlatform(FoodPlatform):
    """iFood platform implementation"""
    
    def __init__(self):
        super().__init__("iFood", "https://www.ifood.com.br")
        self.api_headers = {
            'Accept': 'application/json',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
            'secret_key': '9ef4fb4f-7a1d-4e0d-a9b1-9b82873297d8',
            'access_key': '69f181d5-0046-4221-b7b2-deef62bd60d5'
        }
        
    def search_ingredients(self, ingredients: List[Ingredient]) -> List[CartItem]:
        """Search for ingredients using iFood API"""
        found_items = []
        
        for ingredient in ingredients:
            # Search for supermarkets/grocery stores
            merchants = self._get_grocery_merchants()
            
            for merchant in merchants[:3]:  # Check top 3 merchants
                items = self._search_in_merchant(merchant['uuid'], ingredient.name)
                if items:
                    # Find best match
                    best_item = self._find_best_match(items, ingredient)
                    if best_item:
                        found_items.append(best_item)
                        break
                        
        return found_items
    
    def _get_grocery_merchants(self, latitude=-23.636890, longitude=-46.644978):
        """Get grocery merchants from iFood API"""
        url = f'https://marketplace.ifood.com.br/v1/merchants?latitude={latitude}&longitude={longitude}&page=0&channel=IFOOD&size=50&category=GROCERY'
        
        try:
            req = urllib.request.Request(url, headers=self.api_headers)
            response = urllib.request.urlopen(req).read()
            data = json.loads(response.decode('utf-8'))
            return data.get('merchants', [])
        except Exception as e:
            print(f"Error getting merchants: {e}")
            return []
    
    def _search_in_merchant(self, merchant_uuid: str, ingredient_name: str) -> List[dict]:
        """Search for ingredient in specific merchant"""
        url = f'https://wsloja.ifood.com.br/ifood-ws-v3/restaurants/{merchant_uuid}/menu'
        
        try:
            req = urllib.request.Request(url, headers=self.api_headers)
            response = urllib.request.urlopen(req).read()
            data = json.loads(response.decode('utf-8'))
            
            items = []
            menu = data.get('data', {}).get('menu', [])
            
            for category in menu:
                for item in category.get('items', []):
                    if ingredient_name.lower() in item.get('name', '').lower():
                        items.append(item)
                        
            return items
        except Exception as e:
            print(f"Error searching in merchant: {e}")
            return []
    
    def _find_best_match(self, items: List[dict], ingredient: Ingredient) -> CartItem:
        """Find best matching item for ingredient"""
        if not items:
            return None
            
        # Simple matching logic - can be enhanced with ML
        best_item = items[0]
        
        return CartItem(
            name=best_item.get('name', ''),
            quantity=1,  # Default quantity
            price=best_item.get('price', 0),
            store_id=best_item.get('merchantUuid', '')
        )
    
    def add_to_cart(self, items: List[CartItem]) -> bool:
        """Add items to cart using Selenium"""
        if not items:
            return False
            
        self.setup_driver()
        
        try:
            self.driver.get(self.base_url)
            
            # Use LLM to understand the page and add items
            success = self._add_items_with_llm(items)
            
            return success
            
        except Exception as e:
            print(f"Error adding to cart: {e}")
            return False
    
    def navigate_to_cart(self) -> str:
        """Navigate to cart"""
        try:
            cart_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='cart-button'], .cart-button, #cart"))
            )
            cart_button.click()
            
            time.sleep(2)
            return self.driver.current_url
            
        except TimeoutException:
            print("Cart button not found")
            return None
    
    def _add_items_with_llm(self, items: List[CartItem]) -> bool:
        """Use LLM to understand page structure and add items"""
        page_html = self.driver.page_source
        
        # Simplified LLM prompt - you'd need to implement actual LLM integration
        prompt = f"""
        You are a web automation assistant. Given this HTML page structure, 
        help me add these items to the cart: {[item.name for item in items]}
        
        Return CSS selectors for:
        1. Search box
        2. Add to cart buttons
        3. Cart navigation
        
        HTML snippet: {page_html[:2000]}...
        """
        
        # This would call your LLM service (OpenAI, etc.)
        # For now, using basic selectors
        selectors = {
            'search': 'input[placeholder*="search"], input[type="search"]',
            'add_to_cart': 'button[data-testid*="add"], .add-to-cart',
            'cart': '[data-testid="cart"], .cart-icon'
        }
        
        return self._execute_cart_actions(items, selectors)
    
    def _execute_cart_actions(self, items: List[CartItem], selectors: Dict[str, str]) -> bool:
        """Execute cart actions based on selectors"""
        try:
            for item in items:
                # Search for item
                search_box = self.driver.find_element(By.CSS_SELECTOR, selectors['search'])
                search_box.clear()
                search_box.send_keys(item.name)
                search_box.submit()
                
                time.sleep(3)
                
                # Add to cart
                add_buttons = self.driver.find_elements(By.CSS_SELECTOR, selectors['add_to_cart'])
                if add_buttons:
                    add_buttons[0].click()
                    time.sleep(2)
                    
            return True
            
        except Exception as e:
            print(f"Error executing cart actions: {e}")
            return False

class InstacartPlatform(FoodPlatform):
    """Instacart platform implementation"""
    
    def __init__(self):
        super().__init__("Instacart", "https://www.instacart.com")
    
    def search_ingredients(self, ingredients: List[Ingredient]) -> List[CartItem]:
        # Implementation for Instacart API/scraping
        return []
    
    def add_to_cart(self, items: List[CartItem]) -> bool:
        # Implementation for Instacart cart
        return False
    
    def navigate_to_cart(self) -> str:
        # Implementation for Instacart cart navigation
        return None

class DeliverooPerogram(FoodPlatform):
    """Deliveroo platform implementation"""
    
    def __init__(self):
        super().__init__("Deliveroo", "https://deliveroo.com")
    
    def search_ingredients(self, ingredients: List[Ingredient]) -> List[CartItem]:
        # Implementation for Deliveroo
        return []
    
    def add_to_cart(self, items: List[CartItem]) -> bool:
        # Implementation for Deliveroo cart
        return False
    
    def navigate_to_cart(self) -> str:
        # Implementation for Deliveroo cart navigation
        return None

class WoltPlatform(FoodPlatform):
    """Wolt platform implementation"""
    
    def __init__(self):
        super().__init__("Wolt", "https://wolt.com")
    
    def search_ingredients(self, ingredients: List[Ingredient]) -> List[CartItem]:
        # Implementation for Wolt
        return []
    
    def add_to_cart(self, items: List[CartItem]) -> bool:
        # Implementation for Wolt cart
        return False
    
    def navigate_to_cart(self) -> str:
        # Implementation for Wolt cart navigation
        return None

class MeituanPlatform(FoodPlatform):
    """Meituan platform implementation"""
    
    def __init__(self):
        super().__init__("Meituan", "https://www.meituan.com")
        self.api_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Type': 'application/json',
            'Referer': 'https://www.meituan.com'
        }
        self.session = requests.Session()
        self.session.headers.update(self.api_headers)
    
    def search_ingredients(self, ingredients: List[Ingredient]) -> List[CartItem]:
        """Search for ingredients using Meituan API"""
        found_items = []
        
        for ingredient in ingredients:
            # Get nearby supermarkets
            shops = self._get_nearby_supermarkets()
            
            for shop in shops[:3]:  # Check top 3 shops
                items = self._search_in_shop(shop['poi_id'], ingredient.name)
                if items:
                    best_item = self._find_best_match(items, ingredient)
                    if best_item:
                        found_items.append(best_item)
                        break
        
        return found_items
    
    def _get_nearby_supermarkets(self, latitude=39.9042, longitude=116.4074):
        """Get nearby supermarkets from Meituan API"""
        url = "https://apimobile.meituan.com/group/v1/deal/topic/recommend"
        
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'category_id': 20,  # Supermarket category
            'offset': 0,
            'limit': 20
        }
        
        try:
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('data', {}).get('deals', [])
        except Exception as e:
            print(f"Error getting Meituan supermarkets: {e}")
        
        return []
    
    def _search_in_shop(self, shop_id: str, ingredient_name: str) -> List[dict]:
        """Search for ingredient in specific Meituan shop"""
        url = f"https://apimobile.meituan.com/group/v1/deal/list/shop/{shop_id}"
        
        params = {
            'keyword': ingredient_name,
            'offset': 0,
            'limit': 20
        }
        
        try:
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
        except Exception as e:
            print(f"Error searching in Meituan shop: {e}")
        
        return []
    
    def _find_best_match(self, items: List[dict], ingredient: Ingredient) -> CartItem:
        """Find best matching item for ingredient"""
        if not items:
            return None
        
        best_item = items[0]
        
        return CartItem(
            name=best_item.get('title', ''),
            quantity=1,
            price=best_item.get('price', 0),
            store_id=best_item.get('deal_id', '')
        )
    
    def add_to_cart(self, items: List[CartItem]) -> bool:
        """Add items to cart on Meituan"""
        if not items:
            return False
        
        try:
            for item in items:
                cart_data = {
                    'deal_id': item.store_id,
                    'count': item.quantity,
                    'sku_id': ''
                }
                
                response = self.session.post(
                    'https://apimobile.meituan.com/group/v1/cart/add',
                    json=cart_data
                )
                
                if response.status_code != 200:
                    print(f"Failed to add {item.name} to Meituan cart")
                    return False
            
            return True
        except Exception as e:
            print(f"Error adding to Meituan cart: {e}")
            return False
    
    def navigate_to_cart(self) -> str:
        """Navigate to cart on Meituan"""
        return "https://www.meituan.com/cart"

class JustEatTakeawayPlatform(FoodPlatform):
    """Just Eat Takeaway platform implementation"""
    
    def __init__(self):
        super().__init__("Just Eat Takeaway", "https://www.just-eat.com")
        self.api_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-GB,en;q=0.9',
            'Content-Type': 'application/json',
            'x-je-platform': 'web'
        }
        self.session = requests.Session()
        self.session.headers.update(self.api_headers)
    
    def search_ingredients(self, ingredients: List[Ingredient]) -> List[CartItem]:
        """Search for ingredients using Just Eat Takeaway API"""
        found_items = []
        
        for ingredient in ingredients:
            # Get grocery stores
            stores = self._get_grocery_stores()
            
            for store in stores[:3]:  # Check top 3 stores
                items = self._search_in_store(store['id'], ingredient.name)
                if items:
                    best_item = self._find_best_match(items, ingredient)
                    if best_item:
                        found_items.append(best_item)
                        break
        
        return found_items
    
    def _get_grocery_stores(self, postcode="SW1A 1AA"):
        """Get grocery stores from Just Eat Takeaway API"""
        url = "https://uk.api.just-eat.io/restaurants"
        
        params = {
            'q': postcode,
            'cuisines': 'grocery',
            'limit': 20
        }
        
        try:
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('restaurants', [])
        except Exception as e:
            print(f"Error getting Just Eat stores: {e}")
        
        return []
    
    def _search_in_store(self, store_id: str, ingredient_name: str) -> List[dict]:
        """Search for ingredient in specific Just Eat store"""
        url = f"https://uk.api.just-eat.io/restaurants/{store_id}/menu"
        
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                data = response.json()
                items = []
                
                for category in data.get('menu', {}).get('categories', []):
                    for product in category.get('products', []):
                        if ingredient_name.lower() in product.get('name', '').lower():
                            items.append(product)
                
                return items
        except Exception as e:
            print(f"Error searching in Just Eat store: {e}")
        
        return []
    
    def _find_best_match(self, items: List[dict], ingredient: Ingredient) -> CartItem:
        """Find best matching item for ingredient"""
        if not items:
            return None
        
        best_item = items[0]
        
        return CartItem(
            name=best_item.get('name', ''),
            quantity=1,
            price=best_item.get('price', 0),
            store_id=best_item.get('id', '')
        )
    
    def add_to_cart(self, items: List[CartItem]) -> bool:
        """Add items to cart on Just Eat Takeaway"""
        if not items:
            return False
        
        try:
            for item in items:
                cart_data = {
                    'productId': item.store_id,
                    'quantity': item.quantity,
                    'notes': ''
                }
                
                response = self.session.post(
                    'https://uk.api.just-eat.io/basket/add',
                    json=cart_data
                )
                
                if response.status_code not in [200, 201]:
                    print(f"Failed to add {item.name} to Just Eat cart")
                    return False
            
            return True
        except Exception as e:
            print(f"Error adding to Just Eat cart: {e}")
            return False
    
    def navigate_to_cart(self) -> str:
        """Navigate to cart on Just Eat Takeaway"""
        return "https://www.just-eat.com/basket"


class FoodOrderingSystem:
    """Main food ordering system"""
    
    def __init__(self):
        self.platforms = {
            'ifood': IFoodPlatform(),
            'instacart': InstacartPlatform(),
            'deliveroo': DeliverooPerogram(),
            'wolt': WoltPlatform(),
            'meituan': MeituanPlatform(),
            'deliveryhero': DeliveryHeroPlatform(),
            'justeat': JustEatTakeawayPlatform()
        }
        
    def process_order(self, ingredients: List[Ingredient]) -> str:
        """Process complete order flow"""
        
        # Display ingredients
        print("\n📋 Ingredients to order:")
        for i, ingredient in enumerate(ingredients, 1):
            print(f"{i}. {ingredient.name}: {ingredient.quantity}g")
        
        # Choose platform
        platform = self._choose_platform()
        
        if not platform:
            return "Order cancelled"
        
        # Search for ingredients
        print(f"\n🔍 Searching for ingredients on {platform.name}...")
        found_items = platform.search_ingredients(ingredients)
        
        if not found_items:
            print("❌ No ingredients found on this platform")
            return "No ingredients found"
        
        # Display found items
        print(f"\n✅ Found {len(found_items)} items:")
        total_price = 0
        for item in found_items:
            print(f"- {item.name}: ${item.price:.2f}")
            total_price += item.price
        
        print(f"\n💰 Total: ${total_price:.2f}")
        
        # Confirm order
        confirm = input("\n❓ Add these items to cart? (y/n): ").lower()
        if confirm != 'y':
            return "Order cancelled"
        
        # Add to cart
        print(f"\n🛒 Adding items to cart on {platform.name}...")
        success = platform.add_to_cart(found_items)
        
        if not success:
            print("❌ Failed to add items to cart")
            return "Failed to add to cart"
        
        # Navigate to cart
        print("\n Navigating to cart...")
        cart_url = platform.navigate_to_cart()
        
        if cart_url:
            print(f"✅ Cart URL: {cart_url}")
            print("🌐 Opening cart in browser...")
            webbrowser.open(cart_url)
            return f"Order processed successfully. Cart: {cart_url}"
        else:
            print("❌ Could not navigate to cart")
            return "Could not navigate to cart"
    
    def _choose_platform(self) -> Optional[FoodPlatform]:
        """Let user choose platform"""
        st.markdown("\n🚀 Available platforms:")
        platforms_list = list(self.platforms.keys())
        
        for i, platform in enumerate(platforms_list, 1):
            st.markdown(f"{i}. {platform.capitalize()}")
        
        st.error(f"{len(platforms_list) + 1}. Custom platform (specify URL)")
        
        try:
            choice = int(input("\nChoose platform (number): "))
            
            if 1 <= choice <= len(platforms_list):
                return self.platforms[platforms_list[choice - 1]]
            elif choice == len(platforms_list) + 1:
                return self._create_custom_platform()
            else:
                st.error("Invalid choice")
                return None
                
        except ValueError:
            print("Invalid input")
            return None
    
    def _create_custom_platform(self) -> Optional[CustomPlatform]:
        """Create custom platform"""
        name = input("Enter platform name: ").strip()
        url = input("Enter platform URL: ").strip()
        
        if not name or not url:
            print("Invalid name or URL")
            return None
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        return CustomPlatform(name, url)


# Helper functions
def create_ingredient(name: str, quantity: float, alternatives: List[str] = None) -> Ingredient:
    """Create an ingredient object"""
    return Ingredient(name, quantity, alternatives or [])

def create_recipe_ingredients(recipe_dict: Dict[str, float]) -> List[Ingredient]:
    """Create ingredient list from recipe dictionary"""
    return [create_ingredient(name, quantity) for name, quantity in recipe_dict.items()]

