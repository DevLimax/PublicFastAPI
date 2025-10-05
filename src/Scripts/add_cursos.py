import csv
import requests
from colorama import Fore, init

url = "http://127.0.0.1:8000/api/v1/courses/"
token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzU5NjkzMjMyLCJpYXQiOjE3NTk2MDY4MzIsInN1YiI6IjEifQ.i8pYgu1HDStGzfx5aEfLo7kl6b1-vF4FKIWt5fp7drU"
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
            "id": row.get('CODIGO_CURSO'),
            "name": row.get('NOME_CURSO'),
            "ies_id": row.get('CODIGO_IES'),
            "academic_degree": row.get('GRAU'),
            "area_ocde": row.get('AREA_OCDE'),
        }
        data_list.append(data)

def post_course(data: dict):
        try:
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 201:
                print(f"{Fore.BLUE}msg{Fore.WHITE}: Instancia ({Fore.YELLOW}{response.json().get('id')} - {response.json().get('name')}{Fore.WHITE}) Criada - Status:{Fore.GREEN}{response.status_code}")

            elif response.status_code == 400:
                print(Fore.YELLOW + "⚠️ Erro de validação! Verifique os dados enviados.")
                try:
                    print("Detalhes:", data, response.json())
                except ValueError:
                    print("Detalhes (texto):", response.text)

            elif response.status_code == 409:
                print(f"{Fore.BLUE}msg{Fore.WHITE}: Instancia ({Fore.YELLOW}{data.get('id')}-{data.get('name')}{Fore.WHITE}) já cadastrada - Status:{Fore.YELLOW}{response.status_code}")
            else:
                print(f"{Fore.BLUE}msg{Fore.WHITE}: Erro ao criar instancia ({data.get('name')}) - Status:{Fore.RED}{response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"{Fore.BLUE}msg{Fore.WHITE}: Erro de conexão - {Fore.RED}{e}")
        except Exception as e:
            print(f"{Fore.BLUE}msg{Fore.WHITE}: Erro inesperado - {Fore.RED}{e}")

for data in data_list:
    post_course(data=data)

print("Cursos Adicionados com sucesso!")
