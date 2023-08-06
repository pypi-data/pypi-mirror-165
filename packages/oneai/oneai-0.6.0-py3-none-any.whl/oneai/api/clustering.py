import json
import requests
import oneai, oneai.api


ENDPOINT = "clustering/v1/collections"


def get_clustering(path: str, api_key: str = None):
    api_key = api_key or oneai.api_key
    if not api_key:
        raise Exception("API key is required")
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
        "User-Agent": f"python-sdk/{oneai.__version__}/{oneai.api.uuid}",
    }
    response = requests.get(
        f"{oneai.URL}/{ENDPOINT}/{path}",
        headers=headers,
    )
    return json.loads(response.content)


def post_clustering(path: str, data: dict, api_key: str = None):
    api_key = api_key or oneai.api_key
    if not api_key:
        raise Exception("API key is required")
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
        "User-Agent": f"python-sdk/{oneai.__version__}/{oneai.api.uuid}",
    }
    response = requests.post(
        f"{oneai.URL}/{ENDPOINT}/{path}", headers=headers, json=data
    )
    return json.loads(response.content)
