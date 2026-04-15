# 🎧 Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeFinder 1.0**

A rule-based music recommender that matches songs to a listener's taste profile using genre, mood, energy, and acoustic preference.

---

## 2. Intended Use

VibeFinder is designed to suggest songs from a small catalog that best fit a listener's stated preferences. It is built for classroom exploration — not for production use on a real streaming platform.

The system assumes the user already knows what they like and can describe it in simple terms: a favorite genre, a favorite mood, an energy level between 0 and 1, and whether they like acoustic-sounding music. It does not learn from listening history or adapt over time.

It should not be used to make recommendations in a commercial product, to represent any user's full musical identity, or in any context where a wrong recommendation could cause harm. It is a learning tool for understanding how scoring-based recommenders work.

---

## 3. How the Model Works

Think of VibeFinder like a judge at a talent show with a scorecard. Every song in the catalog walks on stage, and the judge awards points based on how well the song matches what the listener said they wanted.

The scorecard works like this:

- **Genre match** is worth the most — 2 points. If a listener says they like lofi and the song is tagged lofi, it gets the full 2 points. If the genre is anything else, it gets zero. There is no partial credit.
- **Mood match** is worth 1 point. Same rule — it either matches or it does not.
- **Energy closeness** is worth up to 1 point. The closer the song's energy level is to the listener's target, the more points it earns. A perfect match gives the full point; a song at the opposite extreme gives nearly zero.
- **Acousticness preference** is worth half a point. If the listener likes acoustic-sounding music and the song scores high on acousticness, it earns the bonus. If they prefer electric/produced music and the song is low on acousticness, it earns the bonus the other way.

Every song gets scored, the scores are sorted from highest to lowest, and the top five are returned as recommendations.

---

## 4. Data

The catalog contains 17 songs stored in `data/songs.csv`. Each song has ten attributes: a numeric ID, title, artist, genre, mood, and five audio feature scores (energy, tempo in BPM, valence, danceability, and acousticness). The numeric features are all on a 0–1 scale except tempo, which is in beats per minute.

Genres represented: pop, lofi, rock, ambient, synthwave, jazz, electronic, country, reggae, metal, classical, soul, and indie pop. Moods represented: happy, chill, intense, focused, relaxed, moody, nostalgic, melancholic, aggressive, calm, and peaceful.

The dataset was not modified from the starter version. Nine of the thirteen genres appear only once, which means the catalog is very thin for most genre preferences. There is no hip-hop, R&B, folk, or classical-crossover music. Tempo and danceability are present as fields but are not used by the scoring logic.

---

## 5. Strengths

VibeFinder works best when the listener's preferences align tightly with a well-represented genre. A lofi/chill listener gets an almost perfect top-3 (Midnight Coding, Library Rain, Focus Flow) because three lofi songs exist and all of them have low energy and high acousticness — every feature pulls in the same direction.

The energy similarity score is a genuine strength over a purely categorical system. Even when no genre or mood matches, the recommender can still surface songs that "feel" right in terms of intensity. The Dead-Centre jazz profile shows this: once the single jazz song takes #1, the remaining four slots are filled by songs near energy 0.5, which is at least a coherent fallback.

The reasons list returned with each recommendation makes it easy to understand exactly why a song was chosen. This transparency would be difficult to achieve with a machine learning model.

---

## 6. Limitations and Bias

**Genre dominance and the single-song trap.** The genre weight (2.0) is larger than mood, energy, and acousticness combined (1.0 + 1.0 + 0.5 = 2.5 max). For the nine genres that appear only once in the 17-song catalog — rock, metal, classical, jazz, country, reggae, electronic, synthwave, soul — the one matching song will always rank first by a wide margin, no matter how poorly it fits on every other dimension. A jazz listener always gets Coffee Shop Stories as #1 regardless of their energy or acousticness preferences.

**No concept of genre similarity.** Genre matching is a strict string equality check. The system treats "rock" and "metal" as completely unrelated, so a user who asks for intense rock gets Metal Fury ranked fourth — below songs it would realistically beat — simply because that song is tagged "metal" rather than "rock." Real listening taste does not work this way.

**Energy symmetry hides a directional bias.** The energy score is calculated as `1.0 - |target - song_energy|`, which penalizes a song equally whether it is too high or too low. In practice, a user with `target_energy = 0.8` is unlikely to reject a 0.9-energy song the same way they would reject a 0.3-energy song, but the scorer does exactly that. This makes the system less useful for users who prefer "at least this energetic" rather than "exactly this energetic."

