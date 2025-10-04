import streamlit as st
from pint import UnitRegistry

UNIT_TYPES = {
  "Length": ["meter", "kilometer", "centimeter", "millimeter", "micrometer", "nanometer", "mile", "yard", "foot", "inch", "lightyear"],
  "Temperature": ["Celsius", "Kelvin", "Fahrenheit"],
  "Area": [
    "square meter",
    "square kilometer",
    "square centimeter",
    "square millimeter",
    "hectare",
    "square mile",
    "square yard",
    "square foot",
    "square inch",
    "acre",
  ],
  "Volume": [
    "cubic meter",
    "cubic kilometer",
    "cubic centimeter",
    "cubic millimeter",
    "liter",
    "milliliter",
    "gallon",
    "quart",
    "pint",
    "cup",
    "fluid ounce",
    "tablespoon",
    "teaspoon",
    "cubic mile",
    "cubic yard",
    "cubic foot",
    "cubic inch",
  ],
  "Weight": ["kilogram", "gram", "milligram", "pound", "ounce", "carat"],
  "Time": ["second", "millisecond", "microsecond", "nanosecond", "minute", "hour", "day", "week", "month", "year"],
}

UNIT_MAPPING = {"Celsius": "degree_Celsius", "Fahrenheit": "degree_Fahrenheit", "Kelvin": "kelvin"}


def convert_units(value, from_unit, to_unit):
  convertor = UnitRegistry().Quantity
  try:
    from_unit = UNIT_MAPPING.get(from_unit, from_unit)
    to_unit = UNIT_MAPPING.get(to_unit, to_unit)
    value = convertor(value, from_unit)
    result = value.to(to_unit)
    return result.magnitude, result.units
  except Exception as e:
    return None, str(e)


def unitsConvertor():
  col1, col2 = st.columns(2)
  with col1:
    value = st.number_input("Enter value", min_value=0.0, format="%.2f")
  with col2:
    unit_type = st.selectbox("Select unit type", options=list(UNIT_TYPES.keys()))

  col3, col4 = st.columns(2)
  with col3:
    from_unit = st.selectbox("From unit", options=UNIT_TYPES[unit_type])
  with col4:
    to_unit = st.selectbox("To unit", options=UNIT_TYPES[unit_type])

  if st.button("Convert"):
    result, error = convert_units(value, from_unit, to_unit)
    if result is not None:
      st.success(f"{value} {from_unit} = {result} {to_unit}", icon="✅")
    else:
      st.error(f"Conversion failed: {error}", icon="🚨")
