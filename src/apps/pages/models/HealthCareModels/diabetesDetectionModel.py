import tensorflow as tf
import streamlit as st
import numpy as np
import gdown

@st.cache_resource
def load_model():
	gdown.download(f"https://drive.google.com/uc?id={st.secrets['diabetesDetectionModel']['DIABETES_TEST_MODEL']}", 'diabetes_test_model.keras', quiet=False)
	model = tf.keras.models.load_model('diabetes_test_model.keras')
	return model

def diabetesTestForm():
	details = []
	with st.form("dbtest"):
		col1,col2 = st.columns(2)
		details.append(col1.number_input("Pregnancies",min_value=0,step=1))
		details.append(col2.number_input("Glucose"))
		details.append(st.number_input("Blood pressure in mm Hg"))
		details.append(st.number_input("Triceps Skin Thickness in mm"))
		details.append(st.number_input("Insulin in mu U/ml"))
		details.append(st.number_input("BMI"))
		details.append(st.number_input("Age",min_value=1,step=1))
		btn = st.form_submit_button("Submit")
		return details, btn

def do_diabetes_test(input):
	model = load_model()
	res = model.predict(input)
	if res*100 > 50:
		return 1
	else:
		return 0

def diabetesDetectionModel():
	st.markdown("#### Enter all details for better results")
	diabetes_testset,db_btn = diabetesTestForm()
	diabetes_testset = np.array(diabetes_testset)
	diabetes_testset = diabetes_testset.reshape(-1,7)
	diabetes_res = do_diabetes_test(diabetes_testset)
	if db_btn:
		if diabetes_res == 0:
			st.success(f'Congrats {st.session_state.name},\n You are not diagnosed with diabetes')
		if diabetes_res==1:
			st.error(f'Hi {st.session_state.name},\nYou are diagnosed with diabetes.\nPlease consult a doctor.')
