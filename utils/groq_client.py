import os, json, requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GroqClient:
    def __init__(self):
        """Initialize Groq client with API key from environment"""
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            st.error("GROQ_API_KEY not found in environment variables")
            raise ValueError("GROQ_API_KEY is required")
        
        self.model = os.getenv('GROQ_MODEL')
        self.api_url = os.getenv('GROQ_API_URL', 'https://api.groq.com/openai/v1/chat/completions')
                
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def _make_api_call(self, messages, temperature=0.3, max_tokens=4000):
        """Make a call to the Groq API"""
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API request failed with status {response.status_code}: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            st.error(f"Network error during API call: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Unexpected error during API call: {str(e)}")
            return None
        
    def generate_dietary_goals(self, age, sex, weight, height):      
        # Create prompt for LLM
        prompt = f"""
        Based on the following user profile, generate personalized daily dietary goals:
        
        User Profile:
        - Age: {age} years
        - Sex: {sex}
        - Weight: {weight} kg
        - Height: {height} cm
        
        Please provide daily intake recommendations for:
        1. Calories (considering moderate activity level, in kCal/day)
        2. Fiber (in grams/day)
        3. Protein (in grams/day)
        
        Format your response as a JSON object with the following structure:
        {{
            "explanation": "<brief explanation of the recommendations>",
            "calories": <number>,
            "fiber": <number>,
            "protein": <number>
        }}
        
        Consider standard nutritional guidelines and the user's specific profile.
        Limit your response to the block of JSON.
        """
        
        messages = [
            {
                "role": "system",
                "content": "You are a nutritionist AI that provides personalized dietary recommendations. Always respond with valid JSON format."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        response = self._make_api_call(messages)
        
        if response and 'choices' in response:
            return response['choices'][0]['message']['content']
        else:
            return None
            
    
    def generate_meal_recommendations(self, user_data, meal_preferences):
        """
        Generate meal recommendations based on user data and preferences
        """
        try:
            try:
                goals = json.loads(user_data.get('DIETARY_GOALS'))
                goals_str = f"""
                Calories: {goals['calories']} kCal/day ({round(goals['calories']/3)} kCal per meal)
                Fiber: {goals['fiber']} g/day ({round(goals['fiber']/3)} grams per meal)
                Protein: {goals['protein']} g/day ({round(goals['protein']/3)} grams per meal)
                """
            except:
                goals_str = user_data.get('DIETARY_GOALS')
                st.error(f"diet goals might be incorrectly parsed: {goals_str}")

            prompt = f"""
            Please generate 3 recipes, with the following constraints:
            - The client has the following dietary and preferences: {user_data.get('DIETARY_RESTRICTIONS', 'None')}
            - The client has given the following instructions for today: {meal_preferences}
            - Dietary Goals: {goals_str}
            
            Format your response as a JSON object with the following structure:
            {{
                "recipe 1" : {{
                    "title": "<the recipe's name>",
                    "instructions": "<instructions of the recipe>",
                    "time": "<estimated preparation time in minutes>",
                    "ingredients": [
                        "<ingredient 1 (with quantity)>",
                        "<ingredient 2 (with quantity)>",
                        etc.
                    ],
                    "calories": <number, estimated amount of calories>,
                    "fiber": <number, estimated amount of fiber>,
                    "protein": <number, estimated amount of protein>
                }},
                "recipe 2" : {{
                    follow the same structure as recipe 1
                }},
                "recipe 3" : {{
                    follow the same structure as recipe 1
                }}
            }}
    
            ---
    
            Here is an example:
            {{
                "recipe 1": {{
                    "title": "Classic Gazpacho",
                    "instructions": "1. Combine all ingredients in a blender.\n2. Blend until smooth.\n3. Strain the mixture through a fine-mesh sieve into a large bowl, pressing on the solids to extract as much liquid as possible.\n4. Discard the solids and chill the soup in the refrigerator for at least 2 hours.\n5. Serve cold, garnished with diced cucumber, bell pepper, and croutons if desired.",
                    "time": 20,
                    "ingredients": [
                        "1.5 kg tomatoes",
                        "1 cucumber",
                        "1 red bell pepper",
                        "1 small red onion",
                        "2 cloves garlic",
                        "500 ml tomato juice",
                        "120 ml extra-virgin olive oil",
                        "30 ml red wine vinegar",
                        "Salt and pepper"
                    ],
                    "calories": 500,
                    "fiber": 10,
                    "protein": 20
                }},
                "recipe 2": {{
                    "title": "Caprese Salad",
                    "instructions": "1. Slice the tomatoes and mozzarella into 1/4-inch thick slices.\n2. Arrange the tomato and mozzarella slices alternately on a platter.\n3. Drizzle with olive oil and balsamic glaze.\n4. Sprinkle with salt and pepper to taste.\n5. Garnish with fresh basil leaves.\n6. Serve immediately.",
                    "time": 15,
                    "ingredients": [
                        "4 large  tomatoes",
                        "250 g fresh mozzarella cheese",
                        "1/4 cup fresh basil leaves",
                        "2 tbsp extra-virgin olive oil",
                        "2 tbsp balsamic glaze",
                        "Salt and pepper"
                    ],
                    "calories": 450,
                    "fiber": 12,
                    "protein": 18
                }},
                "recipe 3": {{
                    "title": "Chicken Caesar Salad",
                    "instructions": "1. In a large bowl, combine the chopped romaine lettuce, grilled chicken breast, croutons, and shredded Parmesan cheese.\n2. In a small bowl, whisk together the Caesar dressing and lemon juice.\n3. Pour the dressing over the salad and toss to coat evenly.\n4. Season with salt and pepper to taste.\n5. Serve immediately.",
                    "time": 20,
                    "ingredients": [
                        "1 head romaine lettuce",
                        "2 chicken breasts",
                        "2 cups croutons",
                        "1/2 cup shredded Parmesan cheese",
                        "1/2 cup Caesar dressing",
                        "1 tbsp lemon juice",
                        "Salt and pepper"
                    ],
                    "calories": 520,
                    "fiber": 12,
                    "protein": 25
                }}
            }}
    
            ---
    
            Try to give varied recipes. Do not add styling, markdown or line breaks inside the instructions.
            The recipes need to be JSON-safe, this is important ! 
            
            """
            
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant for nutrition and cooking."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            response = self._make_api_call(messages, temperature=0.7, max_tokens=1500)

            if response and 'choices' in response:
                return response['choices'][0]['message']['content']
            else:
                return None
                
        except Exception as e:
            st.error(f"Error generating meal recommendations: {str(e)}")
            return None