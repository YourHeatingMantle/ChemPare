#!/usr/bin/env python3
import os
import sys
import pytest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from class_utils import ClassUtils

class TestClass(ClassUtils, object):
    @pytest.mark.parametrize('value,price,currency', [
        ('$123.45','123.45','$'),
        ('123.45 USD','123.45','USD'),
        ('123.45 CAD','123.45', 'CAD'),
        ('$12,345.45','12,345.45','$')
    ])
    def test_parse_price(self, value, price, currency):
        result = self._parse_price(value)
        assert type(result) is dict
        assert 'currency' in result
        assert 'price' in result
        assert result['currency'] == currency
        assert result['price'] == price


    @pytest.mark.parametrize('value,quantity,uom', [
        ('43 ounce','43','ounce'),
        ('4 lb','4','lb'),
        ('5 g','5','g'),
        ('123.45mm','123.45','mm')
    ])
    def test_parse_quantity(self, value, quantity, uom):
        result = self._parse_quantity(value)
        assert type(result) is dict
        assert 'quantity' in result
        assert 'uom' in result
        assert result['quantity'] == quantity
        assert result['uom'] == uom


    @pytest.mark.parametrize('value,param_name,expected_result', [
        ('http://google.com?foo=bar&product_id=12345',None,{'foo':'bar','product_id':'12345'}),
        ('http://google.com?foo=bar&product_id=12345','product_id','12345'),

    ])
    def test_get_param_from_url(self, value, param_name, expected_result):
        result = self._get_param_from_url(value, param_name)
        assert type(result) is type(expected_result)
        assert result == expected_result


    def test_split_array_into_groups(self):
        result = self._split_array_into_groups(['Variant', '500 g', 'CAS', '1762-95-4'])
        assert type(result) is list
        assert len(result) == 2
        assert len(result[0]) == 2
        assert len(result[1]) == 2
        assert result[0][0] == 'Variant'
        assert result[0][1] == '500 g'
        assert result[1][0] == 'CAS'
        assert result[1][1] == '1762-95-4'


    def test_nested_arr_to_dict(self):
        result = self._nested_arr_to_dict([['foo','bar'], ['baz','quux']])
        assert type(result) is dict
        assert 'foo' in result
        assert 'baz' in result
        assert result['foo'] == 'bar'
        assert result['baz'] == 'quux'


    def test_epoch(self):
        result = self._epoch
        assert type(result) is int


    @pytest.mark.parametrize('cas,valid_cas', [
        ('123-34-34',False),
        ('321-2-1',False),
        ('a-1-333',False),
        ('7732-18-5',True),
        ('7664-93-9',True)
    ])
    def test_is_cas(self, cas, valid_cas):
        result = self._is_cas(cas)
        assert type(result) is bool
        assert result is valid_cas


    @pytest.mark.parametrize('value,casted_value,value_type', [
        ('1234',1234,int),
        ('test','test',str),
        ('false',False,bool),
        ('true',True,bool),
        ('123.35',123.35,float),
        #('',None,None)
    ])
    def test_cast_type(self, value, casted_value, value_type):
        result = self._cast_type(value)
        assert type(result) is value_type
        assert result == casted_value


    def test_random_string(self):
        result_a = self._random_string()
        result_b = self._random_string()
        assert type(result_a) is str
        assert type(result_b) is str
        assert result_a != result_b


    @pytest.mark.parametrize('value,expected_result', [
        ({'foo':123, 'bar':555}, {'bar':555}),
        ({'foo':999999, 'bar':123}, {'foo':999999})
    ])
    def test_filter_highest_value(self, value, expected_result):
        result = self._filter_highest_value(value)
        assert result == expected_result


    def test_get_common_phrases(self):
        result = self._get_common_phrases([
            'oxidane','WATER', 'Atomic oxygen','Monooxygen','Oxygen(sup 3P)',
            'Oxygen, atomic','Photooxygen','Singlet oxygen','acqua','agua',
            'aqua','H2O','HYD','HYDROXY GROUP','BOUND OXYGEN'
        ])
        assert type(result) is dict
        assert result[('atomic',)] == 2
        assert result[('oxygen',)] == 4
