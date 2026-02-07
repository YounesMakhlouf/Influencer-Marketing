FROM python:3.12-slim

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory in the container
WORKDIR /app

# Copy dependency manifest first (cache-friendly layer)
COPY pyproject.toml uv.lock* ./

# Install dependencies (no dev extras in production)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ && \
    uv sync --no-dev --frozen && \
    apt-get purge -y gcc g++ && apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY web/ /app/web/
COPY dataScraper/ /app/dataScraper/
COPY shared/ /app/shared/
COPY config.ini /app/

# Download NLTK data and spaCy model at build time
RUN uv run python -m spacy download en_core_web_sm && \
    uv run python -c "import nltk; nltk.download('stopwords', quiet=True)"

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
# Build from project root: docker build -f web/Dockerfile .
ENTRYPOINT ["uv", "run", "gunicorn", "--bind", "0.0.0.0:5000", "web.app:app"]