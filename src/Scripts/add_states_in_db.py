import requests
import csv

filepath = 'src/Scripts/CSVs/states.csv'
url = "http://localhost:8000/api/v1/states/"
token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzU4ODQ4NTU5LCJpYXQiOjE3NTg3NjIxNTksInN1YiI6IjIifQ.iZeTyptkjsfS3aF-Yh4XxHzk006AM7EkBuZrH4TiSDE"
        
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
            
