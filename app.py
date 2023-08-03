import os
import streamlit as st
import requests
import urllib.parse
import hashlib
import hmac
import base64
import time
import pandas as pd
import plotly.graph_objects as go

# Read Kraken API key and secret stored in environment variables
api_url = "https://api.kraken.com"
api_key = os.environ['API_KEY_KRAKEN']
api_sec = os.environ['API_SEC_KRAKEN']

# Read the contents of the README.md file
with open('README.md', 'r') as file:
    readme_text = file.read()

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

def get_crypto_balances():
    # Construct the request and print the result
    resp = kraken_request('/0/private/Balance', {
        "nonce": str(int(1000*time.time()))
    }, api_key, api_sec)

    # Convert the response JSON to a Python dictionary
    data = resp.json()

    # Get the balances from the 'result' field in the response
    balances = data['result']
    return balances

if __name__ == "__main__":
    # Set page title and favicon
    st.set_page_config(page_title="Kraken Crypto Balances", page_icon=":moneybag:")

    st.markdown(readme_text, unsafe_allow_html=True)

    # Fetch cryptocurrency balances from Kraken
    balances = get_crypto_balances()

    # Create a summary above the chart and datatable
    total_balance = sum(float(balance) for balance in balances.values())
    st.write(f"Total Balance: ${total_balance:.2f}")

    # Create a DataFrame to display the cryptocurrency balances
    df = pd.DataFrame({'Cryptocurrency': list(balances.keys()), 'Balance': list(balances.values())})

    # Create two columns for chart and datatable side by side
    col1, col2 = st.columns(2)

    # Plot the pie chart in the first column
    fig = go.Figure(data=go.Pie(labels=df['Cryptocurrency'], values=df['Balance']))
    fig.update_layout(title='Crypto Account Balances', showlegend=False)
    col1.plotly_chart(fig)

    # Display the data table in the second column
    col2.dataframe(df)
