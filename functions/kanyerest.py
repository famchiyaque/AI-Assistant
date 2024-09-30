import requests

def get_kanye_quote():
    response = requests.get('https://api.kanye.rest/')
    if response.status_code == 200:
        quote = response.json()['quote']
        return quote
    else:
        return "kanye rest api didn't work"
