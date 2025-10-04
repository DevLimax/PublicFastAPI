import csv

filepath = "src/Scripts/CSVs/courses.csv"

seen_codes = set()
unique_rows = []

with open(filepath, "r", encoding="utf-8") as file_in:
    reader = csv.DictReader(file_in)

    for row in reader:
        code_course = row["CODIGO_CURSO"]
        if code_course not in seen_codes and "Pública" in row["CATEGORIA_ADMINISTRATIVA"]:
            seen_codes.add(code_course)
            unique_rows.append(row)
        
with open("src/Scripts/CSVs/courses_extracted.csv", "a", newline="", encoding="utf-8") as file_out:
    writer = csv.writer(file_out)
    if file_out.tell() == 0:
        writer.writerow(["CODIGO_CURSO", "NOME_CURSO", "GRAU", "AREA_OCDE", "CODIGO_IES"])
        
    for row in unique_rows:
        writer.writerow([row["CODIGO_CURSO"], row["NOME_CURSO"], row["GRAU"], row["AREA_OCDE"], row["CODIGO_IES"]])
        
print("CSV extracted successfully!")

