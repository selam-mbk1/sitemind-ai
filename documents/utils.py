import requests
from django.conf import settings


def get_embedding(text):
    response = requests.post(
        "https://api.voyageai.com/v1/embeddings",
        headers={
            "Authorization": f"Bearer {settings.VOYAGE_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "voyage-2",
            "input": text
        }
    )

    response.raise_for_status()
    return response.json()["data"][0]["embedding"]
