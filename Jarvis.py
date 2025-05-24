import streamlit as st

# /auth
auth_page = st.Page("src/auth/auth.py", title="Authentication", icon=":material/lock_open:")
env_page = st.Page("src/auth/env.py", title="Environment Variables", icon=":material/settings_input_component:")

# /apps/public
home = st.Page("src/apps/public/home.py", title="Home", icon=":material/home:")
youtubePlaylist = st.Page("src/apps/public/youtubePlaylist.py", title="Jarvis Videos", icon=":material/ondemand_video:")

MAIN_DIR = "src/apps/pages"

# /programs
api = st.Page(f"{MAIN_DIR}/programs/apiProgram.py", title="API", icon=":material/api:")
image = st.Page(f"{MAIN_DIR}/programs/imageProgram.py", title="Image", icon=":material/image:")
study = st.Page(f"{MAIN_DIR}/programs/studyProgram.py", title="Study", icon=":material/school:")
utility = st.Page(f"{MAIN_DIR}/programs/simpleProgram.py", title="Utility", icon=":material/extension:")
games = st.Page(f"{MAIN_DIR}/programs/games.py",title="Games",icon=":material/casino:")

# /models
chatBotModels = st.Page(f"{MAIN_DIR}/models/chatBotModel.py", title="Chat Bot Models", icon=":material/smart_toy:")
healthCareModels = st.Page(f"{MAIN_DIR}/models/healthCareModel.py", title="Health Care Models", icon=":material/health_and_safety:")
recommendationModels = st.Page(f"{MAIN_DIR}/models/recommendationModel.py", title="Recommendation Models", icon=":material/recommend:")
objectDetectionModels = st.Page(f"{MAIN_DIR}/models/objectDetectionModel.py", title="Object Detection Models", icon=":material/camera_alt:")

# /automations
messenger = st.Page(f"{MAIN_DIR}/automations/messenger.py", title="Messenger", icon=":material/email:")
socialMediaApps = st.Page(f"{MAIN_DIR}/automations/socialMediaApps.py", title="Social Media Apps", icon=":material/share:")
websites = st.Page(f"{MAIN_DIR}/automations/website.py", title="Websites", icon=":material/web:")
coding = st.Page(f"{MAIN_DIR}/automations/coding.py", title="Coding Platforms", icon=":material/code:")

def application():
  pages = {
    "": [
      home,
      youtubePlaylist,
    ],
    "Account": [
      auth_page,
    ],
  }

  if st.user and st.user.is_logged_in:
    pages.update({
      "Programs": [
        api,
        image,
        study,
        utility,
        games,
      ],
      "Models": [
        chatBotModels,
        healthCareModels,
        recommendationModels,
        objectDetectionModels,
      ],
      "Automations": [
        messenger,
        socialMediaApps,
        websites,
        coding,
      ],
      "Jarvis Credentials": [
        env_page,
      ],
    })

  return st.navigation(pages)

application().run()
