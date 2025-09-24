import csv

filepath = "./Scripts/CSVs/instituicoes.csv"
with open(filepath, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    list_ies_publics = [row for row in reader if row["CATEGORIA_DA_IES"] == "Pública" and row["SITUACAO_IES"] == "Ativa"]
    
with open("./Scripts/CSVs/ies_publics.csv", "a", newline="", encoding="utf-8") as file_out:
    writer = csv.writer(file_out)
    if file_out.tell() == 0:
        writer.writerow(["CODIGO_DA_IES","NOME_DA_IES", "SIGLA", "CATEGORIA_DA_IES", "SITUACAO_IES", "CODIGO_MUNICIPIO_IBGE","MUNICIPIO", "UF"])
        
    for row in list_ies_publics:
        writer.writerow([row["CODIGO_DA_IES"], row["NOME_DA_IES"], row["SIGLA"], row["CATEGORIA_DA_IES"], row["SITUACAO_IES"], row["CODIGO_MUNICIPIO_IBGE"][8:], row["MUNICIPIO"], row["UF"]])
        
        
print("CSV extracted successfully!")