import requests
import json
from colorama import init, Fore

init(autoreset=True)

# Headers, Url, Token
url = "http://localhost:8000/api/v1/ies/"
token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzU4OTMxNjg2LCJpYXQiOjE3NTg4NDUyODYsInN1YiI6IjIifQ.hh0Ax9LWQLcb8XxKHoFjpGCVO1zbeA8rr5zfDWtRQ9w"
headers = {
    "Authorization": f"Bearer {token}"
}

with open("src/Scripts/json/universidades.json", "r", encoding="utf-8") as file:
    list_ies = json.load(file)

    for ies in list_ies:
        response = requests.post(url, json=ies, headers=headers)

        if response.status_code == 201:
            print(f"Universidade: {Fore.BLUE}{ies.get('name')}{Fore.WHITE} Adicionada com Sucesso - {Fore.YELLOW}Status:{Fore.GREEN}{response.status_code}")
        else:
            print(f"Error ao adicionar Universidade: {Fore.BLUE}{ies.get('name')}{Fore.WHITE} - {Fore.YELLOW}Status:{Fore.RED}{response.status_code}")
            print(f"Resposta: {Fore.YELLOW}{response.text}")
    
    print("Finalizado o Script")