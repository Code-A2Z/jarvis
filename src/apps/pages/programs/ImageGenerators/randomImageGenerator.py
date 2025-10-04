import base64

import requests
import streamlit as st

resolutions = {
  "Instagram": {
    "Square": (1080, 1080),
    "Portrait": (1080, 1350),
    "Landscape": (1080, 566),
    "Story": (1080, 1920),
    "Reels": (1080, 1920),
  },
  "Facebook": {
    "Post": (1200, 630),
    "Cover": (820, 312),
    "Story": (1080, 1920),
    "Event": (1920, 1080),
  },
  "Twitter": {
    "Post": (1200, 675),
    "Header": (1500, 500),
    "Card": (800, 418),
  },
  "LinkedIn": {
    "Post": (1200, 627),
    "Banner": (1584, 396),
    "Story": (1080, 1920),
  },
  "YouTube": {
    "Thumbnail": (1280, 720),
    "Channel Art": (2560, 1440),
    "Video": (1920, 1080),
  },
  "TikTok": {
    "Post": (1080, 1920),
    "Story": (1080, 1920),
  },
  "Snapchat": {
    "Snap": (1080, 1920),
    "Story": (1080, 1920),
  },
  "WhatsApp": {
    "Status": (1080, 1920),
    "Post": (1080, 1080),
  },
  "Telegram": {
    "Post": (1280, 720),
    "Story": (1080, 1920),
  },
  "Discord": {
    "Post": (1200, 675),
    "Banner": (1920, 480),
  },
}


def getImage(height, width, isGrayscale, blur):
  params = []
  if isGrayscale:
    params.append("grayscale")
  if blur:
    params.append(f"blur={blur}")
  URL = f"https://picsum.photos/{width}/{height}" + ("?" + "&".join(params) if params else "")

  try:
    response = requests.get(URL)
    if response.status_code == 200:
      fileFormat = response.headers.get("Content-Type", "image/jpeg").split("/")[-1]
      encoded_image = base64.b64encode(response.content).decode()
      return response.content, encoded_image, fileFormat
    else:
      st.error("Could not get image. Please try again later.")
      return None, None, None
  except Exception as e:
    st.error(str(e))
    return None, None, None


def randomImageGenerator():
  choice = st.selectbox("Select a social media platform", list(resolutions.keys()) + ["Custom Resolutions"])
  if choice == "Custom Resolutions":
    col1, col2 = st.columns(2)
    with col1:
      width = st.number_input("Select image width", min_value=0, max_value=2400, value=400, step=10)
    with col2:
      height = st.number_input("Select image height", min_value=0, max_value=2400, value=300, step=10)
  elif choice in resolutions:
    resolution = st.selectbox("Select a resolution", list(resolutions[choice].keys()))
    width, height = resolutions[choice][resolution]

  blur = st.slider("Blur", 0, 10, 0)
  isGrayscale = st.checkbox("Grayscale")

  if st.button("Find"):
    image_bytes, encoded_image, fileFormat = getImage(height, width, isGrayscale, blur)
    if image_bytes:
      st.image(image_bytes, caption="Generated Image", channels="RGB", output_format=fileFormat)
      st.download_button(label="Download Image", data=image_bytes, file_name=f"random_image.{fileFormat}", mime=f"image/{fileFormat}")
