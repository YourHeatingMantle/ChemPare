import requests
from bs4 import BeautifulSoup

def fetch_from_es_drei(chem):
    name_list = []
    price_list = []
    supplier_name = "S3 Chemicals"
    location = "Germany"

    url = f"https://shop.es-drei.de/search?sSearch={chem}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        # Find all product names and prices
        names = soup.find_all("a", class_="product--title", limit=3)
        prices = soup.find_all("span", class_="price--default is--nowrap", limit=3)

        # Extract names and prices
        for i in range(min(len(names), len(prices))):
            name_list.append(names[i].text.strip())
            price_list.append(prices[i].text.strip())
    except AttributeError:
        pass  # Handle cases where elements are not found

    return name_list, price_list, supplier_name, location, url
    