import os

from dotenv import load_dotenv
from langchain_community.retrievers import PineconeHybridSearchRetriever
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from pinecone_text.sparse import BM25Encoder

load_dotenv()

texts = [
    "The balk rule was introduced in 1898.",
    "A strike zone is the area over home plate.",
    "An infield fly is an automatic out.",
]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
bm25 = BM25Encoder()
bm25.fit(texts)

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(os.environ["PINECONE_INDEX_NAME_V3"])

retriever = PineconeHybridSearchRetriever(
    embeddings=embeddings,
    sparse_encoder=bm25,
    index=index,
    top_k=3,
    alpha=0.5,
)

retriever.add_texts(texts=texts)
print("Success")
