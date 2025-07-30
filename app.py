import streamlit as st
from spotify_auth import get_token
import spotipy
import sqlite3

def init_db():
    conn = sqlite3.connect('swiper.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 spotify_id TEXT PRIMARY KEY,
                 display_name TEXT,
                 email TEXT,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
              )''')

    ## Add other tables (playlists, songs, swipes) similarly
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Swiper", layout="wide")

# Get token (will stop execution if not authenticated)
token = get_token()


def fetch_playlists(token):
    sp = spotipy.Spotify(auth=token)
    playlists = sp.current_user_playlists()

    # Simple display
    st.write("## Your Playlists")
    for playlist in playlists['items']:
        st.write(f"- {playlist['name']} ({playlist['tracks']['total']} tracks)")

    return playlists



if token:
    sp = spotipy.Spotify(auth=token)
    user = sp.me()

    st.success(f"✅ Logged in as {user['display_name']}")

    try:
        fetch_playlists(token)
    except Exception as e:
        st.error(f"Error loading playlists: {str(e)}")

    st.balloons()

    # Your app content goes here
    st.write("Authentication successful! Add your app content here.")
