import requests

with open("sre_knowledge.txt") as f:
    data = f.read()

paragraphs = [p.strip() for p in data.split("\n\n") if p.strip()]

for p in paragraphs:
    r = requests.post(
        "http://localhost:8000/ingest",
        json={"text": p}
    )

    print(r.status_code, p[:50])
