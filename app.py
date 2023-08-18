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
    page_icon="💰",  # Replace with your desired emoji
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

# Function to plot crypto balances
def plot_crypto_balances(balances):
    sorted_balances = {k: v for k, v in sorted(balances.items(), key=lambda item: float(item[1]), reverse=True)}
    crypto_names = list(sorted_balances.keys())
    crypto_amounts = list(sorted_balances.values())

    # Create an interactive pie chart using Plotly
    fig = go.Figure(data=go.Pie(labels=crypto_names, values=crypto_amounts))
    fig.update_layout(title='Crypto Account Balances')
    st.plotly_chart(fig)

    # Create a DataFrame to display the cryptocurrency balances
    df = pd.DataFrame({'Cryptocurrency': crypto_names, 'Balance': crypto_amounts})
    st.dataframe(df)

if __name__ == "__main__":
    # Construct the Kraken API request and get the balances
    resp = kraken_request('/0/private/Balance', {
        "nonce": str(int(1000*time.time()))
    }, api_key, api_sec)

    # Convert the response JSON to a Python dictionary
    data = resp.json()

    # Get the balances from the 'result' field in the response
    balances = data['result']

    # Show the README content
    readme_expander = st.beta_expander("README Documentation")
    with readme_expander:
        st.markdown(readme_text)

    st.write("")
    st.write("")

    # Plot the crypto balances
    plot_crypto_balances(balances)

    # Read coin types from CSV file
    coin_types_df = pd.read_csv('kraken_lookup.csv')

    # Merge coin types with balances data
    merged_data = pd.merge(coin_types_df, pd.DataFrame(balances.items(), columns=['kraken_name', 'Balance']), on='kraken_name', how='right')

    st.write("")
    st.write("## Breakdown by Coin Type")

    # Create a bar chart showing balances by coin type
    type_balances = merged_data.groupby('type')['Balance'].sum()
    st.bar_chart(type_balances)

    # Show metrics by coin type
    st.write("### Metrics by Coin Type")
    st.dataframe(type_balances)

    # Calculate total balance
    total_balance = type_balances.sum()
    st.write("### Total Balance")
    st.write(total_balance)
