from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import psycopg2
import requests

app = FastAPI()

Instrumentator().instrument(app).expose(app)

model = SentenceTransformer("all-MiniLM-L6-v2")

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "postgres"
}

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

class TextData(BaseModel):
    text: str

@app.post("/ingest")
def ingest(data: TextData):
    embedding = model.encode(data.text).tolist()

    cur.execute(
        """
        INSERT INTO documents (content, embedding)
        VALUES (%s, %s::vector)
        """,
        (data.text, str(embedding))
    )

    conn.commit()

    return {"status": "stored"}

@app.post("/query")
def query(data: TextData):

    query_embedding = model.encode(data.text).tolist()

    cur.execute(
        """
        SELECT content
        FROM documents
        ORDER BY embedding <-> %s::vector
        LIMIT 3
        """,
        (str(query_embedding),)
    )

    results = cur.fetchall()

    context = "\n".join([r[0] for r in results])

    prompt = f"""
You are a Kubernetes SRE assistant.

Context:
{context}

Question:
{data.text}

Answer:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    answer = response.json()["response"]

    return {
        "question": data.text,
        "context": context,
        "answer": answer
    }
