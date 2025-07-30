import streamlit as st
from spotify_auth import get_token
import spotipy

st.set_page_config(page_title="Tinder for Songs", layout="wide")

# Get token (will stop execution if not authenticated)
token = get_token()

if token:
    sp = spotipy.Spotify(auth=token)
    user = sp.me()

    st.success(f"✅ Logged in as {user['display_name']}")
    st.balloons()

    # Your app content goes here
    st.write("Authentication successful! Add your app content here.")