import requests
import re
import json

url = "https://docs.google.com/spreadsheets/u/0/d/e/2CAIWO3els60V5S1vVAh0cccQxdcZ1MYZhD9A1pQ-ojCNPoNh-vJjHhJaUalVsDLQivYf_Z23Un8mEaePxSg/gviz/chartiframe?oid=970629425&resourcekey"

response = requests.get(url)
if response.status_code != 200:
    print("Error al obtener la página:", response.status_code)
    exit()
text = response.text

match = re.search(r"google\.visualization\.Query\.setResponse\((.*)\);", text, re.DOTALL)
if not match:
    print("No se pudo extraer el JSON de la respuesta.")
    exit()

json_str = match.group(1)

data = json.loads(json_str)

cols = data.get("table", {}).get("cols", [])
rows = data.get("table", {}).get("rows", [])

headers = [col.get("label", "") for col in cols]
print("Encabezados:")
print(headers)
print("-" * 40)

for row in rows:
    cells = row.get("c", [])
    values = [cell.get("v", "") if cell is not None else "" for cell in cells]
    print(values)
