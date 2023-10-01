#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Oct 01, 2023
@author: v_lky

--------

About:
    This module, ValkyrieTools, provides utility functions to check and match various types of input.
    It can determine if an object can be interpreted as a float, integer, boolean, list, or dictionary.
    It also offers a function to match a dictionary's values to their correct data types based on these types.
--------

Example:
    >>> ValkyrieTools.isList([1, 2, 3]
    True
    >>> ValkyrieTools.isList({'a': 1, 'b': 2})
    False
    >>> ValkyrieTools.isDict({'a': 1, 'b': 2})
    True
    >>> ValkyrieTools.isBoolean('True')
    True
    >>> ValkyrieTools.isBoolean('False')
    True
    >>> ValkyrieTools.isBoolean('Maybe')
    False
    >>> ValkyrieTools.isFloat('1.0')
    True
    >>> ValkyrieTools.isFloat(1)
    False
    
"""

import ast


# ===============================


class ValkyrieTools:
    @staticmethod
    def isFloat(obj):
        """
        Check if the input can be parsed as a float.

        Args:
            obj (any): The input value to check.

        Returns:
            bool: True if the input can be parsed as a float, False otherwise.
        """
        try:
            float_value = float(obj)
            return float_value != int(float_value) or '.' in str(obj)
        except ValueError:
            return False
    
    @staticmethod
    def isInteger(obj):
        """
        Check if the input can be parsed as an integer.

        Args:
            obj (any): The input value to check.

        Returns:
            bool: True if the input can be parsed as an integer, False otherwise.
        """
        try:
            int_value = int(obj)
            return float(int_value) == float(obj)
        except ValueError:
            return False
    
    @staticmethod
    def isBoolean(obj):
        """
        Check if the input represents a boolean value.

        Args:
            obj (any): The input value to check.

        Returns:
            bool: True if the input represents a boolean value (including yes or no, 1 or 0), False otherwise.
        """
        if str(obj).lower() in ["true", "yes", "false", "no"] or obj in [1, 0, True, False]:
            return True
        else:
            return False
    
    @staticmethod
    def isList(obj):
        """
        Check if the input is a list.

        Args:
            obj: The input value to check.

        Returns:
            bool: True if the input is a list, False otherwise.
        """
        if isinstance(obj, str):
            if obj.startswith("[") and obj.endswith("]"):
                return True
            else:
                return False
        return isinstance(obj, list)
    
    @staticmethod
    def isDict(obj):
        """
        Check if the input is a dictionary.

        Args:
            obj: The input value to check.

        Returns:
            bool: True if the input is a dictionary, False otherwise.
        """
        if isinstance(obj, str):
            if obj.startswith("{") and obj.endswith("}"):
                return True
            else:
                return False
        else:
            return isinstance(obj, dict)
    
    @staticmethod
    def matchDict(obj: dict):
        """
        Match the input dictionary to the correct type.
        
        Identified types are:
            - Integer
            - Float
            - Boolean
            - List
            - Dictionary
        
        Args:
            obj: The input dictionary to match.
            
        Returns:
            dict: The matched dictionary.
        """
        matched = {}
        for entity, settings in obj.items():
            matched[entity] = {}
            if isinstance(settings, dict):
                matched[entity] = ValkyrieTools.matchDict(settings)
            else:
                if ValkyrieTools.isInteger(settings):
                    matched[entity] = int(settings)
                elif ValkyrieTools.isFloat(settings):
                    matched[entity] = float(settings)
                elif ValkyrieTools.isBoolean(settings):
                    if str(settings).lower() in ["true", "yes"] or settings in [1, True]:
                        matched[entity] = True
                    elif str(settings).lower() in ["false", "no"] or settings in [0, False]:
                        matched[entity] = False
                elif ValkyrieTools.isList(settings):
                    matched[entity] = ast.literal_eval(settings)
                elif ValkyrieTools.isDict(settings):
                    matched[entity] = ast.literal_eval(settings)
                else:
                    matched[entity] = str(settings)
        
        return matched


# ===============================


if __name__ == '__main__':
    # List example
    print(f"List: {ValkyrieTools.isList([1, 2, 3])}")  # Returns True
    print(f"List: {ValkyrieTools.isList({'a': 1, 'b': 2})}")  # Returns False
    
    # Dict example
    print(f"Dict: {ValkyrieTools.isDict({'a': 1, 'b': 2})}")  # Returns True
    print(f"Dict: {ValkyrieTools.isDict([1, 2, 3])}")  # Returns False
    
    # String example
    print(f"Float: {ValkyrieTools.isFloat('1.0')}")  # Returns True
    print(f"Float: {ValkyrieTools.isFloat(1)}")  # Returns False
    
    # Integer example
    print(f"Integer: {ValkyrieTools.isInteger(1)}")  # Returns True
    print(f"Integer: {ValkyrieTools.isInteger(1.3)}")  # Returns False
    
    # Boolean example
    print(f"Boolean: {ValkyrieTools.isBoolean('True')}")  # Returns True
    print(f"Boolean: {ValkyrieTools.isBoolean('False')}")  # Returns True
    print(f"Boolean: {ValkyrieTools.isBoolean('Yes')}")  # Returns True
    print(f"Boolean: {ValkyrieTools.isBoolean('No')}")  # Returns True
    print(f"Boolean: {ValkyrieTools.isBoolean('1')}")  # Returns False
    print(f"Boolean: {ValkyrieTools.isBoolean('0')}")  # Returns False
    print(f"Boolean: {ValkyrieTools.isBoolean(1)}")  # Returns True
    print(f"Boolean: {ValkyrieTools.isBoolean(0)}")  # Returns True
    print(f"Boolean: {ValkyrieTools.isBoolean('Maybe')}")  # Returns False
    
    # Match dict example
    test_dict = {
        "a": "1", "b": "2", "c": "3", "d": "True", "e": "False", "f": "Yes", "g": "No",
        "h": "1.3", "i": "1.0", "j": "5", "k": "Maybe", "l": "[1, 2, 3]", "m": "{'a': 1, 'b': 2}"
    }
    print(f"Matched dict: {ValkyrieTools.matchDict(test_dict)}")  # Returns {'a': 1, 'b': 2, 'c': 3, 'd': True, 'e': False, 'f': True, 'g': False, 'h': 1.3, 'i': 1.0, 'j': 5, 'k': 'Maybe', 'l': [1, 2, 3], 'm': {'a': 1, 'b': 2}}
