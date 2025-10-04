import requests
import streamlit as st

BASE_URL = "https://api.jikan.moe/v4"
ALL_GENRES = {
  "Action": 1,
  "Adventure": 2,
  "Comedy": 4,
  "Drama": 8,
  "Educational": 56,
  "Fantasy": 10,
  "Gag Humor": 57,
  "Gourmet": 47,
  "Historical": 13,
  "Idols (Female)": 60,
  "Idols (Male)": 61,
  "Iyashikei": 63,
  "Josei": 43,
  "Kids": 15,
  "Mahou Shoujo": 66,
  "Martial Arts": 17,
  "Mecha": 18,
  "Military": 38,
  "Music": 19,
  "Mythology": 6,
  "Parody": 20,
  "Performing Arts": 70,
  "Pets": 71,
  "Psychological": 40,
  "Racing": 3,
  "Romance": 22,
  "Samurai": 21,
  "School": 23,
  "Sci-Fi": 24,
  "Shoujo": 25,
  "Shounen": 27,
  "Showbiz": 75,
  "Slice of Life": 36,
  "Space": 29,
  "Sports": 30,
  "Strategy Game": 11,
  "Super Power": 31,
  "Supernatural": 37,
  "Suspense": 41,
  "Team Sports": 77,
  "Time Travel": 78,
  "Urban Fantasy": 82,
  "Vampire": 32,
  "Video Game": 79,
  "Visual Arts": 80,
  "Workplace": 48,
}


def top_animes():
  URL = f"{BASE_URL}/top/anime"
  try:
    response = requests.get(URL)
    data = response.json()
    if response.status_code == 200:
      st.toast("Top 10 Animes", icon="✅")
      for anime_details in data["data"][:10]:
        st.divider()
        image = anime_details["images"]["jpg"]["large_image_url"]
        link_url = anime_details["url"]
        status = anime_details["status"] if anime_details["status"] else "--"
        score = str(anime_details["score"]) + "/10" if anime_details["score"] else "--"
        synopsis = anime_details["synopsis"] if anime_details["synopsis"] else "--"
        season = anime_details["season"] if anime_details["season"] else "--"
        year = anime_details["year"] if anime_details["year"] else "--"
        anime_genres = "Genre: " + ", ".join([genre_name["name"] for genre_name in anime_details["genres"]])

        col1, col2 = st.columns([1, 2])
        with col1:
          st.image(image, caption=anime_details["title"])
        with col2:
          st.markdown(f"##### 😀 [{anime_details['title']}]({link_url})")
          st.write(f"{score} &nbsp; | &nbsp;  {year} &nbsp;  |  &nbsp; {season}")
          st.write(f"{anime_genres}")
          st.write(f"**Status**: {status}")
          with st.expander("Synopsis", expanded=False):
            st.write(synopsis)
    else:
      st.error("API call not successful. Please try again later.", icon="🚨")
  except Exception as e:
    st.error(f"An unexpected error occurred: {e}", icon="🚨")


def top_characters():
  URL = f"{BASE_URL}/top/characters"
  try:
    response = requests.get(URL)
    data = response.json()
    if response.status_code == 200:
      st.toast("Top 10 Characters", icon="✅")
      character_map = {character["name"]: character for character in data["data"][:10] if character}
      for character_name, character_details in character_map.items():
        st.divider()
        image_url = character_details["images"]["jpg"]["image_url"]
        link_url = character_details["url"]
        about = character_details["about"] if character_details["about"] else "--"
        nicknames = ", ".join(
          [name for name in character_details["nicknames"]] + [character_details["name_kanji"]] if character_details["name_kanji"] else []
        )

        col1, col2 = st.columns([1, 2])
        with col1:
          st.image(image_url, caption=character_name)
        with col2:
          st.markdown(f"##### 😎 [{character_name}]({link_url})")
          st.write(f"{nicknames}")
          with st.expander("About", expanded=False):
            st.write(about)
    else:
      st.error("API call not successful. Please try again later.", icon="🚨")
  except Exception as e:
    st.error(f"An unexpected error occurred: {e}", icon="🚨")


def get_animes_by_genres(selected_genres, order, sort):
  genres = ",".join([str(ALL_GENRES[genre]) for genre in selected_genres])
  query = f"?genres={genres}&order_by={order}&sort={sort}"
  URL = f"{BASE_URL}/anime{query}"
  try:
    response = requests.get(URL)
    data = response.json()
    if response.status_code == 200:
      st.toast("Anime By Genres", icon="✅")
      for anime_details in data["data"][:10]:
        st.divider()
        image = anime_details["images"]["jpg"]["large_image_url"]
        link_url = anime_details["url"]
        status = anime_details["status"] if anime_details["status"] else "--"
        score = str(anime_details["score"]) + "/10" if anime_details["score"] else "--"
        synopsis = anime_details["synopsis"] if anime_details["synopsis"] else "--"
        season = anime_details["season"] if anime_details["season"] else "--"
        year = anime_details["year"] if anime_details["year"] else "--"
        anime_genres = "Genre: " + ", ".join([genre_name["name"] for genre_name in anime_details["genres"]])

        col1, col2 = st.columns([1, 2])
        with col1:
          st.image(image, caption=anime_details["title"])
        with col2:
          st.markdown(f"##### 👉 [{anime_details['title']}]({link_url})")
          st.write(f"{score} &nbsp; | &nbsp;  {year} &nbsp;  |  &nbsp; {season}")
          st.write(f"{anime_genres}")
          st.write(f"**Status**: {status}")
          with st.expander("Synopsis", expanded=False):
            st.write(synopsis)
    else:
      st.error("API call not successful. Please try again later.", icon="🚨")
  except Exception as e:
    st.error(f"An unexpected error occurred: {e}", icon="🚨")


def anime():
  option = st.selectbox("Select an option", options=["Animes by Genres", "Top Animes", "Top Characters"])

  if option == "Top Animes":
    top_animes()
  elif option == "Top Characters":
    top_characters()
  else:
    col1, col2, col3 = st.columns(3)
    with col1:
      sort = st.selectbox("Select type", options=["desc", "asc"])
    with col2:
      order = st.selectbox("Select order", options=["score", "start_date", "end_date", "episodes", "rank", "popularity", "favorites"])
    with col3:
      selected_genres = st.multiselect("Select genres", options=[genre for genre in ALL_GENRES])
    if selected_genres:
      get_animes_by_genres(selected_genres, order, sort)
