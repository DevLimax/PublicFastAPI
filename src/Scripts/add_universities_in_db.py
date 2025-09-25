import csv
import requests
from googlesearch import search
from colorama import Fore, init

init(autoreset=True)

url = "http://localhost:8000/api/v1/ies/"
filepath = "src/Scripts/CSVs/ies_publics.csv"
token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzU4ODkwNzAxLCJpYXQiOjE3NTg4MDQzMDEsInN1YiI6IjEifQ.CqwWUCV-lIANSasd9TStcwGh3ZHmKA5kHNQGkA-lVbs"

def get_site_link(name, results=2):
    query = name
    results = list(search(query, num_results=results, lang="pt-BR"))    
    for result in results:
        print(f"Retornando link referente a pesquisa:{Fore.YELLOW}{name}{Fore.WHITE} - {Fore.YELLOW}{result}")
        return result  
          
    print("Não foi possivel encontrar o link referente a pesquisa:", Fore.YELLOW , name)
    print("Links encontrados:", Fore.YELLOW, results)
    return None

def get_states_id(uf: str = None, municipio: str = None):
    url = f"http://localhost:8000/api/v1/states/?uf={uf}&city={municipio}"   
    response_get_states = requests.get(url=url)
    
    if response_get_states.status_code != 200:
        print(f"Erro ao buscar estado referente ao municipio: {municipio} - Status:{response_get_states.status_code} - {response_get_states.text}")
        return None    
    if response_get_states.json() == []:
        print("Nao foi possivel encontrar o estado referente ao municipio:", Fore.YELLOW + municipio)
        return None
    state_id = response_get_states.json()[0]["id"]
    print(f"Estado encontrado:", Fore.BLUE + response_get_states.json()[0]["name"])
    return state_id

def post_universities():
    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        for row in reader:  
            data = {
                "id": row["CODIGO_DA_IES"],
                "name": row["NOME_DA_IES"],
                "abbreviation": row["SIGLA"],
                "is_active": [True if row["SITUACAO_IES"] == "Ativa" else False],
                "state_id": get_states_id(uf=row["UF"], municipio=row["MUNICIPIO"]),
                "site":  get_site_link(name=row["NOME_DA_IES"])
            }
            
            try:
                response = requests.post(url, json=data)
                if response.status_code == 201:
                    print(f"{Fore.MAGENTA}msg:{Fore.WHITE} University {Fore.CYAN}{row['NOME_DA_IES']}{Fore.WHITE} added successfully - Status: {Fore.GREEN}{response.status_code}")
                elif response.status_code == 500:
                    print(f"{Fore.MAGENTA}msg:{Fore.WHITE} Internal Server Error - Status: {Fore.RED}{response.status_code}")
                else:
                    print(f"{Fore.MAGENTA}msg:{Fore.WHITE} Failed to add university {Fore.CYAN}{row['NOME_DA_IES']}{Fore.WHITE} - Status: {Fore.RED}{response.status_code} - {Fore.YELLOW}{response.text}")
            except Exception as e:
                print(f"{Fore.MAGENTA}msg:{Fore.WHITE} Erro de conexão - {Fore.RED}{e}")
                   
if __name__ == "__main__":
    post_universities()