import requests
import json
from colorama import init, Fore
from json.decoder import JSONDecodeError

init(autoreset=True)

# Headers, Url, Token
url = "http://localhost:8000/api/v1/ies/"
token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzU5Mzc1NTIzLCJpYXQiOjE3NTkyODkxMjMsInN1YiI6IjEifQ.6VJ14MlKWjbSzoOPaZ5EDmg8kB3nL8bv_Wwh455xIxI"
headers = {
    "Authorization": f"Bearer {token}"
}
    
with open("src/Scripts/json/universidades.json", "r", encoding="utf-8") as file:
    list_ies = json.load(file)                    
    
    for ies in list_ies:
        
        if ies.get('city_id') == "":
            ies['city_id'] = None
            continue
        else:
            ies['city_id'] = int(ies['city_id'])
            
        response = requests.post(url, json=ies, headers=headers)
        if response.status_code == 201:
            print(f"{Fore.MAGENTA}msg:{Fore.WHITE} Ies {Fore.CYAN}{ies['name']}{Fore.WHITE} added successfully - Status: {Fore.GREEN}{response.status_code}")
        else:
            print(f"{Fore.MAGENTA}msg:{Fore.WHITE} Failed to add Ies {Fore.CYAN}{ies['name']}{Fore.WHITE} - Status: {Fore.RED}{response.status_code} - {Fore.YELLOW}{response.text}")