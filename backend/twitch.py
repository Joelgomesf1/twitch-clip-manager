
import requests
from datetime import datetime, timedelta, UTC
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def get_access_token():
    url = "https://id.twitch.tv/oauth2/token"

    response = requests.post(
        url,
        params={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials"
        }
    )

    data = response.json()

    return data["access_token"]

def get_user_id(username):
    token = get_access_token()

    response = requests.get(
        "https://api.twitch.tv/helix/users",
        headers={
            "Client-ID": CLIENT_ID,
            "Authorization": f"Bearer {token}"
        },
        params={
            "login": username
        }
    )

    data = response.json()

    return data

def get_clips(user_id, dias):
    token = get_access_token()

    inicio = datetime.now(UTC) - timedelta(days=dias)

    fim = datetime.now(UTC)

    response = requests.get(
        "https://api.twitch.tv/helix/clips",
        headers={
            "Client-ID": CLIENT_ID,
            "Authorization": f"Bearer {token}"
        },
        params={
        "broadcaster_id": user_id,
        "started_at": inicio.isoformat().replace("+00:00", "Z"),
        "ended_at": fim.isoformat().replace("+00:00", "Z"),
        "first": 100
        }
    )

    return response.json()