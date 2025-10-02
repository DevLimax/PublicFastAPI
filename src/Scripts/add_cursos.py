import csv
import requests
from colorama import Fore, init

url = "http://127.0.0.1:8000/api/v1/courses/"
token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzU5Mzc1NTIzLCJpYXQiOjE3NTkyODkxMjMsInN1YiI6IjEifQ.6VJ14MlKWjbSzoOPaZ5EDmg8kB3nL8bv_Wwh455xIxI"
filepath = "src/Scripts/CSVs/courses_extracted.csv"
data_list = []
headers = {
        "Authorization": f"Bearer {token}"
    }

init(autoreset=True)

with open(filepath, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        if row["GRAU"] == "Tecnológico":
            row["GRAU"] = "Tecnologo"
            
        elif row["GRAU"] == "Área Básica de Ingresso (ABI)":
            row["GRAU"] = "ABI"
        
        data = {
            "name": row["NOME_CURSO"],
            "academic_degree": row["GRAU"],
            "area_ocde": row["AREA_OCDE"],
            "workload": row["CARGA_HORARIA"]
        }
        data_list.append(data)

def post_course(data: dict):
        try:
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 201:
                print(f"{Fore.BLUE}msg{Fore.WHITE}: Instancia ({Fore.YELLOW}{response.json().get('id')} - {response.json().get('name')}) {Fore.WHITE}Criada - Status:{Fore.GREEN}{response.status_code}")

            elif response.status_code == 400:
                print(Fore.YELLOW + "⚠️ Erro de validação! Verifique os dados enviados.")
                try:
                    print("Detalhes:", data, response.json())
                except ValueError:
                    print("Detalhes (texto):", response.text)

            elif response.status_code == 409:
                print(f"{Fore.BLUE}msg{Fore.WHITE}: Instancia já cadastrada - Status:{Fore.YELLOW}{response.status_code}")

            else:
                print(f"{Fore.BLUE}msg{Fore.WHITE}: Erro ao criar instancia ({data.get('name')}) - Status:{Fore.RED}{response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"{Fore.BLUE}msg{Fore.WHITE}: Erro de conexão - {Fore.RED}{e}")
        except Exception as e:
            print(f"{Fore.BLUE}msg{Fore.WHITE}: Erro inesperado - {Fore.RED}{e}")

for data in data_list:
    post_course(data=data)

print("Cursos Adicionados com sucesso!")
