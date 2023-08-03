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

# ... (rest of the code remains the same)

def plot_crypto_balances_with_prices(balances, prices):
    # Convert the balances to float and sort by highest amount
    sorted_balances = {currency: float(amount) for currency, amount in balances.items() if is_numeric(amount)}
    sorted_balances = {k: v for k, v in sorted(sorted_balances.items(), key=lambda item: item[1], reverse=True)}

    # Convert the balances to USD value using the prices
    balances_in_usd = {currency: amount * prices[currency] for currency, amount in sorted_balances.items()}

    # Create a bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(balances_in_usd.keys(), balances_in_usd.values(), color='blue')
    plt.xlabel('Cryptocurrency')
    plt.ylabel('USD Value')
    plt.title('Crypto Account Balances in USD')
    plt.xticks(rotation=45)

    # Show the plot
    plt.tight_layout()
    st.pyplot(plt)

def is_numeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    # ... (rest of the code remains the same)

    # Display the sorted balances as a table
    st.table(sorted_balances)

    # Plot the crypto balances in USD
    plot_crypto_balances_with_prices(sorted_balances, crypto_prices)
