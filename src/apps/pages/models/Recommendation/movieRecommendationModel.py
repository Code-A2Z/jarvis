import pickle

import requests
import streamlit as st

from src.helpers.kaggle import downloadNotebookOutput


def load_data():
  downloadNotebookOutput("avdhesh15", "movie-recommendation-app", "notebook")
  with open("notebook/movies_list.pkl", "rb") as movies_file:
    movies_data = pickle.load(movies_file)
  with open("notebook/similarity.pkl", "rb") as similarity_file:
    similarity = pickle.load(similarity_file)
  movies_list = movies_data["title"].values
  return movies_data, similarity, movies_list


try:
  movies_data, similarity, movies_list = load_data()
except Exception as e:
  st.error(f"Data could not be loaded: {e}", icon="🚨")
  st.stop()


def fetchData(movie_id):
  url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={st.secrets['api_key']['TMDB_API_KEY']}"
  data = requests.get(url).json()
  movie_data = {
    "original_title": data["original_title"],
    "poster_path": f"https://image.tmdb.org/t/p/w500{data['poster_path']}",
    "backdrop_path": f"https://image.tmdb.org/t/p/w500{data['backdrop_path']}",
    "overview": data["overview"],
    "runtime": data["runtime"],
    "release_date": data["release_date"],
    "spoken_languages": data["spoken_languages"],
    "genres": data["genres"],
  }
  return movie_data


def recommend(movie, num_movies_recommend):
  movie_index = movies_data[movies_data["title"] == movie].index[0]
  distances = similarity[movie_index]
  movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1 : num_movies_recommend + 1]
  recommended_movies = []
  recommended_movies_data = []
  for i in movies_list:
    recommended_movies.append(movies_data.iloc[i[0]].title)
    poster = fetchData(movies_data.iloc[i[0]].id)
    recommended_movies_data.append(poster)
  return recommended_movies, recommended_movies_data


def movieRecommendationModel():
  movie = st.selectbox("Select a movie from dropdown", [None] + [m for m in movies_list])
  num_movies_recommend = st.slider("Select number of movies to recommend", 1, 20, 5)

  if st.button("Show Recommend") and movie is not None:
    recommended_movies, recommended_movies_data = recommend(movie, num_movies_recommend)
    if recommended_movies:
      for i, (m, p) in enumerate(zip(recommended_movies, recommended_movies_data, strict=False)):
        st.divider()
        col1, col2 = st.columns([1, 2])
        with col1:
          if p["poster_path"]:
            st.image(p["poster_path"], caption=p["original_title"])
          elif p["backdrop_path"]:
            st.image(p["backdrop_path"], caption=p["original_title"])
          else:
            st.warning("Poster not available", icon="⚠️")
        with col2:
          st.write(f"> ##### {i + 1}. {m}")
          st.write(f"**Overview**: {p['overview']}")
          st.write(f"**Runtime**: {p['runtime']} minutes")
          st.write(f"**Release Date**: {p['release_date']}")
          st.write(f"**Spoken Languages**: {', '.join([language['name'] for language in p['spoken_languages']])}")
          st.write(f"**Genres**: {', '.join([g['name'] for g in p['genres']])}")
    else:
      st.error("No movies found for recommendation.", icon="🚨")
  st.toast("This model is based on content-based filtering.", icon="ℹ️")
