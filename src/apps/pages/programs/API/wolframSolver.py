import requests
import streamlit as st

from src.helpers.checkKeyExist import isKeyExist
from src.helpers.displayInstructions import showInstructions

api_guide = """
### How to get your Wolfram Alpha API Key:
1. Visit [Wolfram Alpha](https://developer.wolframalpha.com/).
2. Sign up for a free account.
3. Generate an API key from your account dashboard.
4. Enter the API key in the input field.
"""

WOLFRAM_URL = "http://api.wolframalpha.com/v2/query"
WOLFRAM_API_KEY = st.secrets["api_key"]["WOLFRAM_API_KEY"]


def calculate_expression(query):
  params = {"input": query, "format": "image,plaintext", "output": "JSON", "appid": WOLFRAM_API_KEY}
  response = requests.get(WOLFRAM_URL, params=params)
  if response.status_code == 200:
    data = response.json()
    if "queryresult" in data and data["queryresult"]["success"]:
      pods = data["queryresult"]["pods"]
      return pods
    else:
      st.error("No results found for the given input!", icon="🚨")
      return None
  else:
    st.error("Error fetching data from Wolfram Alpha", icon="🚨")
    return None


def display_plots(pods):
  for pod in pods:
    if "img" in pod["subpods"][0]:
      image_url = pod["subpods"][0]["img"]["src"]
      st.image(image_url, caption=pod["title"], use_container_width=True)


def display_results(pods):
  if pods:
    for pod in pods:
      st.subheader(pod["title"])
      if "plaintext" in pod["subpods"][0] and pod["subpods"][0]["plaintext"]:
        st.text(pod["subpods"][0]["plaintext"])
    display_plots(pods)
  else:
    st.error("No results found for the given input!", icon="🚨")


def wolframSolver():
  exists = isKeyExist("WOLFRAM_API_KEY", "api_key")
  if not exists["WOLFRAM_API_KEY"]:
    showInstructions(markdown_text=api_guide, fields="WOLFRAM_API_KEY")
    st.stop()
  query = st.text_area("Enter a mathematical or scientific query (e.g., '5 + 5', 'integrate x^2 dx', 'solve x^2 + 5x = 0')")
  if st.button("Calculate"):
    if query:
      result_pods = calculate_expression(query)
      display_results(result_pods)
    else:
      st.error("Please enter a valid query!", icon="🚨")
