FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# CPU-only PyTorch for a reproducible development baseline.
RUN python -m pip install --upgrade pip && \
    python -m pip install torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "src.data.download_datasets", "--datasets", "BBBP", "Tox21", "ESOL"]
