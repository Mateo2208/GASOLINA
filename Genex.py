import requests
from bs4 import BeautifulSoup

url = "https://genex.com.bo/estaciones/?2729_product_cat%5B0%5D=289&2729_filtered=true"

response = requests.get(url)
if response.status_code != 200:
    print("Error al obtener la página:", response.status_code)
    exit()

soup = BeautifulSoup(response.text, "html.parser")

rows = soup.find_all("tr", attrs={"data-wcpt-product-id": True})

for row in rows:
    branch_td = row.find("td", attrs={"data-wcpt-column-index": "1"})
    branch_name = "N/D"
    if branch_td:
        custom_field = branch_td.find("div", class_="wcpt-custom-field")
        if custom_field:
            branch_name = custom_field.get_text(strip=True)
    
    availability_td = row.find("td", attrs={"data-wcpt-column-index": "2"})
    fuel_availability = {}
    if availability_td:
        item_rows = availability_td.find_all("div", class_="wcpt-item-row")
        for item in item_rows:
            spans = item.find_all("span", class_="wcpt-text")
            if len(spans) >= 2:
                fuel_type = spans[0].get_text(strip=True)
                status = spans[1].get_text(strip=True)
                fuel_availability[fuel_type] = status

    print(f"Sucursal: {branch_name}")
    if fuel_availability:
        for fuel, status in fuel_availability.items():
            print(f"   {fuel}: {status}")
    else:
        print("   No se encontró información de disponibilidad.")
    print("-" * 40)
