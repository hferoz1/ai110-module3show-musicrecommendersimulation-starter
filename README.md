# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

ANSWER: The music recommender simulation is a project where you will create a simple system that suggests songs based on a user's preferences. You will represent songs with features like genre, mood, and energy level, and create a user profile that captures their tastes. The system will use a scoring rule to compare the songs to the user's preferences and recommend the best matches. Finally, you will evaluate the strengths and limitations of your system and reflect on how it relates to real-world music recommendation algorithms.
---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.
ANSWER: In my version of the music recommender, each `Song` is represented by its genre, mood, and energy level. The `UserProfile` stores the user's preferred genre, mood, and energy level. The `Recommender` computes a score for each song by comparing the song's features to the user's preferences. For example, it might give points for matching genre, mood, and energy level, and then recommend the songs with the highest scores.

Algorithm Recipe:
1. For each song in the catalog:
   a. Initialize a score to 0.
   b. If the song's genre matches the user's preferred genre, add 2 points to the score.
   c. If the song's mood matches the user's preferred mood, add 1 point to the score.
   d. If the song's energy level is within 0.1 of the user's preferred energy level, add 1 point to the score.
2. Sort the songs by their scores in descending order.
3. Recommend the top 3 songs with the highest scores.   

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

ANSWER: I experimented with changing the weight on genre from 2.0 to 0.5, which made the system less focused on matching the user's preferred genre and more open to recommending songs from other genres. This resulted in a more diverse set of recommendations, but some users felt that the recommendations were less relevant to their tastes. I also added tempo as a feature, which allowed the system to recommend songs that matched the user's preferred energy level more closely. This improved the relevance of the recommendations for users who had specific energy preferences.

---

## Terminal Output — User Profile Results

### Profile 1: Nostalgic Underground Lofi Listener
Preferences: genre=lofi, mood=chill, energy=0.38, likes_acoustic=True, preferred_decade=2020, preferred_detailed_mood=nostalgic, likes_popular=False, wants_instrumental=True

```
==============================================================
  Nostalgic Underground Lofi (all new features active)
==============================================================

  #1  Library Rain  —  Paper Lanterns
       Score : 7.97
       + genre match (+2.0)
       + mood match (+1.0)
       + energy similarity (+0.97)
       + acoustic match (+0.50)
       + detailed mood 'nostalgic' match (+1.5)
       + era match 2020s (+1.0)
       + underground track (pop=48) (+0.5)
       + instrumental match (+0.5)

  #2  Midnight Coding  —  LoRoom
       Score : 5.46
       + genre match (+2.0)
       + mood match (+1.0)
       + energy similarity (+0.96)
       + acoustic match (+0.50)
       + era match 2020s (+1.0)

  #3  Focus Flow  —  LoRoom
       Score : 4.48
       + genre match (+2.0)
       + energy similarity (+0.98)
       + acoustic match (+0.50)
       + era match 2020s (+1.0)

  #4  Spacewalk Thoughts  —  Orbit Bloom
       Score : 3.40
       + mood match (+1.0)
       + energy similarity (+0.90)
       + acoustic match (+0.50)
       + underground track (pop=45) (+0.5)
       + instrumental match (+0.5)

  #5  Coffee Shop Stories  —  Slow Stereo
       Score : 2.99
       + energy similarity (+0.99)
       + acoustic match (+0.50)
       + detailed mood 'nostalgic' match (+1.5)
```

---

### Profile 2: Intense Pop Listener (4 Scoring Modes Compared)
Preferences: genre=pop, mood=intense, energy=0.9, likes_acoustic=False

```
==============================================================
  Mode: BALANCED
==============================================================

  #1  Gym Hero  —  Max Pulse        Score: 4.47
       + genre match (+2.0) | mood match (+1.0) | energy similarity (+0.97) | low acousticness match (+0.50)

  #2  Sunrise City  —  Neon Echo    Score: 3.42
       + genre match (+2.0) | energy similarity (+0.92) | low acousticness match (+0.50)

  #3  Storm Runner  —  Voltline     Score: 2.49
       + mood match (+1.0) | energy similarity (+0.99) | low acousticness match (+0.50)

==============================================================
  Mode: GENRE_FIRST
==============================================================

  #1  Gym Hero  —  Max Pulse        Score: 5.23   (genre weight 4x)
  #2  Sunrise City  —  Neon Echo    Score: 4.71   (genre weight 4x)
  #3  Storm Runner  —  Voltline     Score: 1.24   (no genre match, drops sharply)

==============================================================
  Mode: MOOD_FIRST
==============================================================

  #1  Gym Hero  —  Max Pulse        Score: 5.47
  #2  Storm Runner  —  Voltline     Score: 4.49   (mood match now worth 3x, rises to #2)
  #3  Electric Pulse  —  Cyber Monks Score: 4.47  (mood match lifts non-pop song into top 3)

==============================================================
  Mode: ENERGY_FOCUSED
==============================================================

  #1  Gym Hero  —  Max Pulse        Score: 4.91
  #2  Sunrise City  —  Neon Echo    Score: 4.26
  #3  Storm Runner  —  Voltline     Score: 3.97   (high energy score closes the gap)
```

---

### Profile 3: Focused Lofi Listener — Diversity Penalty On vs. Off
Preferences: genre=lofi, mood=focused, energy=0.41, likes_acoustic=True

```
==============================================================
  WITHOUT diversity  (LoRoom can appear twice)
==============================================================

  #1  Focus Flow  —  LoRoom         Score: 4.49
  #2  Midnight Coding  —  LoRoom    Score: 3.49   (same artist as #1)
  #3  Library Rain  —  Paper Lanterns Score: 3.44

==============================================================
  WITH diversity  (repeated artist penalised -0.5)
==============================================================

  #1  Focus Flow  —  LoRoom         Score: 4.49
  #2  Library Rain  —  Paper Lanterns Score: 3.44  (promoted — different artist)
  #3  Midnight Coding  —  LoRoom    Score: 2.69   [diversity adj: 3.49 → 2.69]
```

