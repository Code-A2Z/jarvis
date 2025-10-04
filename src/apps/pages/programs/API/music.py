import os

import spotipy
import streamlit as st
from spotipy.oauth2 import SpotifyClientCredentials

from src.helpers.checkKeyExist import isKeyExist
from src.helpers.displayInstructions import showInstructions

api_guide = """
### How to get your Spotify Client ID and Secret:
1. Visit [Spotify Developers](https://developer.spotify.com/).
2. Sign up for a free account.
3. Go to the Dashboard and create a new App.
4. Copy the Client ID and Client Secret from the app's settings.
5. Enter the Client ID and Client Secret in the input fields below.
"""


def authenticateSpotify():
  client_id = os.environ.get("SPOTIFY_CLIENT_ID") or st.secrets["spotify"]["SPOTIFY_CLIENT_ID"]
  client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET") or st.secrets["spotify"]["SPOTIFY_CLIENT_SECRET"]

  if client_id and client_secret:
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp
  return None


def fetchMusicData(sp, search_query, search_type, limits):
  if search_type == "track":
    results = sp.search(q=search_query, type="track", limit=limits)
    return results["tracks"]["items"]
  elif search_type == "artist":
    results = sp.search(q=search_query, type="artist", limit=limits)
    return results["artists"]["items"]
  elif search_type == "album":
    results = sp.search(q=search_query, type="album", limit=limits)
    return results["albums"]["items"]


def displayResults(results, search_type):
  if search_type == "track":
    for track in results:
      col1, col2 = st.columns(2)
      with col1:
        st.image(track["album"]["images"][0]["url"], caption=track["name"])
      with col2, st.expander("Track Details", expanded=True):
        st.markdown(f"##### Artist: {track['artists'][0]['name']}")
        st.markdown(f"##### Album: {track['album']['name']}")
        st.markdown(f"##### Release Date: {track['album']['release_date']}")
      st.divider()
  elif search_type == "album":
    for album in results:
      col1, col2 = st.columns(2)
      with col1:
        st.image(album["images"][0]["url"], caption=album["name"])
      with col2, st.expander("Album Details", expanded=True):
        st.markdown(f"##### Artist: {album['artists'][0]['name']}")
        st.markdown(f"##### Release Date: {album['release_date']}")
      st.divider()
  elif search_type == "artist":
    for artist in results:
      col1, col2 = st.columns(2)
      with col1:
        st.image(artist["images"][0]["url"], caption=artist["name"])
      with col2, st.expander("Artist Details", expanded=True):
        st.markdown(f"##### Followers: {artist['followers']['total']}")
        st.markdown(f"##### Genres: {', '.join(artist['genres'])}")
      st.divider()


def music():
  exists = isKeyExist(["SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET"], "spotify")
  if not exists["SPOTIFY_CLIENT_ID"] or not exists["SPOTIFY_CLIENT_SECRET"]:
    showInstructions(markdown_text=api_guide, fields=["SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET"])
    st.stop()

  sp = authenticateSpotify()
  if sp is None:
    st.error("Invalid Spotify Client ID or Secret. Please try again.", icon="🚨")
    st.stop()

  col1, col2 = st.columns(2)
  with col1:
    search_query = st.text_input("Enter artist, album, or track name", placeholder="Type here...")
  with col2:
    search_type = st.selectbox("Select search type", ["track", "album", "artist"])
  limits = st.slider("Select number of results", min_value=1, max_value=50, value=10)
  if st.button("Search") and search_query:
    with st.spinner("Getting results..."):
      results = fetchMusicData(sp, search_query, search_type, limits)
      displayResults(results, search_type)
