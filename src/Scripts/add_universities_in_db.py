import csv
import requests
from googlesearch import search
from colorama import Fore, init
import asyncio

init(autoreset=True)

url = "http://localhost:8000/api/v1/universities/"
filepath = "./Scripts/CSVs/ies_publics.csv"

async def get_site_link(name, results=2):
    query = name
    results = list(search(query, num_results=results, lang="pt-BR", timeout=15))    
    for result in results:
        if result.startswith("https://") and "br" in result:
            print(f"Retornando link referente a pesquisa: {Fore.YELLOW}{name}{Fore.WHITE} - {Fore.YELLOW}{result}")
            return result    
    print("Não foi possivel encontrar o link referente a pesquisa:", {Fore.YELLOW}, name)
    return None

async def get_states_id(uf: str = "", municipio: str = "", codigo_ibge: int = None):
    url = f"http://127.0.0.1:8000/api/v1/states/?uf={uf}&citie={municipio}"
    if codigo_ibge:
        try:
            int(codigo_ibge)
            url = url + f"&codigo_ibge={codigo_ibge}"
        except ValueError:
            print(f"codigo_ibge: {codigo_ibge} nao eh um inteiro")     
        
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

async def post_universities():
    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        for row in reader:  
            data = {
                "id": row["CODIGO_DA_IES"],
                "name": row["NOME_DA_IES"],
                "abbreviation": row["SIGLA"],
                "is_active": [True if row["SITUACAO_IES"] == "Ativa" else False],
                "state": await get_states_id(uf=row["UF"], municipio=row["MUNICIPIO"], codigo_ibge=row["CODIGO_MUNICIPIO_IBGE"]),
                "site":  await get_site_link(row["NOME_DA_IES"])
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
    asyncio.run(post_universities())