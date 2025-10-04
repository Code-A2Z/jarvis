import random

import numpy as np
import streamlit as st


def the2048Game():
  # Add a new tile (2 or 4) to a random empty cell
  def add_new_tile(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
      i, j = random.choice(empty_cells)
      board[i][j] = random.choice([2, 2, 2, 4])

  # Initialize game state
  if "board" not in st.session_state:
    st.session_state.board = np.zeros((4, 4), dtype=int)
    st.session_state.score = 0

    for _ in range(2):
      add_new_tile(st.session_state.board)

  # Merge tiles in a row
  def merge(row):
    row = [x for x in row if x != 0]
    i = 0
    while i < len(row) - 1:
      if row[i] == row[i + 1]:
        row[i] *= 2
        st.session_state.score += row[i]
        row.pop(i + 1)
      i += 1
    return row + [0] * (4 - len(row))

  # Move tiles in the specified direction
  def move(board, direction):
    if direction in ["LEFT", "RIGHT"]:
      for i in range(4):
        row = list(board[i, :])
        if direction == "RIGHT":
          row.reverse()
        row = merge(row)
        if direction == "RIGHT":
          row.reverse()
        board[i, :] = row
    else:
      for j in range(4):
        col = list(board[:, j])
        if direction == "DOWN":
          col.reverse()
        col = merge(col)
        if direction == "DOWN":
          col.reverse()
        board[:, j] = col
    return board

  # Check if the game is over
  def is_game_over():
    if any(0 in row for row in st.session_state.board):
      return False
    for i in range(4):
      for j in range(3):
        if st.session_state.board[i][j] == st.session_state.board[i][j + 1]:
          return False
        if st.session_state.board[j][i] == st.session_state.board[j + 1][i]:
          return False
    return True

  # Move and update board
  def move_and_update(direction):
    old_board = st.session_state.board.copy()
    st.session_state.board = move(st.session_state.board, direction)
    if not np.array_equal(old_board, st.session_state.board):
      add_new_tile(st.session_state.board)

  # Title
  st.markdown(
    """
            
            <h1 style='text-align: center; padding-top: 50px; padding-bottom: 50px; font-size: 100px;'>
                2️⃣0️⃣4️⃣8️⃣ 
            </h1>
            """,
    unsafe_allow_html=True,
  )

  # Scorebox with Game Over Handling
  if is_game_over():
    st.markdown(
      f"""
                <div style='
                    font-size: 36px;
                    font-weight: bold;
                    color: white;
                    margin: 20px 0;
                    text-align: left;
                    border: 3px solid white;
                    border-radius: 10px;
                    padding: 10px 20px;
                    display: inline-block;
                    background-color: rgba(255, 0, 0, 0.7);
                '>
                    Game Over!<br>
                    Final Score: {st.session_state.score}
                </div>
            """,
      unsafe_allow_html=True,
    )
  else:
    st.markdown(
      f"""
                <div style='
                    font-size: 36px;
                    font-weight: bold;
                    color: white;
                    margin: 20px 0;
                    text-align: left;
                    border: 3px solid white;
                    border-radius: 10px;
                    padding: 10px 20px;
                    display: inline-block;
                    background-color: rgba(255, 255, 255, 0.1);
                '>
                    Score: {st.session_state.score}
                </div>
            """,
      unsafe_allow_html=True,
    )

  # Tile colors
  color_dict = {
    0: "#CDC1B4",
    2: "#EEE4DA",
    4: "#EDE0C8",
    8: "#F2B179",
    16: "#F59563",
    32: "#F67C5F",
    64: "#F65E3B",
    128: "#EDCF72",
    256: "#EDCC61",
    512: "#EDC850",
    1024: "#EDC53F",
    2048: "#EDC22E",
  }

  # Display Board
  for i in range(4):
    cols = st.columns(4)
    for j in range(4):
      value = st.session_state.board[i][j]
      bg_color = color_dict.get(value, "#CDC1B4")
      text_color = "#776E65" if value in [2, 4] else "#F9F6F2"
      cols[j].markdown(
        f"""
                    <div style='
                        background-color: {bg_color};
                        aspect-ratio: 1;
                        text-align: center;
                        font-size: 50px;
                        font-weight: bold;
                        color: {text_color};
                        border-radius: 5px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 5px 0px;
                    '>
                        {value if value != 0 else ""}
                    </div>
                    """,
        unsafe_allow_html=True,
      )

  # Transparent New Game Button
  st.markdown(
    """
            <style>
                div[data-testid="stButton"] button[kind="primary"] {
                    font-size: 24px !important;
                    font-weight: bold !important;
                    padding: 15px 30px !important;
                    border-radius: 10px !important;
                    background-color: transparent !important;
                    color: white !important;
                    border: 2px solid white !important;
                    margin: 20px 0 !important;
                }
            </style>
        """,
    unsafe_allow_html=True,
  )
  if st.button("New Game", type="primary"):
    st.session_state.board = np.zeros((4, 4), dtype=int)
    st.session_state.score = 0
    for _ in range(2):
      add_new_tile(st.session_state.board)
    st.rerun()

  # Arrow Controls (Larger Buttons)
  left_space, control_area, right_space = st.columns([2, 3, 2])
  with control_area:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
      if st.button("↑", key="up", type="secondary"):
        move_and_update("UP")
        st.rerun()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
      if st.button("←", key="left", type="secondary"):
        move_and_update("LEFT")
        st.rerun()
    with col2:
      if st.button("↓", key="down", type="secondary"):
        move_and_update("DOWN")
        st.rerun()
    with col3:
      if st.button("→", key="right", type="secondary"):
        move_and_update("RIGHT")
        st.rerun()

  # Add this custom CSS for bigger arrow buttons
  st.markdown(
    """
            <style>
                /* Existing New Game button style */
                div[data-testid="stButton"] button[kind="primary"] {
                    font-size: 24px !important;
                    font-weight: bold !important;
                    padding: 15px 30px !important;
                    border-radius: 10px !important;
                    background-color: transparent !important;
                    color: white !important;
                    border: 2px solid white !important;
                    margin: 20px 0 !important;
                }
                
                /* New style for arrow buttons */
                div[data-testid="stButton"] button[kind="secondary"] {
                    font-size: 40px !important;
                    padding: 20px 40px !important;
                    width: 100% !important;
                    aspect-ratio: 1 !important;
                    border-radius: 10px !important;
                    background-color: rgba(255, 255, 255, 0.1) !important;
                    color: white !important;
                    border: 2px solid white !important;
                }
            </style>
        """,
    unsafe_allow_html=True,
  )
