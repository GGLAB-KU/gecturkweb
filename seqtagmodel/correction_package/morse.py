from functools import lru_cache

import requests


class Morse():
    def __init__(self):
        pass

    @lru_cache(maxsize=128)
    def analyze(self, text):
        data = data = "{\"text\": \"%s\"}" % text
        data = data.encode()
        result = requests.post("http://localhost:8080/analyze/", data, headers={"Auth-Token": "sometoken"})

        return result.json()["analysis"]
