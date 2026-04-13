import streamlit as st
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from recommender import load_songs, recommend_songs, RANKING_MODES

st.set_page_config(page_title="Music Recommender", page_icon="🎵", layout="centered")
st.title("🎵 Music Recommender")

songs = load_songs(os.path.join(os.path.dirname(__file__), "data", "songs.csv"))

st.subheader("Your Taste Profile")

col1, col2 = st.columns(2)
with col1:
    genre = st.selectbox("Favorite genre", sorted(set(s["genre"] for s in songs)))
    mood = st.selectbox("Favorite mood", sorted(set(s["mood"] for s in songs)))
    mood_tag = st.selectbox("Mood tag (optional)", [""] + sorted(set(s["mood_tag"] for s in songs)))
with col2:
    energy = st.slider("Target energy", 0.0, 1.0, 0.7)
    danceability = st.slider("Danceability", 0.0, 1.0, 0.7)
    valence = st.slider("Valence (happiness)", 0.0, 1.0, 0.7)

likes_acoustic = st.checkbox("I like acoustic songs")

st.divider()

st.subheader("Recommendation Settings")

col3, col4 = st.columns(2)
with col3:
    mode = st.selectbox("Ranking mode", list(RANKING_MODES.keys()))
with col4:
    k = st.slider("Number of results", 1, 10, 5)

diversity = st.checkbox("Enable diversity (penalize repeat artists/genres)")

if st.button("Get Recommendations"):
    user_prefs = {
        "genre": genre,
        "mood": mood,
        "energy": energy,
        "danceability": danceability,
        "valence": valence,
        "likes_acoustic": likes_acoustic,
    }
    if mood_tag:
        user_prefs["mood_tag"] = mood_tag

    recs = recommend_songs(user_prefs, songs, k=k, mode=mode, diversity=diversity)

    st.subheader("Your Recommendations")
    for song, score, explanation in recs:
        with st.container():
            st.markdown(f"**{song['title']}** by {song['artist']} ({song['genre']})")
            st.markdown(f"Score: **{score:.2f}**")
            st.caption(explanation)
            st.divider()
