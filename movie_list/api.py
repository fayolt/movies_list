import requests

BASE_URL = 'https://ghibliapi.herokuapp.com'


def get_data(path):
    try:
        response = requests.get(BASE_URL + path,  timeout=2)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None
