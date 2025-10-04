import bs4
import plotly.graph_objs as go
import requests
import streamlit as st


def getCountries():
  url = "https://www.worldometers.info/coronavirus/"
  result = requests.get(url)
  soups = bs4.BeautifulSoup(result.text, "html.parser")
  country_links = soups.find_all("a", class_="mt_a")
  countries = {}
  for link in country_links:
    countries[link.text.strip()] = link["href"].split("/")[-2]
  return countries


def getDetails(country):
  url = f"https://www.worldometers.info/coronavirus/country/{country}/"
  result = requests.get(url)
  soups = bs4.BeautifulSoup(result.text, "html.parser")
  cases = soups.find_all("div", class_="maincounter-number")
  case_numbers = [case.text.strip() for case in cases]

  graph = soups.find_all("div", class_="graph_row")
  graph = graph[1]
  categories = graph.find("script").text.split("categories:")[1].split("]")[0].split('","')
  categories = [category.replace('"', "") for category in categories]
  categories = [category.replace("[", "") for category in categories]
  categories = [category.replace("]", "") for category in categories]
  data = graph.find("script").text.split("data:")[1].split("]")[0].split(",")

  return case_numbers, (categories, data)


def plotGraph(categories, data, country):
  fig = go.Figure()
  fig.add_trace(go.Bar(x=categories, y=data, name="Daily Cases"))

  fig.update_layout(
    title=f"Daily New Cases in {country}", xaxis_title="Date", yaxis_title="Coronovirus Daily Cases", xaxis=dict(tickmode="array"), showlegend=True
  )
  return fig


def coronaVirus():
  countries = getCountries()
  country = st.selectbox("Select Country", [None] + list(countries.keys()))

  if country is not None:
    case_numbers, graph_data = getDetails(countries[country])

    col1, col2, col3 = st.columns(3)
    with col1:
      st.write("Total Cases")
      st.write(case_numbers[0])
    with col2:
      st.write("Total Deaths")
      st.write(case_numbers[1])
    with col3:
      st.write("Total Recovered")
      st.write(case_numbers[2])

    if graph_data:
      categories, data = graph_data
      fig = plotGraph(categories, data, country)
      st.plotly_chart(fig)
