import random

import requests
import streamlit as st


def quizGame():
  st.title("Dynamic Quiz Generator")

  if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
  if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
  if "submitted" not in st.session_state:
    st.session_state.submitted = False
  if "shuffled_options" not in st.session_state:
    st.session_state.shuffled_options = {}

  st.sidebar.header("Quiz Options")
  categories_url = "https://opentdb.com/api_category.php"
  response = requests.get(categories_url)
  categories_data = response.json()

  if response.status_code == 200 and "trivia_categories" in categories_data:
    categories = categories_data["trivia_categories"]
    category_dict = {cat["name"]: cat["id"] for cat in categories}

    selected_category = st.sidebar.selectbox("Select a category", list(category_dict.keys()))
    selected_category_id = category_dict[selected_category]
    difficulty = st.sidebar.selectbox("Select difficulty", ["easy", "medium", "hard"])
  else:
    st.error("Failed to fetch categories. Try again later.")
    st.stop()

  if st.sidebar.button("Start Quiz"):
    num_questions = 5
    quiz_url = f"https://opentdb.com/api.php?amount={num_questions}&category={selected_category_id}&difficulty={difficulty}&type=multiple"
    quiz_response = requests.get(quiz_url)
    quiz_data = quiz_response.json()

    if quiz_response.status_code == 200 and quiz_data["response_code"] == 0:
      st.session_state.quiz_data = quiz_data["results"]
      st.session_state.user_answers = {}
      st.session_state.submitted = False
      st.session_state.shuffled_options = {}
    else:
      st.error("Failed to fetch quiz questions. Try again later.")

  if st.session_state.quiz_data:
    st.subheader(f"{selected_category} Quiz ({difficulty.capitalize()})")

    with st.form("quiz_form"):
      for i, q in enumerate(st.session_state.quiz_data):
        question = q["question"]
        correct_answer = q["correct_answer"]
        incorrect_answers = q["incorrect_answers"]

        if i not in st.session_state.shuffled_options:
          options = incorrect_answers + [correct_answer]
          random.shuffle(options)
          st.session_state.shuffled_options[i] = options
        else:
          options = st.session_state.shuffled_options[i]

        st.write(f"**Question {i + 1}:** {question}")
        st.session_state.user_answers[i] = st.radio(
          f"Choose an answer for Question {i + 1}",
          options,
          key=f"q{i}",
        )

      if st.form_submit_button("Submit Quiz"):
        st.session_state.submitted = True

  if st.session_state.submitted:
    st.subheader("Quiz Results")
    score = 0

    for i, q in enumerate(st.session_state.quiz_data):
      correct_answer = q["correct_answer"]
      if st.session_state.user_answers.get(i) == correct_answer:
        score += 1
        st.write(f"✅ **Question {i + 1}:** Correct!")
      else:
        st.write(f"❌ **Question {i + 1}:** Incorrect! The correct answer was **{correct_answer}**.")

    st.write(f"Your score: **{score}/{len(st.session_state.quiz_data)}**")
    if score == len(st.session_state.quiz_data):
      st.balloons()
    else:
      st.warning("Better luck next time!")
