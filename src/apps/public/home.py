import streamlit as st

def home():
  st.title("Welcome to Jarvis - Your Virtual AI Assistant!")
  st.toast("Welcome to Jarvis!", icon="👋")
  st.image('assets/image.gif', caption='Empower Your Digital Life with Jarvis', width=600)

  st.markdown("""
  ## Key Features
  - **Voice Commands**: Control your computer effortlessly using voice commands.
  - **Web Automation**: Open websites, search the internet, and get instant results.
  - **Media Control**: Play your favorite music and videos with a single command.
  - **Productivity Tools**: Open code editors, manage your time, and stay organized.
  - **Information Retrieval**: Get instant answers from Wikipedia and other sources.
  - **Email Management**: Send and receive emails directly from the assistant.
  """)

  with st.expander("## See Jarvis in Action"):
    try:
      video_id = st.secrets["general"]["YOUTUBE_VIDEO_ID"]
      st.video(f'https://www.youtube.com/watch?v={video_id}', start_time=0)
    except (KeyError, FileNotFoundError):
      st.info("Video demonstration will be available when configured.")
      st.markdown("Check out the [YouTube Playlist](https://www.youtube.com/playlist?list=PLPUts_2rBVRVTrLlcB54Hwi6Ws51UWLXU) for tutorials.")

  st.markdown("""
  ## Learn More and Get Started
  Explore the capabilities of Jarvis by diving into the following resources:
  - [Documentation](https://codingblogs.hashnode.dev/) - Comprehensive guides on setting up and using Jarvis.
  - [Community Forums](https://discord.gg/tSqtvHUJzE) - Join discussions with other Jarvis users.
  - [GitHub Repository](https://github.com/Code-A2Z/Jarvis) - Contribute to the development or get the latest version.
  - [YouTube Playlist](https://www.youtube.com/playlist?list=PLPUts_2rBVRVTrLlcB54Hwi6Ws51UWLXU) - Watch tutorials and feature demonstrations.
  """)

  st.markdown("""
  ---
  **Jarvis** is continually evolving with new features and improvements. Stay tuned for updates and feel free to contribute to its development.
  """)

home()
