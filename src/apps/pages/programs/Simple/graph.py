import numpy as np
import plotly.graph_objs as go
import streamlit as st


def graph():
  functions = ["Linear", "Quadratic", "Sine", "Cosine", "Exponential", "Logarithmic", "Polynomial"]
  function_type = st.selectbox("Function Type", functions)

  if function_type == "Linear":
    a = st.number_input("Coefficient a", value=1.0)
    b = st.number_input("Coefficient b", value=0.0)
    function = lambda x: a * x + b  # noqa: E731
  elif function_type == "Quadratic":
    a = st.number_input("Coefficient a", value=1.0)
    b = st.number_input("Coefficient b", value=0.0)
    c = st.number_input("Coefficient c", value=0.0)
    function = lambda x: a * x**2 + b * x + c  # noqa: E731
  elif function_type == "Sine":
    amplitude = st.number_input("Amplitude", value=1.0)
    frequency = st.number_input("Frequency", value=1.0)
    function = lambda x: amplitude * np.sin(frequency * x)  # noqa: E731
  elif function_type == "Cosine":
    amplitude = st.number_input("Amplitude", value=1.0)
    frequency = st.number_input("Frequency", value=1.0)
    function = lambda x: amplitude * np.cos(frequency * x)  # noqa: E731
  elif function_type == "Exponential":
    base = st.number_input("Base", value=np.e)
    coefficient = st.number_input("Coefficient", value=1.0)
    function = lambda x: coefficient * (base**x)  # noqa: E731
  elif function_type == "Logarithmic":
    base = st.number_input("Base", value=np.e)
    coefficient = st.number_input("Coefficient", value=1.0)
    function = lambda x: coefficient * np.log(x) / np.log(base)  # noqa: E731
  elif function_type == "Polynomial":
    degree = st.number_input("Degree", value=3, min_value=1)
    coefficients = [st.number_input(f"Coefficient of x^{i}", value=1.0) for i in range(degree + 1)]
    function = lambda x: sum(c * x**i for i, c in enumerate(coefficients))  # noqa: E731

  x_min = st.number_input("x-min", value=-10.0)
  x_max = st.number_input("x-max", value=10.0)
  x_values = np.linspace(x_min, x_max, 400)

  try:
    y_values = function(x_values)
    valid_input = True
  except ValueError as e:
    st.error(f"Error in function evaluation: {e}")
    valid_input = False

  if valid_input:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode="lines", name=function_type))
    fig.update_layout(title=f"{function_type} Function", xaxis_title="x", yaxis_title="f(x)", template="plotly_dark")
    st.plotly_chart(fig)
