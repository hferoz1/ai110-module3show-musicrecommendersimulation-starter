import csv
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Optional

# ── Challenge 2: Scoring mode weight tables ───────────────────────────────────
# Each mode redistributes the same total weight budget differently.
# "balanced"      is the original default.
# "genre_first"   pushes genre to 4x normal; good for label-loyal listeners.
# "mood_first"    triples mood weight; good for emotion-driven listeners.
# "energy_focused" triples energy weight; good for workout / focus playlists.

SCORING_MODES: Dict[str, Dict[str, float]] = {
    "balanced":       {"genre": 2.0, "mood": 1.0, "energy": 1.0, "acousticness": 0.5},
    "genre_first":    {"genre": 4.0, "mood": 0.5, "energy": 0.5, "acousticness": 0.25},
    "mood_first":     {"genre": 1.0, "mood": 3.0, "energy": 1.0, "acousticness": 0.5},
    "energy_focused": {"genre": 1.0, "mood": 0.5, "energy": 3.0, "acousticness": 0.5},
}


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
    # Challenge 1: extended features (default values keep old tests passing)
    popularity: int = 50
    release_decade: int = 2020
    detailed_mood: str = ""
    liveness: float = 0.15
    instrumentalness: float = 0.10


@dataclass
class UserProfile:
    """Represents a listener's taste preferences used to score and rank songs."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    # Challenge 1: extended preferences (all optional so existing tests pass)
    preferred_decade: Optional[int] = None
    preferred_detailed_mood: Optional[str] = None
    likes_popular: Optional[bool] = None
    wants_instrumental: bool = False
    wants_live_feel: bool = False


class Recommender:
    """Scores and ranks a catalog of songs against a user's taste profile."""

    def __init__(self, songs: List[Song]):
        """Initializes the recommender with a catalog of Song objects."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5, mode: str = "balanced") -> List[Song]:
        """Returns the top-k songs ranked by score for the given user profile."""
        user_prefs = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
            "preferred_decade": user.preferred_decade,
            "preferred_detailed_mood": user.preferred_detailed_mood,
            "likes_popular": user.likes_popular,
            "wants_instrumental": user.wants_instrumental,
            "wants_live_feel": user.wants_live_feel,
        }
        scored = []
        for song in self.songs:
            score, _ = score_song(user_prefs, asdict(song), mode=mode)
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
        if user.preferred_detailed_mood and song.detailed_mood == user.preferred_detailed_mood:
            reasons.append(f"detailed mood '{song.detailed_mood}' matches your vibe")
        if user.preferred_decade and song.release_decade == user.preferred_decade:
            reasons.append(f"from your preferred era ({song.release_decade}s)")
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
                # Challenge 1: extended features
                "popularity": int(row.get("popularity", 50)),
                "release_decade": int(row.get("release_decade", 2020)),
                "detailed_mood": row.get("detailed_mood", ""),
                "liveness": float(row.get("liveness", 0.15)),
                "instrumentalness": float(row.get("instrumentalness", 0.10)),
            })
    return songs


def score_song(
    user_prefs: Dict, song: Dict, mode: str = "balanced"
) -> Tuple[float, List[str]]:
    """Scores a song against user preferences and returns a (score, reasons) tuple."""
    weights = SCORING_MODES.get(mode, SCORING_MODES["balanced"])
    score = 0.0
    reasons = []

    # ── Core scoring (Challenge 2: weights vary by mode) ─────────────────────

    # Genre match
    genre_pts = weights["genre"]
    if song.get("genre") == user_prefs.get("favorite_genre"):
        score += genre_pts
        reasons.append(f"genre match (+{genre_pts:.1f})")

    # Mood match
    mood_pts = weights["mood"]
    if song.get("mood") == user_prefs.get("favorite_mood"):
        score += mood_pts
        reasons.append(f"mood match (+{mood_pts:.1f})")

    # Energy similarity: scale max points by the mode's energy weight
    energy_weight = weights["energy"]
    energy_diff = abs(song.get("energy", 0.5) - user_prefs.get("target_energy", 0.5))
    energy_score = round(max(0.0, energy_weight * (1.0 - energy_diff)), 2)
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score:.2f})")

    # Acousticness preference
    acousticness_pts = weights["acousticness"]
    acousticness = song.get("acousticness", 0.5)
    if user_prefs.get("likes_acoustic") and acousticness > 0.6:
        score += acousticness_pts
        reasons.append(f"acoustic match (+{acousticness_pts:.2f})")
    elif not user_prefs.get("likes_acoustic") and acousticness < 0.4:
        score += acousticness_pts
        reasons.append(f"low acousticness match (+{acousticness_pts:.2f})")

    # ── Extended scoring (Challenge 1: new features) ──────────────────────────

    # Detailed mood match: +1.5 — rewards a precise vibe alignment
    if user_prefs.get("preferred_detailed_mood") and \
            song.get("detailed_mood") == user_prefs["preferred_detailed_mood"]:
        score += 1.5
        reasons.append(f"detailed mood '{song['detailed_mood']}' match (+1.5)")

    # Era match: +1.0 — rewards songs from the listener's preferred decade
    if user_prefs.get("preferred_decade") and \
            song.get("release_decade") == user_prefs["preferred_decade"]:
        score += 1.0
        reasons.append(f"era match {song['release_decade']}s (+1.0)")

    # Popularity preference: +0.5 — explicit preference for mainstream or underground
    popularity = song.get("popularity", 50)
    if user_prefs.get("likes_popular") is True and popularity > 70:
        score += 0.5
        reasons.append(f"popular track (pop={popularity}) (+0.5)")
    elif user_prefs.get("likes_popular") is False and popularity < 50:
        score += 0.5
        reasons.append(f"underground track (pop={popularity}) (+0.5)")

    # Instrumentalness: +0.5 — rewards instrumental-heavy tracks when requested
    if user_prefs.get("wants_instrumental") and song.get("instrumentalness", 0.1) > 0.6:
        score += 0.5
        reasons.append("instrumental match (+0.5)")

    # Liveness: +0.5 — rewards live-feel recordings when requested
    if user_prefs.get("wants_live_feel") and song.get("liveness", 0.15) > 0.25:
        score += 0.5
        reasons.append(f"live feel (liveness={song.get('liveness', 0.15):.2f}) (+0.5)")

    return (score, reasons)


def _rerank_for_diversity(
    scored: List[Tuple[Dict, float, str]],
    k: int,
    artist_penalty: float = 0.5,
    genre_penalty: float = 0.3,
) -> List[Tuple[Dict, float, str]]:
    """Greedily selects top-k songs, penalizing repeated artists and over-represented genres."""
    remaining = list(scored)
    selected: List[Tuple[Dict, float, str]] = []
    artist_counts: Dict[str, int] = {}
    genre_counts: Dict[str, int] = {}

    while remaining and len(selected) < k:
        best_idx, best_adjusted = 0, float("-inf")

        for i, (song, base_score, _) in enumerate(remaining):
            artist = song.get("artist", "")
            genre = song.get("genre", "")
            adjusted = base_score
            # Penalize each repeated appearance by the same artist
            adjusted -= artist_penalty * artist_counts.get(artist, 0)
            # Penalize a genre once it already has 2+ representatives
            if genre_counts.get(genre, 0) >= 2:
                adjusted -= genre_penalty * (genre_counts[genre] - 1)
            if adjusted > best_adjusted:
                best_adjusted, best_idx = adjusted, i

        chosen, orig_score, explanation = remaining.pop(best_idx)
        artist = chosen.get("artist", "")
        genre = chosen.get("genre", "")

        # Annotate the explanation if a penalty was actually applied
        if artist_counts.get(artist, 0) > 0:
            explanation += f" [diversity adj: {orig_score:.2f} → {best_adjusted:.2f}]"

        selected.append((chosen, best_adjusted, explanation))
        artist_counts[artist] = artist_counts.get(artist, 0) + 1
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

    return selected


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
    diversity: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """Scores every song in the catalog and returns the top-k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, mode=mode)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)

    if diversity:
        return _rerank_for_diversity(scored, k)
    return scored[:k]
