import streamlit as st
import webbrowser
import requests
import datetime
import os

from src.helpers.displayInstructions import showInstructions
from src.helpers.checkKeyExist import isKeyExist

api_guide = """### How to get your API Key:
1. Visit [api.nasa.gov](https://api.nasa.gov/).
2. Sign up for a free account.
3. Generate an API key from your account dashboard.
4. Enter the API key in the input field.
"""

def SpaceNews(NASA_API_KEY):
  date = st.date_input("What day would you like to know ?", max_value=datetime.date.today())
  URL = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
  params = {'date': str(date)}
  data = requests.get(URL, params=params).json()

  if 'code' in data and data['code'] == 400:
    st.error(data['msg'], icon='🚨')
    st.stop()

  title = data['title']
  explanation = data['explanation']
  url = data['url']
  media_type = data['media_type']

  hd_url, copyright = "", ""
  if 'hdurl' in data:
    hd_url = data['hdurl']
  if 'copyright' in data:
    copyright = data['copyright']

  st.markdown(f"##### {title} - {copyright}")
  if media_type == 'image':
    if hd_url:
      st.image(hd_url, caption=data['date'])
    else:
      st.image(url, caption=data['date'])
  elif media_type == 'video':
    st.video(url)

  st.write(explanation)

def MarsImage(NASA_API_KEY):
  date = st.date_input("What day would you like to know ?", min_value=datetime.date(2012, 8, 16), max_value=datetime.date(2024, 1, 21))
  url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={date}&api_key={NASA_API_KEY}"
  data = requests.get(url).json()
  photos = data['photos'][0:]
  try:
    for index, photo in enumerate(photos):
      camera_name = photo['camera']['full_name']
      date_of_photo = photo['earth_date']
      img_url = photo['img_src']
      st.image(img_url, caption=f"Camera Name : {camera_name} | Date : {date_of_photo}")
  except:
	  st.error("No data found for the selected date!", icon="🚨")

def Asteroids(NASA_API_KEY):
  col1, col2 = st.columns(2)
  with col1:
    start_date = st.date_input("Starting Date", value=datetime.date.today()-datetime.timedelta(days=1))
  with col2:
    end_date = st.date_input("Ending Date")

  if start_date > end_date:
    st.error("Starting Date should be less than Ending Date!", icon="🚨")
    st.stop()
  if (end_date - start_date).days > 7:
    st.error("Difference between 2 dates should be only 7 days!", icon="🚨")
    st.stop()

  url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={NASA_API_KEY}"
  data = requests.get(url).json()

  try:
    totalAstro = data['element_count']
    neo = data['near_earth_objects']

    st.markdown(f"##### `Total asteroids between {start_date} and {end_date} are {totalAstro}`")
    st.divider()
    for dateData in neo:
      for index, body in enumerate(neo[dateData]):
        id = body['id']
        name = body['name']
        absolute = body['absolute_magnitude_h']
        nasa_jpl_url = body['nasa_jpl_url']
        is_potentially_hazardous = body['is_potentially_hazardous_asteroid']
        is_seneitive = body['is_sentry_object']
        estimated_diameter = body['estimated_diameter']['kilometers']['estimated_diameter_max']
        close_approach_data = body['close_approach_data'][0]

        colx, coly, colz = st.columns(3)
        with colx:
          st.write(f"###### `{dateData}`")
        with coly:
          st.write(f"###### Data of Asteroid {index+1}")
        with colz:
          st.write(f"###### `Asteroid ID : {id}`")

        col1, col2, col3 = st.columns(3)
        with col1:
          st.write(f"Name : {name}")
        with col2:
          st.write(f"Absolute Magnitude : {absolute}")
        with col3:
          if is_potentially_hazardous:
            st.write(f"`Potentially Hazardous : {is_potentially_hazardous}`")

        col4, col5, col6 = st.columns(3)
        with col4:
          st.write(f"Estimated Diameter : {estimated_diameter} km")
        with col5:
          st.write(f"Close Approach Date : {close_approach_data['close_approach_date_full']}")
        with col6:
          st.write(f"Velocity : {close_approach_data['relative_velocity']['kilometers_per_hour']} km/hr")

        col7, col8, col9 = st.columns(3)
        with col7:
          st.write(f"Miss Distance : {close_approach_data['miss_distance']['kilometers']} km")
        with col8:
          st.write(f"Orbiting Body : {close_approach_data['orbiting_body']}")
        with col9:
          if is_seneitive:
            st.write(f"`Sentry Object : {is_seneitive}`")

        if st.button("More Info", key=id):
          webbrowser.open_new_tab(nasa_jpl_url)
        st.divider()
  except:
    st.error("No data found for the selected date!", icon="🚨")

@st.cache_data(ttl=86400)
def fetchSolarBodiesData():
  url = "https://api.le-systeme-solaire.net/rest/bodies/"
  data = requests.get(url).json()
  return data

