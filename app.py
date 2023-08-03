import os
import streamlit as st
import requests
import urllib.parse
import hashlib
import hmac
import base64
import time
import matplotlib.pyplot as plt

load_dotenv()

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
    params = {
        'ids': 'bitcoin,ethereum,ripple',
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=params)
    crypto_prices = response.json()
    return crypto_prices

def plot_crypto_balances_with_prices(balances, prices):
    sorted_balances = {k: v for k, v in sorted(balances.items(), key=lambda item: float(item[1]), reverse=True)}
    crypto_names = list(sorted_balances.keys())
    crypto_amounts = list(sorted_balances.values())
    crypto_prices = [prices[name.lower()]['usd'] for name in crypto_names]

    # Plot the crypto balances with their prices in USD
    plt.figure(figsize=(12, 6))
    plt.bar(crypto_names, crypto_amounts, color='blue')
    plt.xlabel('Cryptocurrency')
    plt.ylabel('Balance')
    plt.title('Crypto Account Balances')
    plt.xticks(rotation=45)

    # Add the prices as annotations on the bars
    for i in range(len(crypto_names)):
        plt.text(i, crypto_amounts[i], f"${crypto_prices[i]:.2f}", ha='center', va='bottom')

    # Show the plot
    plt.tight_layout()
    st.pyplot(plt)

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
