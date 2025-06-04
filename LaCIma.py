import re

def extraer_litros_y_hora(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    resultados = []
    fecha_hora_actual = ""

    for i, linea in enumerate(lineas):
        match_fecha = re.match(r"\[\d{1,2}/\d{1,2}/\d{2,4}, \d{2}:\d{2}:\d{2}\]", linea)
        if match_fecha:
            fecha_hora_actual = match_fecha.group().strip("[]")
        match_litros = re.findall(r"(\d{1,3}(?:,\d{3})*|\d+)[\s\n]*LTS", linea.upper())
        for cantidad in match_litros:
            litros = int(cantidad.replace(",", ""))
            resultados.append({
                "fecha_hora": fecha_hora_actual,
                "litros": litros
            })

    return resultados

# === USO ===
if __name__ == "__main__":
    datos = extraer_litros_y_hora("chat.txt")
    for d in datos:
        print(f"{d['fecha_hora']}: {d['litros']} LTS")