def SolarBodies():
  try:
    data = fetchSolarBodiesData()
    solarBodies = [body['englishName'] for body in data['bodies']]
    bodies = data['bodies']
    
    st.markdown(f"### 🌌 Solar System Explorer")
    st.markdown(f"##### `Number of bodies in the Solar System: {len(bodies)}`")
    
    body = st.selectbox("🔭 Select a Celestial Body", [None] + solarBodies)
    if body is None:
      st.stop()
    body = body.replace(" ", "-")
    
    url2 = f"https://api.le-systeme-solaire.net/rest/bodies/{body.lower()}"
    url3 = f"https://images-api.nasa.gov/search?q={body.lower()}"
    data2 = requests.get(url2).json()
    data3 = requests.get(url3).json()
    
    st.markdown(f"## 🪐 Data of {body}")
    if data3['collection']['items']:
      st.image(data3['collection']['items'][0]['links'][0]['href'], caption=f"{body}")
    
    col1, col2 = st.columns(2)
    with col1:
      if 'moons' in data2 and data2['moons']:
        st.markdown(f"**No. of Moons**: {len(data2.get('moons'))}")
      st.markdown(f"**Semi-Major Axis**: {data2.get('semimajorAxis', 'Data not available')} km")
      st.markdown(f"**Perihelion**: {data2.get('perihelion', 'Data not available')} km")
      st.markdown(f"**Aphelion**: {data2.get('aphelion', 'Data not available')} km")
      st.markdown(f"**Eccentricity**: {data2.get('eccentricity', 'Data not available')}")
      st.markdown(f"**Inclination**: {data2.get('inclination', 'Data not available')}°")

    with col2:
      mass = data2.get('mass')
      if mass:
        st.markdown(f"**Mass**: {mass.get('massValue', 'Data not available')} × 10^{mass.get('massExponent', '')} kg")
      else:
        st.markdown("**Mass**: Data not available")

      vol = data2.get('vol')
      if vol:
        st.markdown(f"**Volume**: {vol.get('volValue', 'Data not available')} × 10^{vol.get('volExponent', '')} km³")
      else:
        st.markdown("**Volume**: Data not available")

      st.markdown(f"**Density**: {data2.get('density', 'Data not available')} g/cm³")
      st.markdown(f"**Gravity**: {data2.get('gravity', 'Data not available')} m/s²")
      st.markdown(f"**Mean Radius**: {data2.get('meanRadius', 'Data not available')} km")

    if data2.get('moons'):
      st.markdown("---")
      st.markdown("### 🌕 Names of all Moons")
      moons = [moon.get('moon', 'Data not available') for moon in data2.get('moons')]
      st.markdown(" | ".join(moons))

    with st.expander("🔍 More Details"):
      st.markdown(f"**Equatorial Radius**: {data2.get('equaRadius', 'Data not available')} km")
      st.markdown(f"**Polar Radius**: {data2.get('polarRadius', 'Data not available')} km")
      st.markdown(f"**Escape Velocity**: {data2.get('escape', 'Data not available')} m/s")
      st.markdown(f"**Flattening**: {data2.get('flattening', 'Data not available')}")
      st.markdown(f"**Dimension**: {data2.get('dimension', 'Data not available')}")
      st.markdown(f"**Surface Area**: {data2.get('sideralOrbit', 'Data not available')} km²")
      st.markdown(f"**Surface Gravity**: {data2.get('sideralRotation', 'Data not available')} m/s²")
    
      around_planet = data2.get('aroundPlanet')
      if around_planet:
        st.markdown(f"**Orbits Around**: {around_planet.get('planet', 'Data not available')}")
      else:
        st.markdown("**Orbits Around**: Data not available")
      
      st.markdown(f"**Discovered By**: {data2.get('discoveredBy', 'Data not available')}")
      st.markdown(f"**Discovery Date**: {data2.get('discoveryDate', 'Data not available')}")
      st.markdown(f"**Alternative Name**: {data2.get('alternativeName', 'Data not available')}")
      st.markdown(f"**Average Temperature**: {data2.get('avgTemp', 'Data not available')} K")
      st.markdown(f"**Body Type**: {data2.get('bodyType', 'Data not available')}")

  except Exception as e:
    st.error(f"Error: {str(e)}. No data found for the selected body.")

def exploreAntariksa():
  exists = isKeyExist("NASA_API_KEY", folder="api_key")
  if not exists["NASA_API_KEY"]:
    showInstructions(markdown_text=api_guide, fields="NASA_API_KEY")
    st.stop()

  choice = st.selectbox("What Would You Like To Know?", [None, "Space News", "Mars Image", "Asteroids", "Solar Bodies"])
  NASA_API_KEY = (os.environ.get("NASA_API_KEY", "") or st.secrets['api_key']["NASA_API_KEY"])

  if choice == "Space News":
    SpaceNews(NASA_API_KEY)
  elif choice == "Mars Image":
    MarsImage(NASA_API_KEY)
  elif choice == "Asteroids":
    Asteroids(NASA_API_KEY)
  elif choice == "Solar Bodies":
    SolarBodies()
