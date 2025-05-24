import tensorflow as tf
import streamlit as st
import numpy as np
import librosa
import matplotlib.pyplot as plt
import gdown

@st.cache_resource
def load_model():
	gdown.download(f"https://drive.google.com/uc?id={st.secrets['depressionDetectionModel']['DEPRESSION_DETECT']}", 'DepressionDetect.keras', quiet=False)
	model = tf.keras.models.load_model("DepressionDetect.keras")
	return model

def depressionDetectionModel():
	model = load_model()
	st.write("Depression Detection Test Using Audio")
	uploaded_file = st.file_uploader("Upload file in .wav format",type="wav")
	if uploaded_file is not None:
		y,sr = librosa.load(uploaded_file,sr=None)
		st.audio(uploaded_file, format='audio/wav')
		fig, ax = plt.subplots()
		librosa.display.waveshow(y, sr=sr, ax=ax)
		ax.set_title('Waveform')
		st.pyplot(fig)
		spec = librosa.power_to_db(librosa.feature.melspectrogram(y = np.float32(y), sr=sr, n_fft=2048, hop_length=128, n_mels=512), ref=np.max)

		fig, ax = plt.subplots()
		img = librosa.display.specshow(spec,sr=sr, x_axis='time', y_axis='mel', ax=ax, cmap='viridis')
		ax.set_title('Mel Spectrogram')
		st.pyplot(fig)

		fig.canvas.draw()
		# Convert to numpy array
		img_array = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.int8)
		img_array = img_array.reshape(fig.canvas.get_width_height()[::-1] + (3,))

		# Prepare the spectrogram for the CNN model
		img_array = tf.image.resize(img_array, [64, 108])  # Resize to 64x108
		img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
		img_array = np.array(img_array,dtype=np.float32)
		prediction = model.predict(img_array)
		if prediction*100 > 50:
			st.error(f'Hi {st.session_state.name}, you seem to have Depression. Please consult a doctor and take care.')
		else:
			st.success(f'Hi {st.session_state.name}, you seem to perfectly fine. Take care and enjoy !!!')
