import requests
import csv
import json

# Headers, Url, Token
url = "http://localhost:8080/api/v1/ies/"
token: str = ""
headers = {
    "Authorization": f"Bearer {token}"
}

# Usando Requests na API Django e Resgatando as universidades
url_django = "http://127.0.0.1:8000/api/v1/universities/"
response = requests.get(url_django)

if response.status_code == 200:
    universities = response.json()
    
matched_universities = []
    
with open('src/Scripts/CSVs/ies_publics.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        for university in universities:
            if str(row["NOME_DA_IES"]).lower() == str(university["name"]).lower():
                data = {
                    "id": row.get("CODIGO_DA_IES"),
                    "name": university.get("name"),
                    "abbreviation": university.get("abbreviation"),
                    "type": university.get("type"),
                    "site": university.get("site"),
                    "state_id": int(university.get("state") - 1),
                    "city_id": row.get("CODIGO_MUNICIPIO_IBGE")
                }
                matched_universities.append(data)
                
                
with open("src/Scripts/CSVs/universidades.json", "w", encoding="utf-8") as f:
    json.dump(matched_universities, f, ensure_ascii=False, indent=4)

