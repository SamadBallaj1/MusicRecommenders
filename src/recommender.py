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

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

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

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences."""
    score = 0.0
    reasons = []

    # Genre match: +2.0
    if song.get("genre", "").lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match: +1.5
    if song.get("mood", "").lower() == user_prefs.get("mood", "").lower():
        score += 1.5
        reasons.append("mood match (+1.5)")

    # Energy closeness: up to +1.0 (closer = higher)
    if "energy" in user_prefs and "energy" in song:
        energy_diff = abs(user_prefs["energy"] - song["energy"])
        energy_score = round(1.0 - energy_diff, 2)
        score += energy_score
        reasons.append(f"energy closeness (+{energy_score})")

    # Danceability closeness: up to +0.5
    if "danceability" in user_prefs and "danceability" in song:
        dance_diff = abs(user_prefs["danceability"] - song["danceability"])
        dance_score = round(0.5 * (1.0 - dance_diff), 2)
        score += dance_score
        reasons.append(f"danceability closeness (+{dance_score})")

    # Valence closeness: up to +0.5
    if "valence" in user_prefs and "valence" in song:
        val_diff = abs(user_prefs["valence"] - song["valence"])
        val_score = round(0.5 * (1.0 - val_diff), 2)
        score += val_score
        reasons.append(f"valence closeness (+{val_score})")

    # Acoustic preference: +0.5 if user likes acoustic and song is acoustic
    if user_prefs.get("likes_acoustic") and song.get("acousticness", 0) > 0.6:
        score += 0.5
        reasons.append("acoustic preference (+0.5)")

    # Popularity bonus: up to +0.3 based on popularity score
    if "popularity" in song:
        pop_score = round(0.3 * (song["popularity"] / 100), 2)
        score += pop_score
        reasons.append(f"popularity bonus (+{pop_score})")

    # Mood tag match: +0.5
    if user_prefs.get("mood_tag") and song.get("mood_tag", "").lower() == user_prefs["mood_tag"].lower():
        score += 0.5
        reasons.append("mood tag match (+0.5)")

    score = round(score, 2)
    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
