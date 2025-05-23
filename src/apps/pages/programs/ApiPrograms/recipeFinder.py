import streamlit as st
import requests
import os

from src.helpers.displayInstructions import showInstructions
from src.helpers.checkKeyExist import isKeyExist

api_guide = """
### How to get your API Key:
1. Visit [Spoonacular API](https://spoonacular.com/food-api).
2. Sign up for a free account.
3. Generate an API key from your account dashboard.
4. Enter the API key in the input field.
"""

def fetchRecipes(query):
  api_key = (os.environ.get("SPOONACULAR_API_KEY", "") or st.secrets['api_key']["SPOONACULAR_API_KEY"])
  api_url = f"https://api.spoonacular.com/recipes/complexSearch?query={query}&apiKey={api_key}"
  response = requests.get(api_url)
  return response.json()

def recipeFinder():
  exists = isKeyExist("SPOONACULAR_API_KEY", "api_key")
  if not exists["SPOONACULAR_API_KEY"]:
    showInstructions(markdown_text=api_guide, fields="SPOONACULAR_API_KEY")
    st.stop()

  query = st.text_input("Ingredients or a dish name, you name it!", placeholder="Mango, Apple, Chocolate cake, etc.")
  if st.button("Find Recipes") and query:
    recipes_data = fetchRecipes(query)
    if recipes_data['totalResults'] > 0:
      recipes = recipes_data['results']
      for recipe in recipes:
        st.divider()
        recipe_url = f"https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-').lower()}-{recipe['id']}"
        col1, col2 = st.columns([2, 1])
        with col1:
          st.image(recipe['image'])
        with col2:
          st.markdown(f"#### {recipe['title']}")
          st.markdown(f"[View Recipe]({recipe_url})")
