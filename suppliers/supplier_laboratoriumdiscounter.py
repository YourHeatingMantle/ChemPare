from suppliers.supplier_base import SupplierBase, TypeProduct, TypeSupplier
from typing import NoReturn

# File: /suppliers/supplier_laboratoriumdiscounter.py
class SupplierLaboratoriumDiscounter(SupplierBase):

     # Supplier specific data
    _supplier: TypeSupplier = dict(
        name = 'Laboratorium Discounter',
        location = None,
        base_url = 'https://www.laboratoriumdiscounter.nl'
    )

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name searches"""

    # If any extra init logic needs to be called... uncmment the below and add changes
    # def __init__(self, query, limit=123):
    #     super().__init__(id, query, limit)
        # Do extra stuff here

    def _query_products(self, query: str) -> NoReturn:
        """Query products from supplier

        Args:
            query (str): Query string to use
        """

        # Example request url for Laboratorium Discounter
        # https://www.laboratoriumdiscounter.nl/en/search/{search_query}/page1.ajax?limit=100
        #
        get_params = {
            # Setting the limit here to 1000, since the limit parameter should apply to
            # results returned from Supplier3SChem, not the rquests made by it.
            'limit': 1000
        }
        search_result = self.http_get_json(f'en/search/{query}/page1.ajax?', params=get_params)

        if not search_result:
            return

        self._query_results = search_result['products'][0:self._limit]

    # Method iterates over the product query results stored at self._query_results and
    # returns a list of TypeProduct objects.
    def _parse_products(self) -> NoReturn:
        for product in self._query_results:
            # Skip unavailable
            if product['available'] is False:
                continue

            # Add each product to the self._products list in the form of a TypeProduct
            # object.
            quantity = self._parse_quantity(product['title'])

            self._products.append(TypeProduct(
                uuid = str(product['id']).strip(),
                name = product['title'],
                title = product['fulltitle'],
                cas = self._get_cas_from_variant(product['variant']),
                description = str(product['description']).strip() or None,
                price = str(product['price']['price']).strip(),
                currency = product['price']['currency'],
                url = product['url'],
                supplier = self._supplier['name'],
                quantity=quantity['quantity'],
                uom=quantity['uom']
            ))

    """ LABORATORIUMDISCOUNTER SPECIFIC METHODS """

    def _get_cas_from_variant(self, variant: str) -> NoReturn:
        """Get the CAS number from the variant, if applicable

        Args:
            variant (str): Variant string

        Returns:
            str: CAS, if one was found
        """

        variant_dict = self._nested_arr_to_dict(variant.split(','))

        if variant_dict is not None and 'CAS' in variant_dict:
            return variant_dict['CAS']

if __package__ == 'suppliers':
    __disabled__ = False