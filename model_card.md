# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

## 2. Intended Use

Suggests songs from a small catalog based on a user's genre, mood, and energy preferences. Built for classroom exploration, not real users.

## 3. How the Model Works

Each song gets scored against the user's preferences. Genre match gives +2.0, mood match +1.5, energy closeness up to +1.0, and smaller bonuses for danceability, valence, acousticness, and popularity. All points add up to a final score, songs get sorted, and the top ones are recommended. Each result includes an explanation like "genre match (+2.0), energy closeness (+0.98)".

There are also different ranking modes (genre-first, mood-first, energy-focused) that shift how much each feature matters.

## 4. Data

20 songs, 15 attributes each. Genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, r&b, country, classical, edm, latin, metal, folk. I expanded the original 10-song starter and added popularity, release decade, mood tags, instrumentalness, and liveness.

The dataset leans toward pop and lofi. Classical, folk, and country only have one song each.

## 5. Strengths

- Works well for popular genres (pop, lofi, rock)
- Explanations show exactly why each song was picked
- Multiple ranking modes let you explore how weights change results
- Diversity penalty prevents the same artist dominating results

## 6. Limitations and Bias

- Genre matching is exact — "indie pop" and "pop" are treated as different
- Dataset is small and unbalanced, so pop fans get better results than classical fans
- No learning from user behavior (listens, skips)
- Popularity bonus slightly favors mainstream songs over niche ones

## 7. Evaluation

Tested 3 profiles: Pop/Happy got pop songs on top, Lofi/Chill got acoustic lofi tracks, Rock/Intense got Storm Runner and Iron Tide. Results matched what I'd expect as a listener. No numeric metrics since the catalog is too small for that.

## 8. Future Work

- Fuzzy genre matching ("indie pop" treated as similar to "pop")
- Learn from listening history over time
- Balance the dataset so every genre has 2-3+ songs
- Let users dislike songs and adjust from that

## 9. Personal Reflection

The biggest thing I learned is that a recommender is only as good as its data and weights. The algorithm is simple math, but the choices about what to weigh more or less control what users see. It's easy to accidentally build something that works for one type of person and not another, just based on what's in the dataset.
