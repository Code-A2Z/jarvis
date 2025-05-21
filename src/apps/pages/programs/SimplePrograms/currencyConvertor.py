import streamlit as st
import requests

def get_exchange_rates():
  url = "https://api.frankfurter.app/currencies"
  response = requests.get(url)
  if response.status_code == 200:
    return response.json()
  else:
    return {}

def convert_currency(amount, from_currency, to_currency):
  url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
  response = requests.get(url)
  if response.status_code == 200:
    return response.json()
  else:
    return {}

def currencyConvertor():
  currencies = get_exchange_rates()
  if currencies:
    col1, col2 = st.columns(2)
    with col1:
      from_currency = st.selectbox("From currency", options=currencies.keys())
    with col2:
      to_currency = st.selectbox("To currency", options=currencies.keys())
    amount = st.number_input("Enter amount", min_value=0.0, format="%.2f")

    if st.button("Convert"):
      conversion_result = convert_currency(amount, from_currency, to_currency)
      if conversion_result:
        rate = conversion_result["rates"][to_currency]
        st.success(f"{amount} {from_currency} = {rate} {to_currency}", icon="✅")
      else:
        st.error("Conversion failed. Please try again.", icon="🚨")
  else:
    st.error("Failed to load currency data. Please try again later.", icon="🚨")
