import os
import random

import instaloader
import streamlit as st
from instabot import Bot

loader = instaloader.Instaloader()


def likeUserPosts(username):
  password = st.text_input("Enter your Instagram password", type="password")
  if password:
    bot = Bot()
    bot.login(username, password)
    user_id = bot.get_user_id_from_username(username)
    user_posts = bot.get_user_medias(user_id)
    if not user_posts:
      st.warning("No posts found to like!")
      return
    num_posts_to_like = st.slider("Select the number of posts to like", 1, len(user_posts))
    posts_to_like = random.sample(user_posts, num_posts_to_like)
    for post in posts_to_like:
      bot.like(media_id=post)
    bot.logout()
    st.success(f"Liked {num_posts_to_like} posts from {username}.", icon="👍")


def followUser(username):
  password = st.text_input("Enter your Instagram password", type="password")
  if password:
    bot = Bot()
    bot.login(username, password)
    if bot.follow(username):
      st.success(f"Followed user: {username}", icon="👥")
    else:
      st.error(f"Failed to follow user: {username}.", icon="❌")
    bot.logout()


def unfollowUser(username):
  password = st.text_input("Enter your Instagram password", type="password")
  if password:
    bot = Bot()
    bot.login(username, password)
    if bot.unfollow(username):
      st.success(f"Unfollowed user: {username}", icon="🚫")
    else:
      st.error(f"Failed to unfollow user: {username}.", icon="❌")
    bot.logout()


def sendDirectMessage(username, message):
  password = st.text_input("Enter your Instagram password", type="password")
  if password:
    bot = Bot()
    bot.login(username, password)
    user_id = bot.get_user_id_from_username(username)
    bot.send_message(message, [user_id])
    bot.logout()
    st.success(f"Sent message to {username}.", icon="✉️")


def profileIDNumber(username):
  profile = instaloader.Profile.from_username(loader.context, username)
  st.success(f"Your profile ID is: {profile.userid}", icon="🆔")


def downloadProfilePicture(username):
  loader.download_profile(username, profile_pic_only=True)
  profile_dir = os.path.join(os.getcwd(), username)
  image = [os.path.join(profile_dir, img) for img in os.listdir(profile_dir) if img.endswith(".jpg")]
  st.image(image[0], caption=f"Profile picture of {username}")
  st.success(f"Profile picture of {username} downloaded.", icon="📸")


def downloadUserData(username):
  profile = instaloader.Profile.from_username(loader.context, username)
  loader.download_profile(profile.username, download_stories=True, fast_update=True)
  st.success(f"Downloaded posts and stories of {username}.", icon="📥")


def instagram():
  st.title("Instagram Automation 🤖")
  st.write("Automate tasks like liking posts, following/unfollowing users, sending messages, downloading profile pictures, and more!")

  username = st.text_input("Enter your Instagram username")
  if username:
    task = st.selectbox(
      "Choose a task",
      [
        None,
        "Know your profile ID number",
        "Download a user's profile picture",
        "Like posts from a user's profile",
        "Follow a user",
        "Unfollow a user",
        "Send a direct message to a user",
        "Download a user's recent posts and stories",
      ],
    )

    if task == "Know your profile ID number":
      profileIDNumber(username)
    elif task == "Download a user's profile picture":
      target_username = st.text_input("Enter the username of the profile")
      if st.button("Download Picture"):
        downloadProfilePicture(target_username)
    elif task == "Like posts from a user's profile":
      likeUserPosts(username)
    elif task == "Follow a user":
      target_username = st.text_input("Enter the username to follow")
      if st.button("Follow"):
        followUser(target_username)
    elif task == "Unfollow a user":
      target_username = st.text_input("Enter the username to unfollow")
      if st.button("Unfollow"):
        unfollowUser(target_username)
    elif task == "Send a direct message to a user":
      target_username = st.text_input("Enter the username to send a message")
      message = st.text_area("Enter your message")
      if st.button("Send Message"):
        sendDirectMessage(target_username, message)
    elif task == "Download a user's recent posts and stories" and st.button("Download Data"):
      downloadUserData(username)
