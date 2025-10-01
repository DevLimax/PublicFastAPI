import requests
import csv
from colorama import Fore, init
from json.decoder import JSONDecodeError

init(autoreset=True)

url = "http://127.0.0.1:8000/api/v1/cities/"
filepath = "src/Scripts/CSVs/municipios.csv"
token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzU5Mzc1NTIzLCJpYXQiOjE3NTkyODkxMjMsInN1YiI6IjEifQ.6VJ14MlKWjbSzoOPaZ5EDmg8kB3nL8bv_Wwh455xIxI"
        
with open(filepath, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    for row in reader:
        response_get_states = requests.get(f"http://127.0.0.1:8000/api/v1/states/?uf={row['uf']}")
        try:
            states_data = response_get_states.json()
        except JSONDecodeError:
            print(f"Erro ao buscar estado referente ao municipio: {row['name']} - Status:{response_get_states.status_code} - {response_get_states.text}")
            states_data = None
            continue
        
        if states_data:
            state_id = states_data[0]['id']
            
            data = {
                "id": row["id"],
                "name": row["name"],
                "state_id": state_id
            }
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 201:
                print(f"{Fore.MAGENTA}msg:{Fore.WHITE} City {Fore.CYAN}{row['name']}{Fore.WHITE} added successfully - Status: {Fore.GREEN}{response.status_code}")
            else:
                print(f"{Fore.MAGENTA}msg:{Fore.WHITE} Failed to add city {Fore.CYAN}{row['name']}{Fore.WHITE} - Status: {Fore.RED}{response.status_code} - {Fore.YELLOW}{response.text}")
                
        else:
            print("Estado não encontrado para UF:", row['uf'])
                
