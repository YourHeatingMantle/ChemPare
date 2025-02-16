import requests

def fetch_from_lab_dis(chem):
    name_list = []
    price_list = []
    supplier_name = "Laboratoriumdiscounter"
    location = "The Netherlands"

    response = requests.get(f'https://www.laboratoriumdiscounter.nl/en/search/{chem}/page1.ajax', params={'limit':100})
    response_json = response.json()
    for product in response_json['products'][:3]:
        name_list.append(product['title'])
        price_list.append(product['price']['price'])

    return name_list, price_list, supplier_name, location, 'https://www.laboratoriumdiscounter.nl/en/search/' + chem

fetch_from_lab_dis('toluene')