from transformers import TFSamModel, SamProcessor
import matplotlib.pyplot as plt
import tensorflow as tf
import streamlit as st
from PIL import Image
import numpy as np

tf.experimental.numpy.experimental_enable_numpy_behavior()

@st.cache_resource(ttl=86400)
def load_model():
  """Load the SAM model and processor."""
  model = TFSamModel.from_pretrained("facebook/sam-vit-base")
  processor = SamProcessor.from_pretrained("facebook/sam-vit-base")
  return model, processor

def generate_random_colors(n):
  """Generate n distinct colors."""
  colors = []
  for i in range(n):
    hue = i / n
    saturation = 0.7 + np.random.rand() * 0.3
    value = 0.7 + np.random.rand() * 0.3

    h = hue * 6
    c = value * saturation
    x = c * (1 - abs(h % 2 - 1))
    m = value - c

    if h < 1:
      rgb = (c, x, 0)
    elif h < 2:
      rgb = (x, c, 0)
    elif h < 3:
      rgb = (0, c, x)
    elif h < 4:
      rgb = (0, x, c)
    elif h < 5:
      rgb = (x, 0, c)
    else:
      rgb = (c, 0, x)

    colors.append(np.array([(r + m) * 0.7 for r in rgb] + [0.5]))
  return colors

def show_masks_on_image(raw_image, masks, scores):
  """Display all masks overlaid on the same image with different colors."""
  plt.clf()

  if isinstance(masks, tf.Tensor):
    masks = masks.numpy()
  if isinstance(scores, tf.Tensor):
    scores = scores.numpy()

  masks = np.squeeze(masks)
  scores = np.squeeze(scores)

  if len(masks.shape) == 2:
    masks = np.expand_dims(masks, 0)
    scores = np.expand_dims(scores, 0)

  fig, ax = plt.subplots(figsize=(12, 8))
  ax.imshow(raw_image)
  colors = generate_random_colors(len(masks))
  for i, (mask, score, color) in enumerate(zip(masks, scores, colors)):
    mask_image = np.zeros((mask.shape[0], mask.shape[1], 4))
    mask_image[:, :, 3] = mask * color[3]
    for j in range(3):
      mask_image[:, :, j] = mask * color[j]
    ax.imshow(mask_image)

    y_indices, x_indices = np.where(mask > 0.5)
    if len(x_indices) > 0 and len(y_indices) > 0:
        center_x = np.mean(x_indices)
        center_y = np.mean(y_indices)
        ax.text(center_x, 
                center_y, 
                f"Score: {float(score):.2f}",
                color='white',
                fontsize=8,
                bbox=dict(facecolor='black', alpha=0.5),
                ha='center',
                va='center'
              )

  ax.axis('off')
  plt.tight_layout()
  return fig

def process_and_show_masks(raw_image, model_outputs, processor_inputs, processor):
  """Process model outputs and display segmentation masks."""
  masks = processor.image_processor.post_process_masks(
    model_outputs.pred_masks,
    processor_inputs["original_sizes"],
    processor_inputs["reshaped_input_sizes"],
    return_tensors="tf",
  )
  fig = show_masks_on_image(raw_image, masks, model_outputs.iou_scores)
  st.pyplot(fig)
  plt.close(fig)

def segment_everything(raw_image, model, processor):
  """Segment all objects in the image using a grid of points."""
  height, width = raw_image.size[1], raw_image.size[0]
  grid_size = 32
  x_points = np.linspace(0, width, num=grid_size)
  y_points = np.linspace(0, height, num=grid_size)

  input_points = [[[x, y] for x in x_points[::4] for y in y_points[::4]]]
  inputs = processor(raw_image, input_points=input_points, return_tensors="tf")
  outputs = model(**inputs)
  return outputs, inputs

def segment_with_box(raw_image, box_coords, model, processor):
  """Segment objects within the specified box."""
  input_boxes = [[[box_coords[0], box_coords[1], box_coords[2], box_coords[3]]]]
  inputs = processor(raw_image, input_boxes=input_boxes, return_tensors="tf")
  outputs = model(**inputs)
  return outputs, inputs

def segment_with_point(raw_image, point_coords, model, processor):
  """Segment objects at the specified point."""
  input_points = [[[point_coords[0], point_coords[1]]]]
  inputs = processor(raw_image, input_points=input_points, return_tensors="tf")
  outputs = model(**inputs)
  return outputs, inputs

def segment_with_text(raw_image, text_prompt, model, processor):
  """Segment objects matching the text description."""
  inputs = processor(raw_image, return_tensors="tf")
  outputs = model(**inputs)
  return outputs, inputs

def segmentAnythingModel():
  with st.expander("About the Segment Anything Model (SAM)"):
    st.write("""
    Choose a segmentation mode and see the results!
    - Segment Everything: Detects and segments all objects in the image
    - Box Prompt: Draw a box around the area you want to segment
    - Point Prompt: Click a point to segment objects at that location
    - Text Prompt: Describe what you want to segment
    """)

  try:
    model, processor = load_model()
  except Exception as e:
    st.error(f"Error loading model: {str(e)}", icon="🚨")
    st.stop()

  uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
  if uploaded_file is not None:
    try:
      raw_image = Image.open(uploaded_file).convert("RGB")
      mode = st.selectbox("Select Segmentation Mode", ["Segment Everything", "Box Prompt", "Point Prompt", "Text Prompt"])
      if mode == "Segment Everything":
        if st.button("Generate Complete Segmentation"):
          outputs, inputs = segment_everything(raw_image, model, processor)
          process_and_show_masks(raw_image, outputs, inputs, processor)

      elif mode == "Box Prompt":
        st.info("Enter box coordinates", icon="ℹ️")
        col1, col2 = st.columns(2)
        with col1:
          x_min = st.number_input("X min", 0, raw_image.size[0])
          y_min = st.number_input("Y min", 0, raw_image.size[1])
        with col2:
          x_max = st.number_input("X max", x_min, raw_image.size[0])
          y_max = st.number_input("Y max", y_min, raw_image.size[1])
        if st.button("Segment with Box"):
          outputs, inputs = segment_with_box(raw_image, [x_min, y_min, x_max, y_max], model, processor)
          process_and_show_masks(raw_image, outputs, inputs, processor)

      elif mode == "Point Prompt":
        col1, col2 = st.columns(2)
        with col1:
          x_coord = st.number_input("X coordinate", 0, raw_image.size[0])
        with col2:
          y_coord = st.number_input("Y coordinate", 0, raw_image.size[1])
        if st.button("Segment at Point"):
          outputs, inputs = segment_with_point(raw_image, [x_coord, y_coord], model, processor)
          process_and_show_masks(raw_image, outputs, inputs, processor)

      elif mode == "Text Prompt":
        text_prompt = st.text_input("Describe what you want to segment")
        if st.button("Segment with Text") and text_prompt:
          outputs, inputs = segment_with_text(raw_image, text_prompt, model, processor)
          process_and_show_masks(raw_image, outputs, inputs, processor)

    except Exception as e:
      st.error(f"An error occurred: {str(e)}", icon="🚨")
