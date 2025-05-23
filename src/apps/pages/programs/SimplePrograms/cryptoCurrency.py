import streamlit as st
import plotly.express as px
import requests

BASE_URL = "https://api.coingecko.com/api/v3"

def clipDecimal(number, precision=1):
  return round(float(number), precision)

def format_price_change(percentage_change):
  value = clipDecimal(percentage_change)
  if value > 0:
    return f"▲ {value}%"
  else:
    return f"🔻 {value}%"

def showTrendingAssets():
  response = requests.get(f"{BASE_URL}/search/trending")
  if response.status_code != 200:
    st.error("API call not successful. Please try again later.", icon="🚨")
    st.stop()

  data = response.json()
  asset_type = st.selectbox("Select an asset:", ["Cryptocurrency", "NFTs", "Categories"])
  st.divider()

  if asset_type == "Cryptocurrency":
    coins = data.get("coins", [])
    if coins:
      for i, c in enumerate(coins):
        coin = c["item"]
        with st.container():
          cols = st.columns([1, 3, 2, 2, 2, 2])
          cols[0].image(coin['thumb'], width=32)
          cols[1].markdown(f"**{coin['name']}** ({coin['symbol']})")
          cols[2].write(f"Rank: {coin['market_cap_rank']}")
          cols[3].write(f"Price: ${clipDecimal(coin['data']['price'],3)}")
          cols[4].markdown(format_price_change(coin['data']['price_change_percentage_24h']['usd']))
          cols[5].image(coin['data']['sparkline'], width=100)
          st.divider()
    else:
      st.info("No trending cryptocurrencies found.", icon="ℹ️")

  elif asset_type == "NFTs":
    nfts = data.get('nfts', [])
    if nfts:
      for i, nft in enumerate(nfts):
        with st.container():
          cols = st.columns([1, 3, 2, 2, 2, 2])
          cols[0].image(nft['thumb'], width=50)
          cols[1].markdown(f"**{nft['name']}** ({nft['symbol']})")
          cols[2].write(f"Floor Price: {nft['data']['floor_price']}")
          cols[3].markdown(format_price_change(nft['data']['floor_price_in_usd_24h_percentage_change']))
          cols[4].write(f"24h Volume: {nft['data']['h24_volume']}")
          cols[5].image(nft['data']['sparkline'], width=100)
          st.divider()
    else:
      st.info("No trending NFTs found.", icon="ℹ️")

  else:
    categories = data.get("categories", [])
    if categories:
      for i, cat in enumerate(categories):
        with st.container():
          cols = st.columns([3, 2, 2, 2, 2])
          cols[0].markdown(f"**{cat['name']}**")
          cols[1].write(f"Coins: {cat['coins_count']}")
          cols[2].markdown(format_price_change(cat['data']['market_cap_change_percentage_24h']['usd']))
          cols[3].write(f"Market Cap: ${cat['data']['market_cap']}")
          cols[4].image(cat['data']['sparkline'], width=100)
          st.divider()
    else:
      st.info("No trending categories found.", icon="ℹ️")

@st.cache_data(ttl=86400)
def getSupportedCurrencies():
  response = requests.get(f"{BASE_URL}/simple/supported_vs_currencies")
  if response.status_code == 200:
    return response.json()
  else:
    st.error("API call not successful. Please try again later.", icon="🚨")

@st.cache_data(ttl=86400)
def getSupportedCoins():
  response = requests.get(f"{BASE_URL}/coins/list")
  if response.status_code == 200:
    return [coin['id'] for coin in response.json()]
  else:
    st.error("API call not successful. Please try again later.", icon="🚨")

def searchCryptocurrency(query):
  response = requests.get(f"{BASE_URL}/search?query={query}")
  if response.status_code == 200:
    data = response.json()
    results = data['coins']
    if results:
      for row in range(0, len(results), 3):
        row_coins = results[row: row+3]
        cols = st.columns(len(row_coins))
        for col, coin in zip(cols, row_coins):
          with col:
            st.image(coin['large'])
            st.markdown(f"**{coin['name']}** ({coin['symbol']})")
            st.write(f"Market Cap Rank: {coin['market_cap_rank']}")
            st.divider()
    else:
      st.error("No results found.", icon="🚨")
  else:
    st.error("API call not successful. Please try again later.", icon="🚨")

def cryptoConversion(from_coin, to_coin):
  response = requests.get(f"{BASE_URL}/simple/price?ids={from_coin}&vs_currencies={to_coin}")
  if response.status_code == 200:
    data = response.json()
    price = data[from_coin][to_coin]
    st.success(f"**{from_coin.upper()} = {price:,.2f} {to_coin.upper()}**", icon="✅")
  else:
    st.error("API call not successful. Please try again later.", icon="🚨")