**Unused features create a false sense of completeness.** The dataset includes `tempo_bpm`, `valence`, and `danceability`, but none of these are used in scoring. A high-valence (emotionally positive) song and a low-valence song with identical genre, mood, and energy receive the same score, even though valence would clearly differentiate them for many listeners.

**Filter bubble risk at scale.** Because genre weight dominates, any user whose favorite genre is well-represented in the catalog will receive a nearly identical top-5 list every run. The experiment of halving the genre weight (to +1.0) and doubling energy (to max +2.0) showed that rankings became noticeably more varied — Rooftop Lights climbed from score 2.41 to 3.32 for the pop/happy profile, and the adversarial acoustic+high-energy profile flipped its #1 entirely — suggesting the current weights push users into a narrow slice of the catalog.

---

## 7. Evaluation

Six user profiles were tested: three standard listeners (High-Energy Pop, Chill Lofi, Deep Intense Rock) and three adversarial cases designed to stress-test edge cases (Acoustic but High-Energy, Metal and Happy, and a Dead-Centre sparse-match profile with Jazz as the preferred genre).

For each profile, the top 5 results were inspected to check whether the song ranked first was genuinely the best fit, whether the score gap between #1 and #2 was sensible, and whether any unexpected song appeared in the list.

The standard profiles all behaved as expected: Sunrise City topped the pop list, Midnight Coding topped the lofi list, and Storm Runner topped the rock list — each earning near-maximum scores by matching genre, mood, and energy simultaneously.

The most surprising result came from the Deep Intense Rock profile: Metal Fury ranked fourth, not first or second. A human listener would almost certainly recommend a metal song to someone who loves intense rock, but the system treats "rock" and "metal" as completely separate labels. Metal Fury earned zero genre points and only reached the list through energy and low-acousticness bonuses.

A weight-shift experiment was also run — genre weight halved to +1.0, energy weight doubled to max +2.0 — to measure how sensitive the rankings were to the scoring formula. The standard profiles were largely unchanged, but the adversarial acoustic+high-energy profile flipped its top result entirely, confirming that the current genre weight dominates and can override energy preferences when they conflict.

---

## 8. Ideas for Improvement

**Use a genre hierarchy instead of exact matching.** Rock, metal, and punk could all belong to a broader "hard rock" family. A partial match within the same family could earn 1.0 point instead of 0, making the system far more useful for niche genre listeners.

**Make energy directional.** Replace the symmetric penalty with an asymmetric one: a song that exceeds the target energy by 0.1 should barely be penalized, while a song that falls 0.1 below target should lose more points. This would better reflect how most listeners describe their preferences ("give me something at least this energetic").

**Use valence and danceability in scoring.** Both fields are already in the dataset and already loaded. Adding even a small weight for valence (emotional positivity) would meaningfully separate songs that currently score identically — for example, a sad low-energy track and a peaceful low-energy track would no longer tie when the user asked for something uplifting.

---

## 9. Personal Reflection

The biggest learning moment in this project was discovering that a scoring formula and a dataset are not independent things. The weights I chose — 2.0 for genre, 1.0 for mood — felt reasonable in isolation, but once I ran them against a 17-song catalog with 9 single-genre entries, the genre weight effectively made mood irrelevant for most users. A design decision that looks fine on paper can behave very differently when it meets real (or even simulated) data.

Using AI tools to generate starter code and docstrings was genuinely useful for moving fast, but I had to double-check every output against the test suite and against my own intuition about the expected results. The AI would sometimes suggest code that was syntactically correct but logically wrong — for example, producing energy similarity values outside the expected 0–1 range — which the tests caught. The lesson is that AI is a good first draft, not a final answer.

What surprised me most was how much a simple point-based system can feel like a real recommendation. When Midnight Coding came back as #1 for the lofi profile with a score of 4.48 and a clear explanation of why, it felt satisfying in a way I did not expect from four lines of math. That feeling is partly why real recommenders are so powerful — and partly why it is so important to look carefully at the cases where they fail quietly instead of loudly.

If I extended this project, I would first expand the catalog to at least 100 songs with balanced genre representation, then replace the binary genre match with a similarity score based on a genre tree. After that, I would look at incorporating listening history — even a simple "liked / skipped" signal — to move from a static profile toward one that updates as the user interacts with the system.
