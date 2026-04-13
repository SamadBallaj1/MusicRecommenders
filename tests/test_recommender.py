from src.recommender import Song, UserProfile, Recommender, load_songs, score_song, recommend_songs
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_load_songs_returns_correct_count():
    songs = load_songs(os.path.join(BASE_DIR, "data", "songs.csv"))
    assert len(songs) >= 15


def test_load_songs_converts_types():
    songs = load_songs(os.path.join(BASE_DIR, "data", "songs.csv"))
    song = songs[0]
    assert isinstance(song["energy"], float)
    assert isinstance(song["popularity"], int)
    assert isinstance(song["id"], int)


def test_score_song_returns_score_and_reasons():
    song = {"genre": "pop", "mood": "happy", "energy": 0.8, "danceability": 0.7, "valence": 0.7, "acousticness": 0.2, "popularity": 70}
    user = {"genre": "pop", "mood": "happy", "energy": 0.8}
    score, reasons = score_song(user, song)
    assert isinstance(score, float)
    assert score > 0
    assert len(reasons) > 0


def test_genre_match_adds_points():
    song = {"genre": "pop", "mood": "sad", "energy": 0.5, "popularity": 50}
    user_match = {"genre": "pop", "energy": 0.5}
    user_no_match = {"genre": "rock", "energy": 0.5}
    score_match, _ = score_song(user_match, song)
    score_no, _ = score_song(user_no_match, song)
    assert score_match > score_no


def test_different_profiles_give_different_results():
    songs = load_songs(os.path.join(BASE_DIR, "data", "songs.csv"))
    pop_user = {"genre": "pop", "mood": "happy", "energy": 0.85}
    lofi_user = {"genre": "lofi", "mood": "chill", "energy": 0.35}
    pop_recs = recommend_songs(pop_user, songs, k=3)
    lofi_recs = recommend_songs(lofi_user, songs, k=3)
    pop_titles = [r[0]["title"] for r in pop_recs]
    lofi_titles = [r[0]["title"] for r in lofi_recs]
    assert pop_titles != lofi_titles


def test_recommend_songs_returns_k_results():
    songs = load_songs(os.path.join(BASE_DIR, "data", "songs.csv"))
    user = {"genre": "pop", "mood": "happy", "energy": 0.8}
    recs = recommend_songs(user, songs, k=3)
    assert len(recs) == 3


def test_recommend_songs_sorted_descending():
    songs = load_songs(os.path.join(BASE_DIR, "data", "songs.csv"))
    user = {"genre": "pop", "mood": "happy", "energy": 0.8}
    recs = recommend_songs(user, songs, k=5)
    scores = [r[1] for r in recs]
    assert scores == sorted(scores, reverse=True)


def test_diversity_changes_results():
    songs = load_songs(os.path.join(BASE_DIR, "data", "songs.csv"))
    user = {"genre": "pop", "mood": "happy", "energy": 0.8}
    normal = recommend_songs(user, songs, k=5, diversity=False)
    diverse = recommend_songs(user, songs, k=5, diversity=True)
    normal_titles = [r[0]["title"] for r in normal]
    diverse_titles = [r[0]["title"] for r in diverse]
    assert normal_titles != diverse_titles
