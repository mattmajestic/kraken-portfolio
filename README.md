# Kraken API Portfolio Tracker with Supabase 🔒

This Streamlit app is a demo of using the Kraken API within a Streamlit app to keep track of your cryptocurrency and fiat currency positions with a backend of `supabase` It fetches your account balances from the Kraken exchange and presents them in an interactive scatter plot along with the current price of each cryptocurrency in USD.

## Overview 📊 

The Kraken API Portfolio Tracker is a simple app that allows you to visualize your cryptocurrency holdings and their respective values. The app communicates with the Kraken API to fetch your account balances, which are then displayed in an interactive plots.

## Supabase Integration 🚄

The backend of this app is with `supabase`. Create a free account, setup an org & table then retreive your API credentials from `supabase`.

## How to Run the App

1. Set up your Kraken API key and secret in your environment variables (`API_KEY_KRAKEN` and `API_SEC_KRAKEN`).
2. Set up your Supabase API Credentials `SUPABASE_URL = os.getenv("SUPABASE_URL")` & `SUPABASE_KEY = os.getenv("SUPABASE_KEY")`
3. Clone the Code with `git clone https://github.dev/mattmajestic/kraken-portfolio``
4. Run the Streamlit app using the following command `streamlit run app.py`