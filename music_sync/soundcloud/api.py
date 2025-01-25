from requests import get

API_URL = "https://api-v2.soundcloud.com/"
CLIENT_ID = "iZIs9mchVcX5lhVRyQGGAYlNPVldzAoX"


def getFromSoundCloudAPI(path: str, params: dict = None, headers: dict = None):
    if headers is None:
        headers = {}
    if params is None:
        params = {}
    _params = {
        "client_id": CLIENT_ID,
    }
    _params.update(params)
    _headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"  # noqa: E501
    }
    _headers.update(headers)

    response = get(f"{API_URL}{path}", params=_params, headers=_headers)
    response.raise_for_status()

    return response


def find_user(username: str):
    params = {"q": username, "limit": 1}
    response = getFromSoundCloudAPI("search/users", params)
    response.raise_for_status()
    id = response.json()["collection"][0]

    return id


def list_liked_tracks(username: str, limit: int = 5000):
    user_id = find_user(username)["id"]
    params = {"limit": limit}
    response = getFromSoundCloudAPI(f"users/{user_id}/likes", params)
    response.raise_for_status()
    likes = response.json()["collection"]

    likes_tracks = [like["track"] for like in likes if like.get("track") is not None]

    return likes_tracks
