import streamlit as st

def update_display(value):
  st.session_state.memory["display"] = value

def on_button_click(button):
  memory = st.session_state.memory
  operators = ["add", "subtract", "multiply", "divide"]

  if button in "0123456789":
    if memory["awaiting_second_value"]:
      update_display(button)
      memory["awaiting_second_value"] = False
    elif memory["display"] == "0" or memory["display"] in operators:
        update_display(button)
    else:
        update_display(memory["display"] + button)

  elif button in operators:
    if memory["awaiting_second_value"]:
      memory["operator"] = button
      update_display(button)
      return

    if memory["first_value"] is None:
      memory["first_value"] = float(memory["display"])

    memory["operator"] = button
    memory["awaiting_second_value"] = True
    update_display(button)

  elif button == "clear":
    update_display("0")
    memory["operator"] = None
    memory["first_value"] = None
    memory["awaiting_second_value"] = False

  elif button == "=":
    try:
      if memory["operator"] and memory["first_value"] is not None:
        second_value = float(memory["display"])
        if memory["operator"] == "add":
          result = memory["first_value"] + second_value
        elif memory["operator"] == "subtract":
          result = memory["first_value"] - second_value
        elif memory["operator"] == "multiply":
          result = memory["first_value"] * second_value
        elif memory["operator"] == "divide":
          if second_value == 0:
            update_display("Error")
            return
          result = memory["first_value"] / second_value
        update_display(str(result))
        memory["operator"] = None
        memory["first_value"] = None
        memory["awaiting_second_value"] = False
    except:
      update_display("Error")

def calculator():
  if "memory" not in st.session_state:
    st.session_state.memory = {
      "display": "0",
      "operator": None,
      "first_value": None,
      "awaiting_second_value": False,
    }

  st.info("This is a simple calculator app which supports basic arithmetic operations.", icon="🧮")
  st.text_input("‎", value=st.session_state.memory["display"], key="display", disabled=True)

  buttons = [
    ["7", "8", "9", "divide"],
    ["4", "5", "6", "multiply"],
    ["1", "2", "3", "subtract"],
    ["0", "clear", "=", "add"],
  ]

  for row in buttons:
    cols = st.columns(4)
    for col, button in zip(cols, row):
      if col.button(button, key=f"btn_{button}", use_container_width=True):
          on_button_click(button)
          st.rerun()
