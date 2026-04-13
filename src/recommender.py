from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int = 50
    release_decade: str = "2020s"
    mood_tag: str = ""
    instrumentalness: float = 0.0
    liveness: float = 0.0

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Scores a Song object against a UserProfile."""
        score = 0.0
        reasons = []

        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
            reasons.append("genre match (+2.0)")

        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.5
            reasons.append("mood match (+1.5)")

        energy_score = round(1.0 - abs(user.target_energy - song.energy), 2)
        score += energy_score
        reasons.append(f"energy closeness (+{energy_score})")

        dance_score = round(0.5 * (1.0 - abs(0.7 - song.danceability)), 2)
        score += dance_score
        reasons.append(f"danceability closeness (+{dance_score})")

        val_score = round(0.5 * (1.0 - abs(0.7 - song.valence)), 2)
        score += val_score
        reasons.append(f"valence closeness (+{val_score})")

        if user.likes_acoustic and song.acousticness > 0.6:
            score += 0.5
            reasons.append("acoustic preference (+0.5)")

        pop_score = round(0.3 * (song.popularity / 100), 2)
        score += pop_score
        reasons.append(f"popularity bonus (+{pop_score})")

        score = round(score, 2)
        return (score, reasons)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns top k songs sorted by score for the given user."""
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explains why a song was recommended for the given user."""
        _, reasons = self._score(user, song)
        return ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file and converts numeric fields."""
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            row["popularity"] = int(row["popularity"])
            row["instrumentalness"] = float(row["instrumentalness"])
            row["liveness"] = float(row["liveness"])
            songs.append(row)
    return songs

RANKING_MODES = {
    "balanced":       {"genre": 2.0, "mood": 1.5, "energy": 1.0, "danceability": 0.5, "valence": 0.5, "acoustic": 0.5, "popularity": 0.3, "mood_tag": 0.5},
    "genre-first":    {"genre": 4.0, "mood": 1.0, "energy": 0.5, "danceability": 0.3, "valence": 0.3, "acoustic": 0.3, "popularity": 0.2, "mood_tag": 0.3},
    "mood-first":     {"genre": 1.0, "mood": 4.0, "energy": 0.5, "danceability": 0.5, "valence": 0.8, "acoustic": 0.5, "popularity": 0.2, "mood_tag": 1.0},
    "energy-focused": {"genre": 1.0, "mood": 0.5, "energy": 3.0, "danceability": 1.0, "valence": 0.3, "acoustic": 0.2, "popularity": 0.2, "mood_tag": 0.2},
}

def score_song(user_prefs: Dict, song: Dict, mode: str = "balanced") -> Tuple[float, List[str]]:
    """Scores a single song against user preferences using the given ranking mode."""
    weights = RANKING_MODES.get(mode, RANKING_MODES["balanced"])
    score = 0.0
    reasons = []

    # Genre match
    if song.get("genre", "").lower() == user_prefs.get("genre", "").lower():
        pts = weights["genre"]
        score += pts
        reasons.append(f"genre match (+{pts})")

    # Mood match
    if song.get("mood", "").lower() == user_prefs.get("mood", "").lower():
        pts = weights["mood"]
        score += pts
        reasons.append(f"mood match (+{pts})")

    # Energy closeness
    if "energy" in user_prefs and "energy" in song:
        energy_diff = abs(user_prefs["energy"] - song["energy"])
        pts = round(weights["energy"] * (1.0 - energy_diff), 2)
        score += pts
        reasons.append(f"energy closeness (+{pts})")

    # Danceability closeness
    if "danceability" in user_prefs and "danceability" in song:
        dance_diff = abs(user_prefs["danceability"] - song["danceability"])
        pts = round(weights["danceability"] * (1.0 - dance_diff), 2)
        score += pts
        reasons.append(f"danceability closeness (+{pts})")

    # Valence closeness
    if "valence" in user_prefs and "valence" in song:
        val_diff = abs(user_prefs["valence"] - song["valence"])
        pts = round(weights["valence"] * (1.0 - val_diff), 2)
        score += pts
        reasons.append(f"valence closeness (+{pts})")

    # Acoustic preference
    if user_prefs.get("likes_acoustic") and song.get("acousticness", 0) > 0.6:
        pts = weights["acoustic"]
        score += pts
        reasons.append(f"acoustic preference (+{pts})")

    # Popularity bonus
    if "popularity" in song:
        pts = round(weights["popularity"] * (song["popularity"] / 100), 2)
        score += pts
        reasons.append(f"popularity bonus (+{pts})")

    # Mood tag match
    if user_prefs.get("mood_tag") and song.get("mood_tag", "").lower() == user_prefs["mood_tag"].lower():
        pts = weights["mood_tag"]
        score += pts
        reasons.append(f"mood tag match (+{pts})")

    score = round(score, 2)
    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "balanced") -> List[Tuple[Dict, float, str]]:
    """Scores all songs and returns the top k sorted by score."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, mode=mode)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
