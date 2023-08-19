import os
import streamlit as st
import requests
import urllib.parse
import hashlib
import hmac
import base64
import time
import plotly.graph_objects as go
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Kraken Portfolio",
    page_icon="💰",
)

# Read the README file
with open('README.md', 'r') as file:
    readme_text = file.read()

# Read Kraken API key and secret stored in environment variables
api_url = "https://api.kraken.com"
api_key = os.environ['API_KEY_KRAKEN']
api_sec = os.environ['API_SEC_KRAKEN']

# Function to get Kraken signature
def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

# Function to make Kraken API request
def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req

if __name__ == "__main__":
    st.title("Kraken Portfolio App 💰")
    st.write("Below is an app to view my Kraken Portfolio. Expand the README Documentation below the Kraken Holdings")
    st.write("")
    st.write("")

    # Construct the Kraken API request and get the balances
    resp = kraken_request('/0/private/Balance', {
        "nonce": str(int(1000*time.time()))
    }, api_key, api_sec)

    # Convert the response JSON to a Python dictionary
    data = resp.json()

    # Get the balances from the 'result' field in the response
    balances = data['result']

    st.write("")
    st.write("")

    # Read coin types from CSV file
    coin_types_df = pd.read_csv('kraken_lookup.csv')

    # Merge coin types with balances data
    merged_data = pd.merge(pd.DataFrame(balances.items(), columns=['kraken_name', 'Balance']), coin_types_df, on='kraken_name', how='left')

    st.write("")
    st.write("## Portfolio Breakdown by Coin Type")

    # Fetch price data from Kraken API for all coins
    coin_names = merged_data['kraken_name'].tolist()
    coin_prices = {}

    for coin in coin_names:
        if coin != 'ZUSD':  # Exclude fiat
            pair = coin + 'USD'
            price_response = requests.get(f'https://api.kraken.com/0/public/Ticker?pair={pair}')
            price_data = price_response.json()
            if 'result' in price_data and pair in price_data['result']:
                coin_prices[coin] = float(price_data['result'][pair]['a'][0])

    # Create a dictionary to store balances by type
    type_balances = {}
    for _, row in merged_data.iterrows():
        coin_type = row['type'] if not pd.isnull(row['type']) else 'Unknown'  # Use 'Unknown' for missing types
        if coin_type not in type_balances:
            type_balances[coin_type] = 0
        balance_in_usd = float(row['Balance']) * coin_prices.get(row['kraken_name'], 0)  # Convert to USD
        type_balances[coin_type] += balance_in_usd

    # Create labels and values for the pie chart
    labels = list(type_balances.keys())
    values = list(type_balances.values())

    # Create an interactive pie chart using Plotly
    fig = go.Figure(data=go.Pie(labels=labels, values=values))
    fig.update_layout(title='Portfolio Breakdown by Coin Type (USD)')
    st.plotly_chart(fig)

    st.write("")
    st.write("## Portfolio Breakdown by Coin Type (USD Equivalent)")
    
    # Create a DataFrame to display balances by type
    df_type_balances = pd.DataFrame(type_balances.items(), columns=['Coin Type', 'USD Equivalent'])
    st.dataframe(df_type_balances)

    # Show the README content
    readme_expander = st.expander("README Documentation")
    with readme_expander:
        st.markdown(readme_text)
