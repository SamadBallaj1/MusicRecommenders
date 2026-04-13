"""
Command line runner for the Music Recommender Simulation.
"""

import os

try:
    from recommender import load_songs, recommend_songs, RANKING_MODES
except ModuleNotFoundError:
    from src.recommender import load_songs, recommend_songs, RANKING_MODES

from tabulate import tabulate

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def print_recommendations(title, recs):
    """Prints recommendations in a formatted table."""
    print(f"\n{title}")
    print("=" * len(title))
    rows = []
    for song, score, explanation in recs:
        rows.append([
            song["title"],
            song["artist"],
            song["genre"],
            f"{score:.2f}",
            explanation
        ])
    print(tabulate(rows, headers=["Song", "Artist", "Genre", "Score", "Why"], tablefmt="grid"))


def run_profile(name, user_prefs, songs):
    """Runs a single user profile through all ranking modes."""
    print(f"\n{'*' * 60}")
    print(f"  Profile: {name}")
    print(f"  Prefs: {user_prefs}")
    print(f"{'*' * 60}")

    # Default balanced mode
    recs = recommend_songs(user_prefs, songs, k=5)
    print_recommendations(f"{name} - Balanced Mode", recs)

    # With diversity on
    recs_div = recommend_songs(user_prefs, songs, k=5, diversity=True)
    print_recommendations(f"{name} - Balanced + Diversity", recs_div)

    # Genre-first mode
    recs_genre = recommend_songs(user_prefs, songs, k=3, mode="genre-first")
    print_recommendations(f"{name} - Genre-First Mode (top 3)", recs_genre)

    # Mood-first mode
    recs_mood = recommend_songs(user_prefs, songs, k=3, mode="mood-first")
    print_recommendations(f"{name} - Mood-First Mode (top 3)", recs_mood)


def main() -> None:
    songs = load_songs(os.path.join(BASE_DIR, "data", "songs.csv"))
    print(f"Loaded {len(songs)} songs")

    profiles = {
        "High-Energy Pop Fan": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.85,
            "danceability": 0.8,
            "valence": 0.8,
            "likes_acoustic": False,
        },
        "Chill Lofi Listener": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "danceability": 0.55,
            "valence": 0.6,
            "likes_acoustic": True,
            "mood_tag": "peaceful",
        },
        "Intense Rock Lover": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
            "danceability": 0.65,
            "valence": 0.45,
            "likes_acoustic": False,
            "mood_tag": "aggressive",
        },
    }

    for name, prefs in profiles.items():
        run_profile(name, prefs, songs)

    print("\n" + "=" * 60)
    print("Done! Check the results above for each profile.")


if __name__ == "__main__":
    main()
