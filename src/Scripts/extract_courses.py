import csv

filepath = "./Scripts/CSVs/courses.csv"

seen_names = set()
unique_rows = []

with open(filepath, "r", encoding="utf-8") as file_in:
    reader = csv.DictReader(file_in)

    for row in reader:
        name_course = row["NOME_CURSO"]
        if name_course not in seen_names:
            seen_names.add(name_course)
            unique_rows.append(row)
        
with open("./Scripts/CSVs/courses_extracted.csv", "a", newline="", encoding="utf-8") as file_out:
    writer = csv.writer(file_out)
    if file_out.tell() == 0:
        writer.writerow(["NOME_CURSO", "GRAU", "AREA_OCDE", "CARGA_HORARIA"])
        
    for row in unique_rows:
        writer.writerow([row["NOME_CURSO"], row["GRAU"], row["AREA_OCDE"], row["CARGA_HORARIA"]])

print("CSV extracted successfully!")

