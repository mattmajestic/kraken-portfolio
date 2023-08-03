# Kraken API Portfolio Tracker

This Streamlit app is a demo of using the Kraken API within a Streamlit app to keep track of your cryptocurrency and fiat currency positions. It fetches your account balances from the Kraken exchange and presents them in an interactive scatter plot along with the current price of each cryptocurrency in USD.

## Overview

The Kraken API Portfolio Tracker is a simple app that allows you to visualize your cryptocurrency holdings and their respective values. The app communicates with the Kraken API to fetch your account balances, which are then displayed in an interactive scatter plot.

## How to Run the App

1. Make sure you have set up your Kraken API key and secret in your environment variables (`API_KEY_KRAKEN` and `API_SEC_KRAKEN`).
2. Clone https://github.dev/mattmajestic/kraken-portfolio
2. Run the Streamlit app using the following command:

```
git clone https://github.dev/mattmajestic/kraken-portfolio
streamlit run app.py
```