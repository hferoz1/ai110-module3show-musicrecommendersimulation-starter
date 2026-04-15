"""
Command line runner for the Music Recommender Simulation.
Demonstrates all three challenge features:
  Challenge 1 — Extended song features (popularity, era, detailed mood, liveness, instrumentalness)
  Challenge 2 — Multiple scoring modes (balanced / genre_first / mood_first / energy_focused)
  Challenge 3 — Diversity penalty (artist and genre repeat suppression)
"""

from src.recommender import load_songs, recommend_songs, SCORING_MODES


def print_results(label: str, recommendations: list, width: int = 62) -> None:
    """Prints a formatted leaderboard for one profile's top-k results."""
    print("\n" + "=" * width)
    print(f"  {label}")
    print("=" * width)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Score : {score:.2f}")
        for reason in explanation.split("; "):
            print(f"       + {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # ── Challenge 1: Extended Features ───────────────────────────────────────
    # Profile activates all 5 new scoring rules:
    #   preferred_decade=2020 (+1.0 for 2020s tracks)
    #   preferred_detailed_mood="nostalgic" (+1.5 for exact vibe match)
    #   likes_popular=False (+0.5 for underground tracks, popularity < 50)
    #   wants_instrumental=True (+0.5 when instrumentalness > 0.6)
    # Library Rain should dominate: lofi/chill/0.35 energy + all 4 new bonuses.

    print("\n\n" + "#" * 62)
    print("  CHALLENGE 1 — Extended Features")
    print("#" * 62)

    nostalgic_underground = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.38,
        "likes_acoustic": True,
        "preferred_decade": 2020,
        "preferred_detailed_mood": "nostalgic",
        "likes_popular": False,
        "wants_instrumental": True,
        "wants_live_feel": False,
    }
    print_results(
        "Nostalgic Underground Lofi (all new features active)",
        recommend_songs(nostalgic_underground, songs, k=5),
    )

    # ── Challenge 2: Scoring Modes ────────────────────────────────────────────
    # Same "intense pop" profile run through all four strategies.
    # Watch how Gym Hero vs Sunrise City swap ranks depending on whether
    # genre or mood carries more weight.

    print("\n\n" + "#" * 62)
    print("  CHALLENGE 2 — Scoring Modes (same profile, 4 strategies)")
    print("#" * 62)

    intense_pop = {
        "favorite_genre": "pop",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "likes_acoustic": False,
    }
    for mode_name in SCORING_MODES:
        print_results(
            f"Mode: {mode_name.upper()}",
            recommend_songs(intense_pop, songs, k=5, mode=mode_name),
        )

    # ── Challenge 3: Diversity Penalty ────────────────────────────────────────
    # LoRoom produces both Midnight Coding (#1) and Focus Flow (#3) for the
    # focused-lofi profile. Diversity reranking penalises Focus Flow by -0.5
    # (artist already represented), promoting Library Rain into the #2 slot.

    print("\n\n" + "#" * 62)
    print("  CHALLENGE 3 — Diversity Penalty")
    print("#" * 62)

    focused_lofi = {
        "favorite_genre": "lofi",
        "favorite_mood": "focused",
        "target_energy": 0.41,
        "likes_acoustic": True,
    }
    print_results(
        "Focused Lofi — WITHOUT diversity  (LoRoom can appear twice)",
        recommend_songs(focused_lofi, songs, k=5, diversity=False),
    )
    print_results(
        "Focused Lofi — WITH diversity  (repeated artist penalised -0.5)",
        recommend_songs(focused_lofi, songs, k=5, diversity=True),
    )


if __name__ == "__main__":
    main()