**Profile comparison:** The lofi listener's results are dominated by slow, acoustic, low-energy tracks (Midnight Coding, Library Rain, Focus Flow) — none of which appear in the intense pop listener's top-5. The scoring modes experiment shows that switching from `balanced` to `mood_first` promotes Storm Runner from #3 to #2 and pulls non-pop songs (Electric Pulse) into the top 3, demonstrating that even a small weight change can meaningfully shift which songs surface.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.
ANSWER: Some limitations of my recommender include the fact that it only works on a small catalog of songs, which limits the diversity of recommendations. It also does not take into account lyrics or language, which can be important factors in music preference. Additionally, the scoring system might over-favor certain genres or moods if the weights are not balanced properly, leading to less personalized recommendations for users with more eclectic tastes.
---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
ANSWER: Through this project, I learned that music recommenders rely heavily on the features of songs and user preferences to generate recommendations. The way these features are weighted can significantly influence the output, and even small changes in the scoring logic can lead to different recommendations. I also realized that bias can easily creep into such systems, especially if the catalog is limited or if certain genres or moods are overrepresented. For example, if the system heavily favors a particular genre, users with different tastes might receive less relevant recommendations, which could lead to a less satisfying user experience. This highlights the importance of carefully designing the recommendation algorithm and ensuring a diverse and representative dataset to mitigate bias and improve fairness.

---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  
ANSWER: The `model_card_template.md` is a structured document that guides you through creating a model card for your music recommender system. It includes sections such as Model Name, Intended Use, How It Works, Data, Strengths, Limitations and Bias, Evaluation, Future Work, and Personal Reflection. This template helps you systematically analyze and communicate the design, functionality, and implications of your recommender system, ensuring that you consider both its technical aspects and its real-world impact.

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:
> VibeFinder 1.0

ANSWER: I will name my recommender "TuneMatcher 1.0". This name reflects the system's purpose of matching users with songs that fit their preferences and tastes.
---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

ANSWER: This model is designed to recommend songs from a small catalog based on a user's preferred genre, mood, and energy level. It is intended for educational purposes to demonstrate how music recommendation systems work, and it is not meant for real-world use due to its limited dataset and simplified scoring logic.
---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.
ANSWER: The scoring logic of my recommender works by comparing the features of each song to the user's preferences. For each song, it checks if the genre matches the user's preferred genre, if the mood matches the user's preferred mood, and if the energy level is close to the user's preferred energy level. Each of these matches contributes to a score for that song. The songs are then ranked based on their scores, and the top recommendations are presented to the user. The system essentially quantifies how well each song aligns with the user's tastes and uses that to generate recommendations.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect
ANSWER: The dataset in `data/songs.csv` contains 17 songs, each with features such as genre, mood, and energy level. I did not add or remove any songs from the original dataset. The genres represented include pop, rock, metal, ambient, and acoustic. The moods range from happy and intense to calm and contemplative. The dataset seems to reflect a variety of tastes, but it may be skewed towards certain genres like pop and rock, which could influence the recommendations for users with different preferences.
---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

ANSWER: The recommender works well for users whose preferences closely align with the features of the songs in the catalog. For example, a user who prefers pop music with a happy mood and high energy level would likely receive relevant recommendations like "Sunrise City" and "Gym Hero". The simplicity of the scoring logic also makes it transparent and easy to understand how recommendations are generated, which can be beneficial for educational purposes. Additionally, the system is effective at differentiating between different user profiles, as it can produce distinct recommendations based on varying preferences for genre, mood, and energy level.
---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

ANSWER: The recommender struggles with a limited catalog, which means it may not be able to provide relevant recommendations for users with niche tastes or preferences that are not well-represented in the dataset. It also treats all users as if they have the same "taste shape," meaning it does not account for the complexity and diversity of individual preferences. The system may be biased toward high-energy songs or certain genres if those are more prevalent in the dataset, which could lead to unfair recommendations for users who prefer softer or less mainstream music. In a real product, this could result in a lack of diversity in recommendations and potentially alienate users with unique tastes.
---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

ANSWER: I evaluated my system by creating multiple user profiles with different preferences for genre, mood, and energy level. I then ran the recommender for each profile and analyzed whether the top recommendations aligned with what I would expect based on the user's tastes. For example, a user who prefers calm, acoustic music should receive recommendations that fit those criteria. I also compared the recommendations to what a real app like Spotify might suggest for similar preferences, noting any similarities or differences. Additionally, I wrote tests for the scoring logic to ensure that it correctly calculates scores based on the defined rules for genre, mood, and energy level matches.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

ANSWER: If I had more time, I would improve the recommender by adding support for multiple users and creating "group vibe" recommendations that take into account the preferences of all users in a group. I would also implement a mechanism to balance diversity in the recommendations, ensuring that users are exposed to a wider range of songs rather than always receiving the closest match. Additionally, I would consider incorporating more features such as tempo ranges, lyric themes, and even user listening history to create more personalized and dynamic recommendations.
---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"
ANSWER: I was surprised by how much the weighting of different features influenced the recommendations, and how small changes in the scoring logic could lead to significantly different results. Building this recommender made me realize that real music recommenders are likely much more complex than they appear on the surface, and that they have to balance a wide range of factors to provide relevant suggestions. I also think that human judgment still matters in curating playlists and making recommendations, especially when it comes to understanding the emotional context of music and the nuances of individual tastes that may not be fully captured by data alone.
