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


def main() -> None:
    songs = load_songs(os.path.join(BASE_DIR, "data", "songs.csv"))
    print(f"Loaded {len(songs)} songs\n")

    # Default profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "danceability": 0.8, "valence": 0.8, "likes_acoustic": False}

    recs = recommend_songs(user_prefs, songs, k=5)
    print_recommendations("Top 5 for Pop/Happy listener", recs)


if __name__ == "__main__":
    main()
