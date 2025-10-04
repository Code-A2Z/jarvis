import random
import time

import keyboard
import pygame
import streamlit as st
from PIL import Image


def dodgeGame():
  # Pygame Initialization (Headless Mode)
  pygame.init()
  SCREEN_WIDTH, SCREEN_HEIGHT = 200, 200
  PLAYER_WIDTH, PLAYER_HEIGHT = 25, 25
  BLOCK_WIDTH, BLOCK_HEIGHT = 25, 25
  FPS = 60

  # Colors
  WHITE = (255, 255, 255)
  BLACK = (0, 0, 0)

  def set_movement(direction):
    st.session_state.move_direction = direction

  # Initialize session state variables
  if "game_active" not in st.session_state:
    st.session_state.game_active = False
  if "game_over" not in st.session_state:
    st.session_state.game_over = False
  if "score" not in st.session_state:
    st.session_state.score = 0
  if "player_x" not in st.session_state:
    st.session_state.player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
  if "last_score" not in st.session_state:
    st.session_state.last_score = None

  def reset_game():
    st.session_state.game_active = True
    st.session_state.game_over = False
    st.session_state.score = 0
    st.session_state.player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
    st.session_state.last_score = None

  # Initialize Pygame in Offscreen Mode
  screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
  clock = pygame.time.Clock()

  def draw_bomb(surface, x, y, width, height):
    # Draw the main circle of the bomb (black)
    bomb_radius = min(width, height) // 2
    center_x = x + width // 2
    center_y = y + height // 2
    pygame.draw.circle(surface, BLACK, (center_x, center_y), bomb_radius)

    # Draw the fuse on top (brown)
    fuse_start = (center_x, center_y - bomb_radius)
    fuse_end = (center_x + width // 4, center_y - bomb_radius - height // 4)
    pygame.draw.line(surface, (139, 69, 19), fuse_start, fuse_end, 3)

  def dodge_the_blocks():
    player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
    player_speed = 4
    blocks = []
    block_speed = 2
    start_time = time.time()

    score_display = st.empty()
    game_frame = st.empty()

    while True:
      screen.fill(WHITE)

      # Player Control using keyboard
      if keyboard.is_pressed("left") and st.session_state.player_x > 0:
        st.session_state.player_x -= player_speed
      if keyboard.is_pressed("right") and st.session_state.player_x < SCREEN_WIDTH - PLAYER_WIDTH:
        st.session_state.player_x += player_speed

      # Draw Player
      pygame.draw.rect(screen, BLACK, (st.session_state.player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

      # Spawn and Move Blocks
      if random.randint(1, 45) == 1:
        block_x = random.randint(0, SCREEN_WIDTH - BLOCK_WIDTH)
        blocks.append([block_x, -BLOCK_HEIGHT])

      for block in blocks[:]:
        block[1] += block_speed
        draw_bomb(screen, block[0], block[1], BLOCK_WIDTH, BLOCK_HEIGHT)

        # Collision Detection
        if (
          block[1] + BLOCK_HEIGHT > player_y
          and block[1] < player_y + PLAYER_HEIGHT
          and block[0] < st.session_state.player_x + PLAYER_WIDTH
          and block[0] + BLOCK_WIDTH > st.session_state.player_x
        ):
          st.session_state.score = int(time.time() - start_time)
          st.session_state.game_over = True
          st.session_state.game_active = False
          game_frame.empty()
          score_display.empty()
          st.rerun()
          return

      # Remove Blocks Out of Bounds
      blocks = [block for block in blocks if block[1] < SCREEN_HEIGHT]

      # Convert Pygame surface to numpy array and then to PIL Image
      frame = pygame.surfarray.array3d(screen)
      frame = frame.swapaxes(0, 1)
      image = Image.fromarray(frame.astype("uint8"))
      game_frame.image(image, use_container_width=True)

      # Update Score Display
      current_score = int(time.time() - start_time)
      score_display.markdown(
        f"""
                <div style="
                    display: inline-block;
                    background-color: rgba(187, 173, 160, 0.1);
                    border: 2px solid rgba(255, 255, 255, 0.8);
                    border-radius: 10px;
                    padding: 8px 25px;
                    margin-bottom: 10px;
                    min-width: 100px;
                    text-align: center;
                    backdrop-filter: blur(5px);
                ">
                    <div style="
                        color: rgba(238, 228, 218, 0.95);
                        font-size: 13px;
                        font-weight: bold;
                        text-transform: uppercase;
                        margin-bottom: 2px;
                        letter-spacing: 1px;
                    ">
                        Score 💣
                    </div>
                    <div style="
                        color: rgba(255, 255, 255, 1);
                        font-size: 25px;
                        font-weight: bold;
                    ">
                        {current_score}
                    </div>
                </div>
            """,
        unsafe_allow_html=True,
      )

      clock.tick(FPS)

  # Streamlit Interface
  st.title("Dodge the Blocks")

  # Create placeholder for game area
  game_area = st.empty()

  # Game Logic with popup
  if st.session_state.game_over:
    # Clear any previous content
    game_area.empty()

    # Show game over message in game area
    with game_area.container():
      st.error("💥 GAME OVER!")
      st.write(f"### Score: {st.session_state.score}")
      if st.button("Play Again", key="play_again"):
        reset_game()
        st.rerun()

  elif not st.session_state.game_active:
    # Clear any previous content
    game_area.empty()

    # Show start game button
    with game_area.container():
      st.write("Use the **LEFT and RIGHT arrow keys** to move!")
      if st.button("Start Game", key="start"):
        reset_game()

  elif st.session_state.game_active:
    # Clear any previous content
    game_area.empty()

    # Show game instructions and run game
    st.write("Use the **LEFT and RIGHT arrow keys** to move!")
    dodge_the_blocks()
