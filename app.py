import os
import streamlit as st
import requests
import urllib.parse
import hashlib
import hmac
import base64
import time
import plotly.graph_objects as go

# Read Kraken API key and secret stored in environment variables
api_url = "https://api.kraken.com"
api_key = os.environ['API_KEY_KRAKEN']
api_sec = os.environ['API_SEC_KRAKEN']

def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

# Attaches auth headers and returns results of a POST request
def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req

def get_crypto_prices():
    # Fetch cryptocurrency prices from CoinGecko API
    url = 'https://api.coingecko.com/api/v3/simple/price'
    kraken_to_coingecko_mapping = {
        'XXBT': 'bitcoin',
        'XETH': 'ethereum',
        'XXRP': 'ripple',
        # Add more mappings as needed for your specific coins
    }
    params = {
        'ids': ','.join(kraken_to_coingecko_mapping.values()),
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=params)
    crypto_prices = response.json()
    return crypto_prices


def plot_crypto_balances_with_prices(balances, prices):
    sorted_balances = {k: v for k, v in sorted(balances.items(), key=lambda item: float(item[1]), reverse=True)}
    crypto_names = list(sorted_balances.keys())
    crypto_amounts = list(sorted_balances.values())

    # Fetch cryptocurrency prices from CoinGecko
    crypto_prices = []
    for name in crypto_names:
        # Convert the currency name to lowercase
        name_lower = name.lower()
        # Check if the currency name exists in the prices dictionary
        if name_lower in prices:
            # Fetch the price in USD and append it to the list
            crypto_prices.append(prices[name_lower]['usd'])
        else:
            # If the currency name is not found, set the price to 0
            crypto_prices.append(0)

    # Create an interactive scatter plot using Plotly
    fig = go.Figure(data=go.Scatter(x=crypto_names, y=crypto_amounts, mode='markers', marker=dict(size=10, color=crypto_prices, colorscale='Viridis')))
    fig.update_layout(title='Crypto Account Balances', xaxis_title='Cryptocurrency', yaxis_title='Balance', showlegend=False)
    st.plotly_chart(fig)

    # Create a DataFrame to display the cryptocurrency balances and prices
    df = pd.DataFrame({'Cryptocurrency': crypto_names, 'Balance': crypto_amounts, 'Price (USD)': crypto_prices})
    st.dataframe(df)

if __name__ == "__main__":
    # Construct the request and print the result
    resp = kraken_request('/0/private/Balance', {
        "nonce": str(int(1000*time.time()))
    }, api_key, api_sec)

    # Convert the response JSON to a Python dictionary
    data = resp.json()

    # Get the balances from the 'result' field in the response
    balances = data['result']

    # Get cryptocurrency prices
    crypto_prices = get_crypto_prices()

    # Convert balances to USD and plot the crypto balances
    plot_crypto_balances_with_prices(balances, crypto_prices)
