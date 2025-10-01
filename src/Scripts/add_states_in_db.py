import requests
import csv

filepath = 'src/Scripts/CSVs/states.csv'
url = "http://localhost:8000/api/v1/states/"
token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzU5Mzc1NTIzLCJpYXQiOjE3NTkyODkxMjMsInN1YiI6IjEifQ.6VJ14MlKWjbSzoOPaZ5EDmg8kB3nL8bv_Wwh455xIxI"
        
with open(filepath, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    for row in reader:
        body = {
            "name": row["name"],
            "uf": row["uf"]
        }
        response = requests.post(url, json=body, headers=headers)
        if response.status_code == 201:
            print(f"msg: Instancia criada - {response.json()}")
            
        else:
            print(f"msg: Erro ao criar instancia - {response.json()}")
            
