import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
from dotenv import load_dotenv
import sqlite3

load_dotenv()


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URL"),
        scope="user-library-read playlist-read-private",
        cache_path=".spotify_cache",
        show_dialog=True
    )


def get_token():
    # Only create auth flow once
    if 'sp_oauth' not in st.session_state:
        st.session_state.sp_oauth = create_spotify_oauth()

    # Check for existing valid token
    if 'spotify_token' in st.session_state:
        return st.session_state.spotify_token

    # Handle callback
    if st.query_params.get("code"):
        token_info = st.session_state.sp_oauth.get_access_token(st.query_params["code"])
        st.session_state.spotify_token = token_info['access_token']

        sp = spotipy.Spotify(auth=st.session_state.spotify_token)
        user = sp.me()

        conn = sqlite3.connect('swiper.db')
        c = conn.cursor()
        c.execute('''INSERT OR IGNORE INTO users 
                             (spotify_id, display_name, email) 
                             VALUES (?, ?, ?)''',
                  (user['id'], user.get('display_name', ''), user.get('email', '')))
        conn.commit()
        conn.close()

        st.query_params.clear()  # Clear the code
        return st.session_state.spotify_token

    # Show login button if no token exists
    if 'spotify_token' not in st.session_state:
        auth_url = st.session_state.sp_oauth.get_authorize_url()
        st.markdown(f"""
        <a href="{auth_url}">
            <button style="background:#1DB954;color:white;border:none;padding:10px 20px;border-radius:5px;">
                Login with Spotify
            </button>
        </a>
        """, unsafe_allow_html=True)
        st.stop()  # Critical - stops script execution

    return None