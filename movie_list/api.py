import requests

BASE_URL = 'https://ghibliapi.herokuapp.com'

def get_data(path):
    raw_results = requests.get(BASE_URL + path)
    if raw_results.status_code == 200:
        return raw_results.json()