def showTopCryptocurrency():
  response = requests.get(f"{BASE_URL}/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10")
  if response.status_code == 200:
    data = response.json()
    st.divider()
    for coin in data:
      col1, col2 = st.columns([1, 3])
      with col1:
        st.image(coin['image'])
      with col2:
        st.subheader(f"{coin['name']} ({coin['symbol'].upper()})")
        st.write(f"**Current Price**: ${coin['current_price']:,.2f}")
        st.write(f"**Market Cap**: ${coin['market_cap']:,.0f}")
        st.write(f"**24h Price Change**: {format_price_change(coin['price_change_percentage_24h'])}")
        st.divider()
  else:
    st.error("API call not successful. Please try again later.", icon="🚨")

def showCryptoMarketOverview():
  response = requests.get(f"{BASE_URL}/global")
  if response.status_code == 200:
    data = response.json()
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
      st.metric(label="Active Cryptocurrencies", value=data['data']['active_cryptocurrencies'])
    with col2:
      st.metric(label="Ongoing ICOs", value=data['data']['ongoing_icos'])
    with col3:
      st.metric(label="Ended ICOs", value=data['data']['ended_icos'])
    with col4:
      st.metric(label="Markets", value=data['data']['markets'])

    st.info(f"Market Capitalization Change (24h) {format_price_change(data['data']['market_cap_change_percentage_24h_usd'])}", icon="ℹ️")

    coins = list(data['data']['total_volume'].keys())
    volume = list(data['data']['total_volume'].values())

    coin_volume_pairs = list(zip(coins, volume))
    top_10_coin_volume_pairs = sorted(coin_volume_pairs, key=lambda x: x[1], reverse=True)[:10]

    top_10_coins = [coin for coin, _ in top_10_coin_volume_pairs]
    top_10_volumes = [vol for _, vol in top_10_coin_volume_pairs]
    top_10_volume_percentages = [vol / sum(top_10_volumes) * 100 for vol in top_10_volumes]

    st.plotly_chart(px.pie(
      names=top_10_coins,
      values=top_10_volume_percentages,
      title="Cryptocurrency Volume Dominance",
      hole=0.3,
    ))
    st.plotly_chart(px.pie(
      names=[coin for coin in data['data']['market_cap_percentage']],
      values=[data['data']['market_cap_percentage'][coin] for coin in data['data']['market_cap_percentage']],
      title="Cryptocurrency Market Capitalization Dominance",
      hole=0.3,
    ))
  else:
    st.error("API call not successful. Please try again later.", icon="🚨")

def showCompanyHoldings():
  response = requests.get(f"{BASE_URL}/companies/public_treasury/bitcoin")
  if response.status_code == 200:
    data = response.json()
    st.divider()
    st.subheader("🅱️ Bitcoin (BTC) Holdings")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Holdings", value=data["total_holdings"])
    col2.metric(label="Total Value (USD)", value=f"${data['total_value_usd']:.2f}")
    col3.metric(label="Market Cap Dominance", value=f"{data['market_cap_dominance']:.2f}%")

    st.divider()
    st.subheader("🅱️ Companies Holding Bitcoin")
    st.dataframe(data["companies"])
  else:
    st.error("API call not successful. Please try again later.", icon="🚨")

def cryptoCurrency():
  options = [
    "Search Cryptocurrency",
    "Trending Assets",
    "Exchange Rates",
    "Top Cryptocurrency",
    "Crypto Global Market",
    "Companies Bitcoin Holdings"
  ]
  option = st.selectbox("Select an option", options=options)

  if option == "Search Cryptocurrency":
    query = st.text_input(f"Enter the coin name or symbol", placeholder="e.g. Bitcoin, BTC")
    if st.button("Search") and query:
      searchCryptocurrency(query)
  elif option == "Trending Assets":
    showTrendingAssets()

  elif option == "Exchange Rates":
    SUPPORTED_CURRENCIES = getSupportedCurrencies()
    SUPPORTED_COINS = getSupportedCoins()
    col1, col2 = st.columns(2)
    with col1:
      from_currency = st.selectbox("From currency", options=SUPPORTED_COINS)
    with col2:
      to_currency = st.selectbox("To currency", options=SUPPORTED_CURRENCIES)
    if st.button("Convert"):
      cryptoConversion(from_currency, to_currency)

  elif option == "Top Cryptocurrency":
    showTopCryptocurrency()
  elif option == "Crypto Global Market":
    showCryptoMarketOverview()
  else:
    showCompanyHoldings()
