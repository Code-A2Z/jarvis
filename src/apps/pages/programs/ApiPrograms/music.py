import streamlit as st
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from src.helpers.displayInstructions import showInstructions
from src.helpers.checkKeyExist import isKeyExist

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

def fetchMusicData(sp, search_query, search_type):
  if search_type == 'track':
    results = sp.search(q=search_query, type='track', limit=10)
    return results['tracks']['items']
  elif search_type == 'artist':
    results = sp.search(q=search_query, type='artist', limit=10)
    return results['artists']['items']
  elif search_type == 'album':
    results = sp.search(q=search_query, type='album', limit=10)
    return results['albums']['items']

def displayResults(results, search_type):
  if search_type == 'track':
    for track in results:
      st.image(track["album"]["images"][0]["url"], caption=track["name"], use_column_width=True)
      st.write(f"Artist: {track['artists'][0]['name']}")
      st.write(f"Album: {track['album']['name']}")
      st.write(f"Release Date: {track['album']['release_date']}")
      if track['preview_url']:
        st.write("Preview:")
        st.audio(track['preview_url'])
      else:
        st.write("Preview not available.")
      st.divider()
  elif search_type == 'artist':
    for artist in results:
      if artist["images"]:
        st.image(artist["images"][0]["url"], caption=artist["name"], use_column_width=True)
      st.write(f"Followers: {artist['followers']['total']}")
      st.write(f"Genres: {', '.join(artist['genres'])}")
      st.divider()
  elif search_type == 'album':
    for album in results:
      st.image(album["images"][0]["url"], caption=album["name"], use_column_width=True)
      st.write(f"Artist: {album['artists'][0]['name']}")
      st.write(f"Release Date: {album['release_date']}")
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
    search_query = st.text_input("Enter artist, album, or track name")
  with col2:
    search_type = st.selectbox("Select search type", ["track", "album", "artist"])
  if st.button("Search") and search_query:
    with st.spinner("Fetching results..."):
      results = fetchMusicData(sp, search_query, search_type)
      displayResults(results, search_type)
