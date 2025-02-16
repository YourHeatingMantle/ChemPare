import requests
from bs4 import BeautifulSoup

name_list = []
price_list = []
supplier_name = "Onyxmet"
location = "Poland"
url = ""

def fetch_from_onyxmet(chem):

    cookies = {
        # Removing the cookie, since hopefully it won't be needed
        #'OCSESSID': 'e7d2642d83310cfc58135d2914',
        'language': 'en-gb',
        'currency': 'USD',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.7',
        # 'cookie': 'OCSESSID=e7d2642d83310cfc58135d2914; language=en-gb; currency=USD',
        'priority': 'u=0, i',
        'referer': 'https://onyxmet.com/',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

    search_query_params = {
        'route':'product/search/json',
        'term': chem
    }

    url = "https://onyxmet.com/index.php?route=product/search&search=" + chem

    # Send the initial search request (this returns JSON)
    search_request = requests.get('https://onyxmet.com/index.php', cookies=cookies, headers=headers, params=search_query_params)

    # Get the JSON
    search_response = search_request.json()

    # Check each product
    for product in search_response:

        # Limit search to only the first 3 products
        if product == search_response[0] or product == search_response[1] or product == search_response[2]:

            # Send the second request using the hyperlink found in the search response (this returns HTML)
            product_request = requests.get(product['href'], cookies=cookies, headers=headers)

            # Get the product page HTML
            product_response = product_request.text

            # Chicken soup for the soul
            product_soup = BeautifulSoup(product_response, 'html.parser')

            # Since we know the element is a <h3 class=product-price /> element, search for H3's
            h3_elems = product_soup.find_all('h3')  

            # Find the one with the 'product-price' class
            price_elem = next(obj for obj in h3_elems if 'product-price' in obj.get('class'))

            # TODO: I'm sure there's an easier way to just specifically look for the 'h3.product-price' element,
            #       instead of _all_ h3 elements then filtering the results for one that has the 'product-price'
            #       class... But I'll leave that optimization up to you :-)

            if not price_elem:
                raise Exception("No price found")

            product_price = price_elem.contents[0]

            # Add product name, product price and product url to their corresponding lists
            name_list.append(product['label'])
            price_list.append(product_price)

    return name_list, price_list, supplier_name, location, url