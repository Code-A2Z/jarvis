import random

import numpy as np
import streamlit as st


def initialize_game(level):
  if level == "Easy":
    size = 6
    num_mines = 5
  elif level == "Medium":
    size = 10
    num_mines = 20
  else:  # Hard
    size = 20
    num_mines = 50

  board = np.zeros((size, size), dtype=int)
  board = place_mines(board, num_mines)
  board = calculate_adjacent_mines(board)
  flags = np.zeros_like(board, dtype=bool)
  return board, flags, num_mines


def place_mines(board, num_mines):
  size = board.shape[0]
  mines_placed = 0
  while mines_placed < num_mines:
    row = random.randint(0, size - 1)
    col = random.randint(0, size - 1)
    if board[row, col] == 0:
      board[row, col] = -1  # -1 represents a mine
      mines_placed += 1
  return board


def calculate_adjacent_mines(board):
  size = board.shape[0]
  for row in range(size):
    for col in range(size):
      if board[row, col] == -1:
        continue
      count = 0
      for i in range(max(0, row - 1), min(size, row + 2)):
        for j in range(max(0, col - 1), min(size, col + 2)):
          if board[i, j] == -1:
            count += 1
      board[row, col] = count
  return board


def reset_game():
  st.session_state["board"], st.session_state["flags"], st.session_state["num_mines"] = initialize_game(st.session_state["level"])
  st.session_state["revealed"] = np.zeros_like(st.session_state["board"], dtype=bool)
  st.session_state["flag_mode"] = False
  st.session_state["game_over"] = False
  st.session_state["win"] = False


def toggle_flag(row, col):
  st.session_state["flags"][row, col] = not st.session_state["flags"][row, col]


def reveal_cell(row, col):
  if st.session_state["revealed"][row, col] or st.session_state["flags"][row, col]:
    return
  st.session_state["revealed"][row, col] = True
  if st.session_state["board"][row, col] == -1:
    st.session_state["game_over"] = True
    return
  if st.session_state["board"][row, col] == 0:
    for i in range(max(0, row - 1), min(st.session_state["board"].shape[0], row + 2)):
      for j in range(max(0, col - 1), min(st.session_state["board"].shape[1], col + 2)):
        if not st.session_state["revealed"][i, j]:
          reveal_cell(i, j)
  check_win()


def check_win():
  if np.all((st.session_state["board"] == -1) | st.session_state["revealed"]):
    st.session_state["win"] = True


def get_cell_style(value):
  style_map = {
    0: "background-color: white; color: black;",
    1: "background-color: yellow; color: black;",
    2: "background-color: orange; color: black;",
    3: "background-color: red; color: white;",
    4: "background-color: darkred; color: white;",
  }

  return style_map.get(value, "background-color: black; color: white;")


def display_board(board, revealed, flags):
  for i in range(board.shape[0]):
    cols = st.columns(board.shape[1])
    for j in range(board.shape[1]):
      if revealed[i, j]:
        if board[i, j] == -1:
          cols[j].button("💣", disabled=True, key=f"mine-{i}-{j}")
        else:
          cols[j].button(str(board[i, j]), disabled=True, key=f"cell-{i}-{j}")
      elif flags[i, j]:
        cols[j].button("🚩", disabled=True, key=f"flag-{i}-{j}")
      else:
        cols[j].button(" ", key=f"empty-{i}-{j}")


def minesweeper():
  st.title(" 💣 Minesweeper Game 💣 ")

  if "level" not in st.session_state:
    st.session_state["level"] = "Easy"
  if "board" not in st.session_state:
    st.session_state["board"], st.session_state["flags"], st.session_state["num_mines"] = initialize_game(st.session_state["level"])
  if "revealed" not in st.session_state:
    st.session_state["revealed"] = np.zeros_like(st.session_state["board"], dtype=bool)
  if "flag_mode" not in st.session_state:
    st.session_state["flag_mode"] = False
  if "game_over" not in st.session_state:
    st.session_state["game_over"] = False
  if "win" not in st.session_state:
    st.session_state["win"] = False
  if "show_instructions" not in st.session_state:
    st.session_state["show_instructions"] = False

  col1, col2, col3, col4, col5 = st.columns([2, 2, 1.5, 2, 1])

  with col1:
    level = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=["Easy", "Medium", "Hard"].index(st.session_state["level"]))
    if level != st.session_state["level"]:
      st.session_state["level"] = level
      reset_game()

  with col2:
    if st.button("Reset Game"):
      reset_game()

  with col3:
    st.session_state["flag_mode"] = st.checkbox("Flag Mode", value=st.session_state["flag_mode"])

  with col4:
    num_flags = np.sum(st.session_state["flags"])
    mines_left = st.session_state["num_mines"] - num_flags
    st.write(f"**Flags**: {num_flags}  |  **Mines left**: {mines_left}")

  with col5:
    instructions_text = """
        ### Minesweeper Game Instructions

        Objective: Clear all cells without hitting a mine.

        How to Play:

        Select Difficulty: Choose from Easy, Medium, or Hard to start the game. Changing difficulty resets the board.

        Revealing Cells:
        - Double Click a cell to reveal it.
        - Numbers indicate nearby mines.
        - Empty cells reveal surrounding areas automatically.
        - Click a mine, and the game ends.

        Flagging Mines:
        - Check Flag Mode to mark suspected mines with a flag (🚩).
        - Toggle Flag Mode to place or remove flags.

        Game Reset: Use Reset Game to start a new board anytime.

        Game End Conditions:
        - Win: You win the game if all non-mine cells are revealed.
        - Loss: If you accidentally reveal a mine, the game is over.

        Enjoy the game!
        """
    if st.button(" ℹ️ "):
      st.session_state["show_instructions"] = not st.session_state["show_instructions"]

  if st.session_state["game_over"]:
    st.error("Game Over! You hit a mine.")
    st.markdown("### Don't give up! Try again by clicking the reset button.")
    for i in range(st.session_state["board"].shape[0]):
      for j in range(st.session_state["board"].shape[1]):
        if st.session_state["board"][i, j] == -1:
          st.session_state["revealed"][i, j] = True

    # Display the board with all mines revealed
    display_board(st.session_state["board"], st.session_state["revealed"], st.session_state["flags"])
    return

  if st.session_state["win"]:
    st.balloons()
    st.success("Congratulations! You won the game.")
    return

  if st.session_state["show_instructions"]:
    st.markdown(instructions_text)

  board = st.session_state["board"]
  revealed = st.session_state["revealed"]
  flags = st.session_state["flags"]

  for row in range(board.shape[0]):
    cols = st.columns(board.shape[1])
    for col in range(board.shape[1]):
      if revealed[row, col]:
        if board[row, col] == -1:
          cols[col].button("💣", key=f"{row}-{col}", disabled=True)
        else:
          style = get_cell_style(board[row, col])
          cols[col].markdown(f"<button style='{style}' disabled>{board[row, col]}</button>", unsafe_allow_html=True)
      else:
        if flags[row, col]:
          if cols[col].button("🚩", key=f"{row}-{col}"):
            toggle_flag(row, col)
        else:
          if cols[col].button(" ", key=f"{row}-{col}"):
            if st.session_state["flag_mode"]:
              toggle_flag(row, col)
            else:
              reveal_cell(row, col)
