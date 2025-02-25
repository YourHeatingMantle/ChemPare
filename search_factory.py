import os
import sys
import re
from typing import List, Set, Tuple, Dict, Any, Optional
from curl_cffi import requests
from abcplus import finalmethod
from class_utils import ClassUtils
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import suppliers

class SearchFactory(ClassUtils, object):
    suppliers: list = suppliers.__all__
    """suppliers property lets scripts call 'SearchFactory.suppliers' to get a list of suppliers"""

    __results: list = []
    """Contains a list of all the product results"""

    __index: int = 0
    """Index used for __iter__ iterations"""

    def __init__(self, query: str, limit: int=3):
        """Factory method for executing a search in all suppliers automatically

        Args:
            query (str): Search query
            limit (int, optional): Limit results to this. Defaults to 3.
        """
        self.__query(query, limit)

    def __iter__(self):
        return self

    def __next__(self):
        """Next dunder method for for loop iterations

        Raises:
            StopIteration: When the results are done

        Returns:
            TypeProduct: Individual products
        """

        if self.__index >= len(self.__results):
            raise StopIteration
        value = self.__results[self.__index]
        self.__index += 1
        return value
    
    def __query(self, query: str, limit: int=None):
        """Iterates over the suppliers, running the query, then returning the results.

        Args:
            query (str): Search query
            limit (int, optional): Amount to limit the search by. Defaults to None.
        """

        query_is_cas = self._is_cas(query)

        # Get both the chemical name and CAS values for searches, to avoid having to make
        # the same HTTP calls to cactus.nci.nih.gov several times
        if query_is_cas is True:
            query_cas = query
            # Use self.__get_name() to get the IUPAC name.
            # Example: '67-64-1' yields 'propan-2-one'
            #query_name = self.__get_name(query) or query

            # Use self.__get_popular_name(query) to try and determine the most common name.
            # Example: '67-64-1' yields 'acetone'
            query_name = self.__get_popular_name(query) or query
        else:
            query_cas = self.__get_cas(query) or query
            query_name = query

        # Iterate over the modules in the suppliers package
        for supplier in suppliers.__all__:
            # Create a direct reference to this supplier class
            supplier_module = getattr(suppliers, supplier)
            supplier_query = query

            # If the supplier allows a CAS search and the current value isn't a CAS number...
            if supplier_module.allow_cas_search is True and query_is_cas is False:
                # ... Then do a lookup to get the CAS number
                supplier_query = query_cas
            # If the supplier does not allow CAS searches, but were searching by CAS..
            elif supplier_module.allow_cas_search is False and query_is_cas is True:
                # ... Then try to lookup the name for this
                supplier_query = query_name
               
            if __debug__:
                print(f'Searching for {supplier_query} from {supplier_module.__name__}...')

            # Execute a search by initializing an instance of the supplier class with
            # the product query term as the first param
            res = supplier_module(supplier_query, limit)
            if not res:
                if supplier_module.allow_cas_search is True:
                    res = supplier_module(query_name, limit)
                    print(f'Searching for {query_name} from {supplier_module.__name__}...')
                if not res:
                    if __debug__:
                        print('  No results found\n')
                    next
            
            if __debug__:
                print(f'  found {len(res.products)} products\n')

            # If there were some results found, then extend the self.__results list with those products
            self.__results.extend(res.products)
    
    def __get_cas(self, chem_name:str) -> Optional[str]:
        """Search for the CAS value(s) given a chemical name

        Args:
            chem_name (str): Name of chemical to search for

        Returns:
            Optional[str]: CAS value of chemical
        """

        cas = None
        try:
            # Send a GET request to the API
            cas_request = requests.get(f'https://cactus.nci.nih.gov/chemical/structure/{chem_name}/cas')
            # Check if the request was successful
            if cas_request.status_code != 200:
                return None
            
            # Decode the bytes to a string
            cas_response = cas_request.content.decode('utf-8')  

            if not cas_response:
                return None

            cas_list = cas_response.split('\n') 
            cas = cas_list[0] 
        except:
            print('Failed to get CAS #')
        finally:
            return cas      

        # # Should only be one line/value, so just strip it before returning, if a value was found
        # return str(cas_response).strip() if cas_response else None
       
    def __get_name(self, cas_no:str) -> Optional[str]:
        """Search for a chemical name given a CAS #

        Args:
            cas_no (str): CAS #

        Returns:
            Optional[str]: IUPAC name
        """
           
        # Send a GET request to the API
        name_request = requests.get(f'https://cactus.nci.nih.gov/chemical/structure/{cas_no}/iupac_name')
        
        # Check if the request was successful
        if name_request.status_code != 200:
            return f"Error: {name_request.status_code}"
        
        name_response = name_request.content.decode('utf-8')  # Decode the bytes to a string
        name_lines = name_response.split('\n')  # Split by newline
            
        # Do we want the first value?
        return name_lines[0]
  
    
    def __get_popular_name(self, query:str) -> str:
        """Get the most frequently used name for a chemical from a list of its aliases

        Args:
            query (str): Chemical name or CAS

        Returns:
            str: The most frequently found name
        """
        # Send a GET request to the API
        name_request = requests.get(f'https://cactus.nci.nih.gov/chemical/structure/{query}/names')
        
        # Check if the request was successful
        if name_request.status_code != 200:
            raise SystemError(f"Error: {name_request.status_code}")
        
        name_response = name_request.content.decode('utf-8')  # Decode the bytes to a string
        name_lines = name_response.split('\n')  # Split by newline

        highest_val = self.__filter_highest_value(self.__get_common_phrases(name_lines))

        keys = list(highest_val.keys())
        return keys[0][0]

    def __filter_highest_value(self, input_dict:Dict) -> Dict:
        """Filter a dictionary for the entry with the highest numerical value.

        Args:
            input_dict (Dict): Dictionary to iterate through

        Returns:
            Dict: Item in dictionary with highest value
        """
        if not input_dict:
            return {}
        max_value = max(input_dict.values())
        return {k: v for k, v in input_dict.items() if v == max_value}
    
    def __get_common_phrases(self, texts:list, maximum_length:int=3, minimum_repeat:int=2, stopwords:list=[]) -> dict:
        """Get the most common phrases out of a list of phrases.

        This is used to analyze the results from a query to https://cactus.nci.nih.gov/chemical/structure/{NAME OR CAS}/names
        to find the most common term used in the results. This term may yield better search results on some sites.

        Source:
            https://dev.to/mattschwartz/quickly-find-common-phrases-in-a-large-list-of-strings-9in

        Args:
            texts (list): Array of text values to analyze
            maximum_length (int, optional): Maximum length of phrse. Defaults to 3.
            minimum_repeat (int, optional): Minimum length of phrse. Defaults to 2.
            stopwords (list, optional): Phrases to exclude. Defaults to [].

        Returns:
            dict: Dictionary of sets of words and the frequency as the value.
        """

        phrases = {}
        for text in texts:
            # Replace separators and punctuation with spaces
            text = re.sub(r'[.!?,:;/\-\s]', ' ', text)
            # Remove extraneous chars
            text = re.sub(r'[\\|@#$&~%\(\)*\"]', '', text)

            words = text.split(' ')
            # Remove stop words and empty strings
            words = [w for w in words if len(w) and w.lower() not in stopwords]
            length = len(words)
            # Look at phrases no longer than maximum_length words long
            size = length if length <= maximum_length else maximum_length
            while size > 0:
                pos = 0
                # Walk over all sets of words
                while pos + size <= length:
                    phrase = words[pos:pos+size]
                    phrase = tuple(w.lower() for w in phrase)
                    if phrase in phrases:
                        phrases[phrase] += 1
                    else:
                        phrases[phrase] = 1
                    pos += 1
                size -= 1

        phrases = {k: v for k, v in phrases.items() if v >= minimum_repeat}

        longest_phrases = {}
        keys = list(phrases.keys())
        keys.sort(key=len, reverse=True)
        for phrase in keys:
            found = False
            for l_phrase in longest_phrases:
                intersection = set(l_phrase).intersection(phrase)
                if len(intersection) != len(phrase):
                    next

                # If the entire phrase is found in a longer tuple...
                # ... and their frequency overlaps by 75% or more, we'll drop it
                difference = (phrases[phrase] - longest_phrases[l_phrase]) / longest_phrases[l_phrase]
                if difference < 0.25:
                    found = True
                    break
            if not found:
                longest_phrases[phrase] = phrases[phrase]

        return longest_phrases

    @property
    @finalmethod 
    def results(self):
        """Results getter"""
        return self.__results