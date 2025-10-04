import os

import requests
import streamlit as st

from src.helpers.checkKeyExist import isKeyExist
from src.helpers.displayInstructions import showInstructions

URL = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=PLPUts_2rBVRVTrLlcB54Hwi6Ws51UWLXU"
BLOG_URL = "https://avdhesh-portfolio.netlify.app/blog/fetch-youtube-playlist-in-reactjs"
api_guide = """
1. Go to the [Google Developers Console](https://console.developers.google.com/).
2. Create a new project or select an existing project.
3. In the left sidebar, click on 'Credentials'.
4. Click on 'Create Credentials' and select 'API key'.
5. Copy the generated API key and paste it in the text box below.
6. Click on 'Submit' to save the API key.
"""


def youtubePlaylistVideos(API_KEY):
  URL2 = f"{URL}&key={API_KEY}"
  response = requests.get(URL2)
  videos = response.json().get("items", [])
  return videos


def displayVideos(videos):
  filtered_videos = [video for video in videos if video["snippet"].get("title", "").lower() != "private video"]
  for i in range(0, len(filtered_videos), 2):
    cols = st.columns(2)
    for j in range(2):
      if i + j < len(filtered_videos):
        video = filtered_videos[i + j]
        video_title = video["snippet"]["title"].split("|")[0].strip()
        video_url = f"https://www.youtube.com/watch?v={video['snippet']['resourceId']['videoId']}"
        with cols[j]:
          st.markdown(f"##### [{video_title}]({video_url})")
          st.video(video_url)


def youtubePlaylist():
  st.title("🎬 YouTube Playlist")
  st.markdown(
    "Explore the latest videos from the Jarvis YouTube playlist. Watch tutorials, feature demonstrations, and more to get started with Jarvis."
  )
  exists = isKeyExist("YOUTUBE_API_KEY", "api_key")
  if not exists["YOUTUBE_API_KEY"]:
    showInstructions(markdown_text=api_guide, fields="YOUTUBE_API_KEY")
    st.info(f"You can also go through my [blog post]({BLOG_URL}) for a detailed guide on how to get the YouTube API key.", icon="📝")
    st.error("YouTube API key not found. Please add your API key to the secrets manager.", icon="🚨")
    st.stop()

  API_KEY = st.secrets["api_key"]["YOUTUBE_API_KEY"] or os.environ["YOUTUBE_API_KEY"]
  if st.button("Show Videos"):
    videos = youtubePlaylistVideos(API_KEY)
    displayVideos(videos)


youtubePlaylist()
