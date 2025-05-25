from keras.preprocessing import image
from datetime import datetime
import tensorflow as tf
import streamlit as st
import numpy as np
import gdown
import cv2

@st.cache_resource
def load_model():
  gdown.download(f"https://drive.google.com/uc?id={st.secrets['maskDetectionModel']['RES10_300x300_SSD_ITER_140000']}", 'res10_300x300_ssd_iter_140000.caffemodel', quiet=False)
  gdown.download(f"https://drive.google.com/uc?id={st.secrets['maskDetectionModel']['DEPLOY']}", 'deploy.prototxt', quiet=False)
  gdown.download(f"https://drive.google.com/uc?id={st.secrets['maskDetectionModel']['MASKCHECK']}", 'maskcheck.keras', quiet=False)
  model = tf.keras.models.load_model('maskcheck.keras')
  return model

def hardware():
  with st.form("mtest"):
    option = st.selectbox("What are you using",("Laptop camera", "External camera"))
    btn = st.form_submit_button("Submit")
    if option == "Laptop camera":
      return 0, btn
    else:
      return 1, btn

def maskDetectionModel():
  cnn = load_model()
  modelFile = "res10_300x300_ssd_iter_140000.caffemodel"
  configFile = "deploy.prototxt"
  net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
  flag = False
  h,flag = hardware()
  cap = cv2.VideoCapture(h)
  st.write("Press 'q' to stop")

  if flag == True:
    while cap.isOpened():
      ret, img = cap.read()
      if not ret:
        break

      h, w = img.shape[:2]
      blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
      net.setInput(blob)
      detections = net.forward()

      for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
          box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
          (x, y, x1, y1) = box.astype("int")
          face_img = img[y:y1, x:x1]
          cv2.imwrite('temp.jpg', face_img)
          test_image = image.load_img('temp.jpg', target_size=(64, 64))
          test_image = image.img_to_array(test_image)
          test_image = np.expand_dims(test_image, axis=0)
          pred = cnn.predict(test_image) * 100

          if pred > 50:
            cv2.rectangle(img, (x, y), (x1, y1), (0, 0, 255), 3)
            cv2.putText(img, 'No Mask', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
          else:                 
            cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 3)
            cv2.putText(img, 'Mask', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

          datet = str(datetime.now())
          cv2.putText(img, datet, (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow('img', img)
        if cv2.waitKey(1) == ord('q'):
          break

  cv2.destroyAllWindows()
