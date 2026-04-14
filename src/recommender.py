import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """Represents a song and its audio feature attributes."""
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
    """Represents a listener's taste preferences used to score and rank songs."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """Scores and ranks a catalog of songs against a user's taste profile."""

    def __init__(self, songs: List[Song]):
        """Initializes the recommender with a catalog of Song objects."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top-k songs ranked by score for the given user profile."""
        user_prefs = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        scored = []
        for song in self.songs:
            song_dict = {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "acousticness": song.acousticness,
            }
            score, _ = score_song(user_prefs, song_dict)
            scored.append((song, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable string explaining why a song was recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"genre matches '{user.favorite_genre}'")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood matches '{user.favorite_mood}'")
        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff < 0.2:
            reasons.append(
                f"energy ({song.energy:.2f}) is close to your target ({user.target_energy:.2f})"
            )
        if user.likes_acoustic and song.acousticness > 0.6:
            reasons.append(
                f"high acousticness ({song.acousticness:.2f}) suits your acoustic preference"
            )
        elif not user.likes_acoustic and song.acousticness < 0.4:
            reasons.append(
                f"low acousticness ({song.acousticness:.2f}) suits your preference"
            )
        if not reasons:
            return f"'{song.title}' has some features that may appeal to you."
        return f"'{song.title}' recommended because: " + ", ".join(reasons) + "."


def load_songs(csv_path: str) -> List[Dict]:
    """Reads a CSV file and returns each row as a dict with numeric fields cast to float/int."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song against user preferences and returns a (score, reasons) tuple."""
    score = 0.0
    reasons = []

    # +2.0 for genre match
    if song.get("genre") == user_prefs.get("favorite_genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    # +1.0 for mood match
    if song.get("mood") == user_prefs.get("favorite_mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy similarity: closer to target_energy earns more points (max +1.0)
    energy_diff = abs(song.get("energy", 0.5) - user_prefs.get("target_energy", 0.5))
    energy_score = round(max(0.0, 1.0 - energy_diff), 2)
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score:.2f})")

    # +0.5 for acousticness preference alignment
    acousticness = song.get("acousticness", 0.5)
    if user_prefs.get("likes_acoustic") and acousticness > 0.6:
        score += 0.5
        reasons.append("acoustic preference match (+0.5)")
    elif not user_prefs.get("likes_acoustic") and acousticness < 0.4:
        score += 0.5
        reasons.append("low acousticness match (+0.5)")

    return (score, reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song in the catalog and returns the top-k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
