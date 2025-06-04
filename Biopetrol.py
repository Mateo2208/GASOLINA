import requests
from bs4 import BeautifulSoup
import json

def scrape_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Error al obtener la página:", response.status_code)
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    data = []

    branches = soup.find_all("div", class_="btn-bio-app")
    for branch in branches:
        # Nombre de la sucursal
        name_div = branch.find("div", class_="rounded-top")
        branch_name = name_div.get_text(strip=True) if name_div else "Sin nombre"

        volume_divs = branch.find_all("div", class_="text-right")
        litros = None
        for div in volume_divs:
            text = div.get_text(strip=True)
            if "Lts" in text:
                litros = text
                break

        data.append({
            "sucursal": branch_name,
            "litros": litros
        })

    return data

if __name__ == "__main__":
    url = "http://ec2-3-22-240-207.us-east-2.compute.amazonaws.com/guiasaldos/main/donde/134"
    resultado = scrape_data(url)

    if resultado is not None:
        print(json.dumps(resultado, indent=4, ensure_ascii=False))
