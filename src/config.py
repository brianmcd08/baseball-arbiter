import os

# from secrets import get_secret
from langchain_anthropic import ChatAnthropic

# os.environ["ANTHROPIC_API_KEY"] = get_secret("ANTHROPIC_API_KEY")

# scraper
MLB_SCHEMA = "https://www.mlb.com"
MLB_RULEBOOK_URL = MLB_SCHEMA + "/glossary/rules"
SCRAPER_TIMEOUT = 10

# Embeddings
EMBEDDINGS_MODEL = "text-embedding-3-small"
BM25_MODEL_PATH = "models/bm25_values.json"

# Pinecone
INDEX_DIMENSION = 1536
INDEX_CLOUD = "aws"
INDEX_METRIC = "dotproduct"
INDEX_REGION = "us-east-1"

# Retrieval
ALPHA = 0.5
K_GENERAL = 8

# Ingestion
K_INGEST = 25
BATCH_SIZE = 50

# LLM
ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"
ANTHROPIC_JUDGE = "claude-sonnet-4-6"
LLM_TIMEOUT = 30
