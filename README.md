# Influencer-Marketing

A machine-learning tool that **automatically categorises Instagram influencers by topic** using [BERTopic](https://maartengr.github.io/BERTopic/).
Given an influencer's username, the system scrapes their public profile, cleans the text, and predicts which content category they belong to (e.g. fitness, food, travel, beauty …).

## How it works

1. **Data collection** – Instagram bios and captions are scraped via `httpx` (or bulk-imported with [Apify](https://apify.com/)).
2. **Text cleaning** – translation to English (Google Translate), emoji removal, stop-word removal (NLTK), and lemmatisation (spaCy).
3. **Topic modelling** – a BERTopic model (embedding: `all-MiniLM-L6-v2`, clustering: HDBSCAN, representation: c-TF-IDF) trained on ~38 000 influencer documents.
4. **Serving** – a Flask + Gunicorn API exposes three endpoints for real-time predictions.

> We also experimented with LDA (Gensim) but its coherence score (0.27) was significantly lower than BERTopic's (0.37). See [`report/report.tex`](report/report.tex) for the full analysis.

## Project structure

```
├── web/                  # Flask API + Dockerfile
│   ├── app.py            # /predict, /scrape, /predict_user endpoints
│   ├── cleaning.py       # Text cleaning pipeline
│   ├── bert_9.pkl        # Pickled BERTopic model (88 MB)
│   └── Dockerfile
├── dataScraper/          # Instagram scraping & parsing
│   ├── scraper.py
│   └── dataParser.py
├── shared/               # Shared utilities
│   ├── config.py         # Centralised config loader (config.ini)
│   └── mongo.py          # MongoDB singleton connection
├── services/             # MongoDB CRUD for influencers
├── data-cleaning/        # Standalone cleaning scripts (batch mode)
├── model-training/       # Jupyter notebooks for LDA & BERTopic training
├── report/               # LaTeX project report
├── pyproject.toml        # Dependency manifest (managed with uv)
└── config.ini            # MongoDB & app configuration
```

## Requirements

- Python **3.10 – 3.13** (3.12 recommended)
- [uv](https://docs.astral.sh/uv/) package manager

## Getting started

```bash
# 1. Install dependencies
uv sync

# 2. Configure MongoDB connection
#    Edit config.ini with your MongoDB URI, database, and collection names.

# 3. Run the API locally
uv run flask --app web.app run
```

## API endpoints

| Method | Path            | Body                  | Description                                              |
|--------|-----------------|-----------------------|----------------------------------------------------------|
| POST   | `/predict`      | `{"text": "..."}`     | Predict topic from raw text                              |
| POST   | `/scrape`       | `{"name": "username"}`| Scrape an Instagram user's bio & category                |
| POST   | `/predict_user` | `{"name": "username"}`| Scrape, clean, and predict an influencer's topic in one call |

### Example

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "fitness coach personal trainer workout motivation"}'
```

## Docker

Build and run from the project root:

```bash
docker build -f web/Dockerfile -t influencer-marketing .
docker run -p 5000:5000 influencer-marketing
```

The image uses `python:3.12-slim` with CPU-only PyTorch (~3 GB smaller than the CUDA variant).

## Tech stack

| Layer            | Technology                                    |
|------------------|-----------------------------------------------|
| Topic modelling  | BERTopic, all-MiniLM-L6-v2, HDBSCAN, c-TF-IDF|
| NLP              | spaCy, NLTK, deep-translator, Unidecode       |
| Web framework    | Flask, Gunicorn                               |
| Scraping         | httpx (with timeout & retries)                |
| Database         | MongoDB (pymongo)                             |
| Package manager  | uv                                            |
| Containerisation | Docker                                        |