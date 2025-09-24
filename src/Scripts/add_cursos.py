import csv
import requests
from colorama import Fore, init

url = "http://127.0.0.1:8000/api/v1/courses/"
filepath = "./Scripts/CSVs/courses_extracted.csv"
data_list = []

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
            "area_knowledge": row["AREA_OCDE"],
            "workload": row["CARGA_HORARIA"]
        }
        data_list.append(data)

def post_course(data):
        try:
            response = requests.post(url, json=data)

            if response.status_code == 201:
                print(f"{Fore.BLUE}msg{Fore.WHITE}: Instancia {Fore.YELLOW}{response.json().get('id')} {Fore.WHITE}Criada - Status:{Fore.GREEN}{response.status_code}")

            elif response.status_code == 400:
                print(Fore.YELLOW + "⚠️ Erro de validação! Verifique os dados enviados.")
                try:
                    print("Detalhes:", data, response.json())
                except ValueError:
                    print("Detalhes (texto):", response.text)

            elif response.status_code == 409:
                print(f"{Fore.BLUE}msg{Fore.WHITE}: Instancia já cadastrada - Status:{Fore.YELLOW}{response.status_code}")

            else:
                print(f"{Fore.BLUE}msg{Fore.WHITE}: Erro ao criar instancia - Status:{Fore.RED}{response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"{Fore.BLUE}msg{Fore.WHITE}: Erro de conexão - {Fore.RED}{e}")
        except Exception as e:
            print(f"{Fore.BLUE}msg{Fore.WHITE}: Erro inesperado - {Fore.RED}{e}")

for data in data_list:
    post_course(data=data)

print("Cursos Adicionados com sucesso!")
