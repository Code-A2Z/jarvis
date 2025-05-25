import streamlit as st
import importlib
import random

from src.helpers.getModules import getModules
from src.helpers.getFolders import getFolders

icons = [
  ":material/api:",
  ":material/image:",
  ":material/image_search:",
  ":material/code:",
  ":material/extension:",
  ":material/rocket_launch:",
  ":material/casino:",
  ":material/school:",
  ":material/emoji_events:",
  ":material/smart_toy:",
  ":material/email:",
  ":material/web:",
  ":material/camera_alt:",
  ":material/assignment:",
  ":material/health_and_safety:",
  ":material/recommend:",
  ":material/share:",
]

def createPageModule(MAIN_DIR, MODULES):
  st.title(MAIN_DIR)
  choice = st.selectbox('Select a program to execute', [None] + list(MODULES.keys()), key=MAIN_DIR)
  st.divider()

  if choice in MODULES:
    module_name = MODULES[choice]
    try:
      module = importlib.import_module(f"src.apps.pages.programs.{MAIN_DIR}.{module_name}")
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

def structPages(path):
  folders = getFolders(path)
  pages = []
  for name, folder in folders.items():
    COMMON_MODULE_PATH = f"{path}/{folder}"
    MODULES = getModules(COMMON_MODULE_PATH)
    if MODULES:
      pages.append(
        st.Page(
          lambda folder=folder, MODULES=MODULES: createPageModule(folder, MODULES),
          title=name,
          icon=random.choice(icons),
          url_path=folder
        )
      )
  return pages
