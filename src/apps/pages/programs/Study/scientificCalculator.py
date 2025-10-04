import math

import streamlit as st

MATH_CONTEXT = {
  "sin": math.sin,
  "cos": math.cos,
  "tan": math.tan,
  "log": math.log10,
  "ln": math.log,
  "sqrt": math.sqrt,
  "pow": math.pow,
  "pi": math.pi,
  "e": math.e,
  "factorial": math.factorial,
  "sinh": math.sinh,
  "cosh": math.cosh,
  "tanh": math.tanh,
}


def evaluate_expression(expr):
  try:
    result = eval(expr, {"__builtins__": None}, MATH_CONTEXT)
    st.success(f"Result: {result}", icon="✅")
  except Exception as e:
    st.error(f"Error: {str(e)}", icon="🚫")


def scientificCalculator():
  st.toast("""
  - **Basic Operators**: `+`, `-`, `*`, `/`
  - **Trigonometric Functions**: `sin(x)`, `cos(x)`, `tan(x)` (input in radians)
  - **Logarithmic Functions**: `log(x)` (base 10), `ln(x)` (natural log)
  - **Square Root**: `sqrt(x)`
  - **Exponentiation**: `pow(x, y)` or `x**y`
  - **Factorial**: `factorial(x)`
  - **Hyperbolic Functions**: `sinh(x)`, `cosh(x)`, `tanh(x)`
  - **Constants**: `pi`, `e`
  """)

  expression = st.text_input("Mathematical expression", placeholder="e.g., sin(30) + log(10)")
  if st.button("Evaluate"):
    evaluate_expression(expression)
