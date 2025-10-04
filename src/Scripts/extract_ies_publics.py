import csv

filepath = "src/Scripts/CSVs/cursos_ies.csv"
with open(filepath, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    list_courses = [row for row in reader if "Pública" in row["CATEGORIA_ADMINISTRATIVA"]]
    print("Extraindo cursos de ies publicas...")
    print(f"Total de cursos: {len(list_courses)}")
    print("Extracao concluida!")
    
with open("src/Scripts/CSVs/courses_ies_extracted.csv", "a", newline="", encoding="utf-8") as file_out:
    writer = csv.writer(file_out)
    if file_out.tell() == 0:
        writer.writerow(["CODIGO_IES", "CODIGO_CURSO", "NOME_CURSO", "GRAU", "AREA_OCDE", "MODALIDADE", "SITUACAO_CURSO", "QT_VAGAS_AUTORIZADAS", "CARGA_HORARIA", "CODIGO_MUNICIPIO"])
        
    for row in list_courses:
        writer.writerow([row["CODIGO_IES"], row["CODIGO_CURSO"], row["NOME_CURSO"], row["GRAU"], row["AREA_OCDE"], row["MODALIDADE"][8:], row["SITUACAO_CURSO"], row["QT_VAGAS_AUTORIZADAS"], row["CARGA_HORARIA"], row["CODIGO_MUNICIPIO"][8:]])
print("CSV extracted successfully!")