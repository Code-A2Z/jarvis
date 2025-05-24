import os
import importlib
import streamlit as st
from src.helpers.getModules import getModules

MAIN_DIR = 'UtilityModels'
BASE_DIR = os.path.dirname(__file__)
COMMON_MODULE_PATH = os.path.join(BASE_DIR, MAIN_DIR)
MODULES = getModules(COMMON_MODULE_PATH)

def UtilityModels():
  st.title('Utility Models')
  choice = st.selectbox('Select a model to execute', [None] + list(MODULES.keys()))
  st.divider()

  if choice in MODULES:
    module_name = MODULES[choice]
    try:
      module = importlib.import_module(f"src.apps.pages.models.{MAIN_DIR}.{module_name}")
      func = getattr(module, module_name)
      func()
    except ModuleNotFoundError as e:
      st.toast(f"Module '{module_name}.py' could not be found.", icon="🚫")
      st.error(f"An error occurred: {e}", icon="🚫")
    except AttributeError as e:
      st.toast(f"Function '{module_name}' could not be found in '{module_name}.py'.", icon="🚫")
      st.error(f"An error occurred: {e}", icon="🚫")
    except Exception as e:
      st.error(f"An error occurred: {e}", icon="🚫")
  else:
    st.info("Star this project on [GitHub](https://github.com/Code-A2Z/jarvis), if you like it!", icon='⭐')

UtilityModels()
