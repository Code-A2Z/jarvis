import gdown
import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image

breed_labels = [
  "affenpinscher",
  "afghan_hound",
  "african_hunting_dog",
  "airedale",
  "american_staffordshire_terrier",
  "appenzeller",
  "australian_terrier",
  "basenji",
  "basset",
  "beagle",
  "bedlington_terrier",
  "bernese_mountain_dog",
  "black-and-tan_coonhound",
  "blenheim_spaniel",
  "bloodhound",
  "bluetick",
  "border_collie",
  "border_terrier",
  "borzoi",
  "boston_bull",
  "bouvier_des_flandres",
  "boxer",
  "brabancon_griffon",
  "briard",
  "brittany_spaniel",
  "bull_mastiff",
  "cairn",
  "cardigan",
  "chesapeake_bay_retriever",
  "chihuahua",
  "chow",
  "clumber",
  "cocker_spaniel",
  "collie",
  "curly-coated_retriever",
  "dandie_dinmont",
  "dhole",
  "dingo",
  "doberman",
  "english_foxhound",
  "english_setter",
  "english_springer",
  "entlebucher",
  "eskimo_dog",
  "flat-coated_retriever",
  "french_bulldog",
  "german_shepherd",
  "german_short-haired_pointer",
  "giant_schnauzer",
  "golden_retriever",
  "gordon_setter",
  "great_dane",
  "great_pyrenees",
  "greater_swiss_mountain_dog",
  "groenendael",
  "ibizan_hound",
  "irish_setter",
  "irish_terrier",
  "irish_water_spaniel",
  "irish_wolfhound",
  "italian_greyhound",
  "japanese_spaniel",
  "keeshond",
  "kelpie",
  "kerry_blue_terrier",
  "komondor",
  "kuvasz",
  "labrador_retriever",
  "lakeland_terrier",
  "leonberg",
  "lhasa",
  "malamute",
  "malinois",
  "maltese_dog",
  "mexican_hairless",
  "miniature_pinscher",
  "miniature_poodle",
  "miniature_schnauzer",
  "newfoundland",
  "norfolk_terrier",
  "norwegian_elkhound",
  "norwich_terrier",
  "old_english_sheepdog",
  "otterhound",
  "papillon",
  "pekinese",
  "pembroke",
  "pomeranian",
  "pug",
  "redbone",
  "rhodesian_ridgeback",
  "rottweiler",
  "saint_bernard",
  "saluki",
  "samoyed",
  "schipperke",
  "scotch_terrier",
  "scottish_deerhound",
  "sealyham_terrier",
  "shetland_sheepdog",
  "shih-tzu",
  "siberian_husky",
  "silky_terrier",
  "soft-coated_wheaten_terrier",
  "staffordshire_bullterrier",
  "standard_poodle",
  "standard_schnauzer",
  "sussex_spaniel",
  "tibetan_mastiff",
  "tibetan_terrier",
  "toy_poodle",
  "toy_terrier",
  "vizsla",
  "walker_hound",
  "weimaraner",
  "welsh_springer_spaniel",
  "west_highland_white_terrier",
  "whippet",
  "wire-haired_fox_terrier",
  "yorkshire_terrier",
]


@st.cache_resource
def loadModel():
  """Recreate the model architecture and load weights"""
  try:
    gdown.download(f"https://drive.google.com/uc?id={st.secrets['dogBreedClassificationModel']['MODEL']}", "Model.h5", quiet=False)
    base_model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights="imagenet")
    base_model.trainable = False
    model = tf.keras.Sequential(
      [
        base_model,
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(120, activation="softmax", kernel_regularizer=tf.keras.regularizers.l2(0.01)),
      ]
    )

    try:
      model.load_weights("Model.h5")
    except Exception:
      model.load_weights(tf.train.latest_checkpoint("./"))
    return model
  except Exception as e:
    st.error(f"Error loading model: {e}", icon="🚨")
    return None


def preprocessImage(img):
  """Preprocess image for MobileNetV2"""
  img = img.convert("RGB")
  img = img.resize((224, 224))
  img_array = tf.keras.preprocessing.image.img_to_array(img)
  img_array = np.expand_dims(img_array, axis=0)
  img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
  return img_array


def uploadDogImg():
  img = st.file_uploader("Upload a dog image", type=["jpg", "jpeg", "png"])
  if img is not None:
    try:
      img_data = Image.open(img)
      processed_img = preprocessImage(img_data)
      return processed_img
    except Exception as e:
      st.error(f"Error processing image: {e}", icon="🚨")
      return None
  return None


def predictBreed(x):
  """Predict dog breed from preprocessed image"""
  model = loadModel()
  if model is None:
    st.toast("Failed to load model", icon="🚨")
    return None, 0

  try:
    predictions = model.predict(x)
    predicted_idx = np.argmax(predictions[0])
    confidence = predictions[0][predicted_idx]
    return breed_labels[predicted_idx], confidence
  except Exception as e:
    st.error(f"Error making prediction: {e}", icon="🚨")
    return None, 0


def dogBreedClassifier():
  st.toast("Upload a photo of a dog to identify its breed", icon="🐶")
  input_img = uploadDogImg()

  if st.button("Predict Breed") and input_img is not None:
    breed, confidence = predictBreed(input_img)
    if breed is not None:
      st.success(f"Hi User, This appears to be a {breed} breed with {confidence:.2%} confidence! 🐕", icon="🎉")
