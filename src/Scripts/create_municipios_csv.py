import csv
import requests

url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to fetch data: {response.status_code}")
municipios = response.json()

filepath = "./Scripts/CSVs/"
filename = "municipios.csv"

with open(filepath + filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "name", "uf"])
    
    for municipio in municipios:
        try:     
            id: int = municipio["id"]
            name: str = municipio["nome"]
            uf: str = municipio["microrregiao"]["mesorregiao"]["UF"]["sigla"]
        except (KeyError, TypeError):
            print(f"municipio: {municipio} caiu no except, tratando erro")
            uf = municipio["regiao-imediata"]["regiao-intermediaria"]["UF"]["sigla"]
            continue
        print(f"Codigo: {id}, Municipio: {name}, UF: {uf}")
        writer.writerow([id, name, uf])
        
print(f"Arquivo {filename} criado com sucesso")
        
