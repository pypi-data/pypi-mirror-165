import requests


def getDefinition(word: str) -> str:
    """Returns the first definition of the given word.
    Returns None if the word does not exist.
    """
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url, timeout=10)
    if response.status_code == 404:
        return None

    responseJson = response.json()
    return responseJson[0]["meanings"][0]["definitions"][0]["definition"]
