import requests
import os

from typing import List

API_BASE_URL = os.environ.get("API_BASE_URL", "https://data-idm.unavco.org/user/profile")


def get_user(access_token: str):
    r = requests.get(
        f"{API_BASE_URL}/api/user/",
        headers={"authorization": f"Bearer {access_token}"},
    )
    if r.status_code == 200:
        return r.json()

    raise RuntimeError(r.json()["detail"])


def lookup_anon(access_token: str, ids: List[str], emails: List[str]):
    r = requests.post(
        f"{API_BASE_URL}/api/user/anon/",
        headers={"authorization": f"Bearer {access_token}"},
        json={"ids": ids, "emails": emails},
    )

    if r.status_code == 200:
        return r.json()

    raise RuntimeError(r.json()["detail"])


