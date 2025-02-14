from S3 import fetch_from_es_drei
from LaboratoriumDiscounter import fetch_from_lab_dis
from Onyxmet import fetch_from_onyxmet
from LabChem import fetch_from_lab_chem
from translateChem import translate
from rich.console import Console
from rich.panel import Panel
import requests
import json
import re
from rich.progress import Progress

def main():
    print("Enter Chemical Name:")
    chem = input("> ")

    # List of supplier functions
    supplier_properties = {
        "es_drei": [fetch_from_es_drei, "de"],
        "lab_dis": [fetch_from_lab_dis, "original"],
        "onyxmet": [fetch_from_onyxmet, "original"],
        "labchem": [fetch_from_lab_chem, "de"]
    }

    combined_name_list = []
    combined_price_list = []
    combined_supplier_name_list = []
    combined_location_list = []
    combined_url_list = []

    console = Console()

    with Progress(console=console) as progress:
        task = progress.add_task("[cyan]Searching.. ", total=len(supplier_fetchers))

        # Automatically call each fetch function and update progressbar
        for supplier, fetch_and_language in supplier_properties.items():
            if fetch_and_language[1] != "original":
                name_list, price_list, supplier_name_list, location_list, url_list = fetch_and_language[0](translate(chem, fetch_and_language[1]))
            else:
                name_list, price_list, supplier_name_list, location_list, url_list = fetch_and_language[0](chem)
            progress.update(task, advance=1)
            combined_name_list.append(name_list)
            combined_price_list.append(price_list)
            combined_supplier_name_list.append(supplier_name_list)
            combined_location_list.append(location_list)
            combined_url_list.append(url_list)

    # Display results
    for name_list, price_list, supplier_name, location, url in zip(combined_name_list, combined_price_list, combined_supplier_name_list, combined_location_list, combined_url_list):
        for name, price in zip(name_list, price_list,):
            panel = Panel(f"[yellow][b]{name}[/b][/yellow]\nPrice: {price}\nSupplier: {supplier_name}\nLocation: {location}\nURL: {url}", expand=True)
            console.print(panel)

if __name__ == "__main__":
    main()
    input("")