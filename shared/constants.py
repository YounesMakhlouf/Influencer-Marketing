"""Shared constants used across notebooks and scripts."""

# Common noise words that leak into influencer bios / posts and should be
# stripped before any topic-modelling or word-cloud generation.
NOISE_WORDS: set[str] = {
    "null",
    "like",
    "com",
    "www",
    "gmail",
    "hotmail",
    "creator",
    "creators",
    "dm",
    "info",
    "email",
    "collab",
    "contact",
}
