import requests
import json
from colorama import init, Fore
from json.decoder import JSONDecodeError

init(autoreset=True)

# Headers, Url, Token
url = "http://localhost:8000/api/v1/ies/"
token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzU4OTg3NDg2LCJpYXQiOjE3NTg5MDEwODYsInN1YiI6IjEifQ.vZTCK7EZqOZzg0pGXRvC_eN0xJEHltzjSae8rsIlA9E"
headers = {
    "Authorization": f"Bearer {token}"
}

def get_id_state(municipio_id: int):
    url = f"http://localhost:8000/api/v1/states/?city_code={municipio_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erro ao buscar estado referente ao municipio: {municipio_id} - Status:{response.status_code} - {response.text}")
        return None
    
    states_data = response.json()
    state_id = states_data[0].get("id")
    return state_id
    
with open("src/Scripts/json/universidades.json", "r", encoding="utf-8") as file:
    list_ies = json.load(file)                    
    
    for ies in list_ies:
        ies['state_id'] = get_id_state(municipio_id=ies['city_id'])
        
        if ies['state_id'] == None:
            print(f"Estado não encontrado, Ies {ies['name']} não sera adicionada ao banco")
            
        else:
            response = requests.post(url, json=ies, headers=headers)
            if response.status_code == 201:
                print(f"{Fore.MAGENTA}msg:{Fore.WHITE} Ies {Fore.CYAN}{ies['name']}{Fore.WHITE} added successfully - Status: {Fore.GREEN}{response.status_code}")
            else:
                print(f"{Fore.MAGENTA}msg:{Fore.WHITE} Failed to add Ies {Fore.CYAN}{ies['name']}{Fore.WHITE} - Status: {Fore.RED}{response.status_code} - {Fore.YELLOW}{response.text}")