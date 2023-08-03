import os
import streamlit as st
import requests
import urllib.parse
import hashlib
import hmac
import base64
import time
import matplotlib.pyplot as plt

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

def plot_crypto_balances(balances):
    # Convert the balances to float
    balances = {currency: float(amount) for currency, amount in balances.items()}

    # Create a bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(balances.keys(), balances.values(), color='blue')
    plt.xlabel('Cryptocurrency')
    plt.ylabel('Balance')
    plt.title('Crypto Account Balances')
    plt.xticks(rotation=45)

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

    # Initialize Streamlit app
    st.title("Crypto Account Balances")
    st.subheader("Your current account balances in Kraken:")

    # Display the balances as a table
    st.table(balances)

    # Plot the crypto balances
    plot_crypto_balances(balances)
