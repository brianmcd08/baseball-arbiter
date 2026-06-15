import os
import time
import uuid

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from pinecone_text.sparse import BM25Encoder

from src.config import (
    BATCH_SIZE,
    BM25_MODEL_PATH,
    EMBEDDINGS_MODEL,
    INDEX_CLOUD,
    INDEX_DIMENSION,
    INDEX_METRIC,
    INDEX_REGION,
)
from src.schema import RuleChunk
from src.scraper import scraper


def fit_bm25(chunks: list[RuleChunk]) -> BM25Encoder:
    bm25_encoder = BM25Encoder(language="english", remove_stopwords=True, stem=True)
    texts = [c.content for c in chunks]
    bm25_encoder.fit(texts)
    os.makedirs(name="models", exist_ok=True)
    bm25_encoder.dump(BM25_MODEL_PATH)
    return bm25_encoder


def embed_data(chunks: list[RuleChunk], encoder: BM25Encoder):
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pc.Index(os.environ["PINECONE_INDEX_NAME_V3"])
    embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)
    batches = [chunks[i : i + BATCH_SIZE] for i in range(0, len(chunks), BATCH_SIZE)]
    for batch in batches:
        batch_texts = [c.content for c in batch]
        dense_vectors = embeddings.embed_documents(batch_texts)
        sparse_vectors = encoder.encode_documents(batch_texts)

        vectors = []
        for i, (chunk, dense, sparse) in enumerate(
            zip(batch, dense_vectors, sparse_vectors)
        ):
            vectors.append(
                {
                    "id": str(uuid.uuid4()),
                    "values": dense,
                    "sparse_values": sparse,
                    "metadata": {
                        "rule_name": chunk.rule_name,
                        "url": chunk.url,
                        "subsection": chunk.subsection,
                        "text": chunk.content,
                    },
                }
            )

        index.upsert(vectors=vectors)


def main():
    load_dotenv()
    chunks = scraper()
    encoder = fit_bm25(chunks)
    embed_data(chunks=chunks, encoder=encoder)


if __name__ == "__main__":
    main()
