from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []

    with open(csv_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"])
            }
            songs.append(song)

    print(f"Loaded songs: {len(songs)}")
    return songs


# ✅ ADDED FUNCTION (only new part)
def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    score = 0.0
    reasons = []

    song_genre = song["genre"].lower()
    song_mood = song["mood"].lower()
    user_genre = user_prefs["genre"].lower()
    user_mood = user_prefs["mood"].lower()

    if song_genre == user_genre:
        score += 2.0
        reasons.append("Genre match (+2.0)")

    if song_mood == user_mood:
        score += 1.5
        reasons.append("Mood match (+1.5)")

    energy_similarity = 1 - abs(song["energy"] - user_prefs["energy"])
    score += energy_similarity * 2
    reasons.append(f"Energy similarity ({round(energy_similarity, 2)})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    results = []

    for song in songs:
        # ✅ UPDATED to use score_song
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)

        results.append((song, score, explanation))

    results.sort(key=lambda x: x[1], reverse=True)

    return results[:k]