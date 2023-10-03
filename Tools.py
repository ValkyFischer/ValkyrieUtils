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
import hashlib
import json
import os
import re
import secrets
import string
import time


# ===============================


class ValkyrieTools:
    @staticmethod
    def isFloat(obj: any) -> bool:
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
    def isInteger(obj: any) -> bool:
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
    def isBoolean(obj: any) -> bool:
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
    def isList(obj: any) -> bool:
        """
        Check if the input is a list.

        Args:
            obj (any): The input value to check.

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
    def isDict(obj: any) -> bool:
        """
        Check if the input is a dictionary.

        Args:
            obj (any): The input value to check.

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
    def isJson(obj: any) -> bool:
        """
        Check if the input is a JSON string.

        Args:
            obj (any): The input value to check.

        Returns:
            bool: True if the input is a JSON string, False otherwise.
        """
        try:
            if obj == "null":
                return False
            json.loads(obj)
            return True
        except json.JSONDecodeError:
            return False
    
    @staticmethod
    def matchDict(obj: dict) -> dict:
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
    
    @staticmethod
    def formatSize(size: int) -> str:
        """
        Format the file size in a human-readable format.
        
        Args:
            size (int): The file size in bytes.
            
        Returns:
            str: The formatted file size.
        """
        if size >= 1e9:  # Gigabytes
            return f"{size / 1e9:.2f} GB"
        elif size >= 1e6:  # Megabytes
            return f"{size / 1e6:.2f} MB"
        elif size >= 1e3:  # Kilobytes
            return f"{size / 1e3:.2f} KB"
        else:  # Bytes
            return f"{size:.2f} B"
        
    @staticmethod
    def formatSpeed(speed: int) -> str:
        """
        Format the speed in a human-readable format.
        
        Args:
            speed (int): The speed in bytes per second.
            
        Returns:
            str: The formatted speed.
        """
        if speed >= 1e6:  # Megabytes per second
            return f"{speed / 1e6:.2f} MB/s"
        elif speed >= 1e3:  # Kilobytes per second
            return f"{speed / 1e3:.2f} KB/s"
        else:  # Bytes per second
            return f"{speed:.2f} B/s"
        
    @staticmethod
    def formatTime(seconds: int, full: bool = False) -> str:
        """
        Format the time in a human-readable format.

        Args:
            seconds (int): The time in seconds.
            full (bool): Whether to include all time units or only the largest one. Default is False.

        Returns:
            str: The formatted time.
        """
        if seconds >= 86400:  # Days
            return f"{seconds / 86400:.2f} days {seconds % 86400 / 3600:.2f} hours {seconds % 3600 / 60:.2f} minutes {seconds % 60:.2f} seconds" if full else f"{seconds / 86400:.2f} days"
        elif seconds >= 3600:  # Hours
            return f"{seconds / 3600:.2f} hours {seconds % 3600 / 60:.2f} minutes {seconds % 60:.2f} seconds" if full else f"{seconds / 3600:.2f} hours"
        elif seconds >= 60:  # Minutes
            return f"{seconds / 60:.2f} minutes {seconds % 60:.2f} seconds" if full else f"{seconds / 60:.2f} minutes"
        else:  # Seconds
            return f"{seconds:.2f} seconds"

    @staticmethod
    def generateHwid() -> str:
        """
        Get a unique hardware ID for the current machine.
        
        Returns:
            str: The unique hardware ID.
        """
        import uuid
        return uuid.getnode()
    
    @staticmethod
    def generateCode(length: int = 32, letters: bool = True, digits: bool = True, punctuation: bool = True) -> str:
        """
        Generate a random code out of:
            - letters
            - digits
            - punctuation
        
        Args:
            length (int): The length of the code to generate, default is 32.
            letters (bool): Whether to include letters in the code, default is True.
            digits (bool): Whether to include digits in the code, default is True.
            punctuation (bool): Whether to include punctuation in the code, default is True.
            
        Returns:
            str: The generated code.
        """
        l = string.ascii_letters if letters is True else ""
        d = string.digits if digits is True else ""
        s = string.punctuation if punctuation is True else ""
        
        alphabet = l + d + s
        
        code = ""
        for i in range(length):
            code += "".join(secrets.choice(alphabet))
        
        return code
    
    @staticmethod
    def markdownHtml(text: str) -> str:
        """
        Parse a string of Markdown to its equivalent HTML part.
        
        Args:
            text (str): The Markdown text to parse.
            
        Returns:
            str: The parsed HTML text.
            
        """
        
        # Define regular expressions for each Markdown element
        bold_and_italic = r'\*\*\*(.*?)\*\*\*'
        bold = r'\*\*(.*?)\*\*'
        italic = r'\*(.*?)\*'
        underlined = r'__(.*?)__'
        strikethrough = r'~~(.*?)~~'
        inline_code = r'`(.*?)`'
        code_block = r'```(.*?)```'
        
        # Define a pattern for code blocks
        code_block_pattern = re.compile(code_block, flags = re.DOTALL)
        
        # Find code blocks and temporarily replace them with placeholders
        code_blocks = code_block_pattern.findall(text)
        code_block_placeholders = []
        for i, block in enumerate(code_blocks):
            placeholder = f"|-|CODE_BLOCK_PLACEHOLDER_{i}|-|"
            code_block_placeholders.append(placeholder)
            text = text.replace(f"```{block}```", placeholder)
        
        # Define a pattern for inline code
        inline_code_pattern = re.compile(inline_code)
        
        # Find inline code and temporarily replace them with placeholders
        inline_codes = inline_code_pattern.findall(text)
        inline_code_placeholders = []
        for i, code in enumerate(inline_codes):
            placeholder = f"|-|INLINE_CODE_PLACEHOLDER_{i}|-|"
            inline_code_placeholders.append(placeholder)
            text = text.replace(f"`{code}`", placeholder)
        
        # Replace Markdown elements with HTML, excluding text within code blocks and inline code
        text = re.sub(bold_and_italic, r'<b><i>\1</i></b>', text)
        text = re.sub(bold, r'<b>\1</b>', text)
        text = re.sub(italic, r'<i>\1</i>', text)
        text = re.sub(underlined, r'<u>\1</u>', text)
        text = re.sub(strikethrough, r'<s>\1</s>', text)
        
        # Replace newlines with <br> and --- with <hr> and replace tabs with 8 spaces
        text = text.replace("[---]\r\n", "<hr>")
        text = text.replace("---\r\n", "<hr>")
        text = text.replace("[---]\r", "<hr>")
        text = text.replace("---\r", "<hr>")
        text = text.replace("[---]\n", "<hr>")
        text = text.replace("---\n", "<hr>")
        text = text.replace("[---]", "<hr>")
        text = text.replace("---", "<hr>")
        text = text.replace("\r\n", "<br>")
        text = text.replace("\r", "<br>")
        text = text.replace("\n", "<br>")
        text = text.replace("\t", "        ")
        text = text.replace("\\t", "        ")
        
        # Replace and embed images, Example: ![Image Text](https://valky.dev/img.png) -> <img src="https://valky.dev/img.png" alt="Image Text">
        text = re.sub(r'!\[(.*?)]\((.*?)\)', r'<img src="\2" alt="\1">', text)
        
        # embed links, Example: [Website](https://valky.dev) -> <a href="https://valky.dev">Website</a>
        text = re.sub(r'\[(.*?)]\((.*?)\)', r'<a class="handle-link" href="\2" target="_blank">\1</a>', text)
        
        # replace some special symbols
        text = text.replace("-> ", " ➜ ")
        text = text.replace("=> ", " ⇒ ")
        text = text.replace(" <3 ", " ❤ ")
        
        # Replace code block placeholders back to code blocks
        for i, placeholder in enumerate(code_block_placeholders):
            text = text.replace(placeholder, f"```{code_blocks[i]}```")
        
        # Replace inline code placeholders back to inline code
        for i, placeholder in enumerate(inline_code_placeholders):
            text = text.replace(placeholder, f"`{inline_codes[i]}`")
        
        # Replace code blocks and inline code
        text = re.sub(code_block, r'<pre><code>\1</code></pre>', text, flags = re.DOTALL)
        text = re.sub(inline_code, r'<code>\1</code>', text)
        
        return text
    
    @staticmethod
    def getHash(data: bytes, hash_type: str = 'md5') -> str:
        """
        Hash the given data using the specified hash type.
        
        Args:
            data (bytes): The data to be hashed.
            hash_type (str): The hash type to be used. Possible values are 'md5', 'sha', 'sha1', 'sha256', and 'sha512'. Default is 'md5'.
            
        Returns:
            str: The hashed data.
        """
        match hash_type:
            case "md5":
                hsh = hashlib.md5()
            case "sha" | "sha1":
                hsh = hashlib.sha1()
            case "sha256":
                hsh = hashlib.sha256()
            case "sha512":
                hsh = hashlib.sha512()
            case _:
                hsh = hashlib.md5()
        
        hsh.update(data)
        return hsh.hexdigest()
    
    @staticmethod
    def getFileHash(file_path: str, hash_type: str = 'md5', buffer: int = 65536) -> str:
        """
        Hash the given file using the specified hash type.
        
        Args:
            file_path (str): The path to the file to be hashed.
            hash_type (str): The hash type to be used. Possible values are 'md5', 'sha', 'sha1', 'sha256', and 'sha512'. Default is 'md5'.
            buffer (int): The buffer size to be used when reading the file. Default is 65536.
            
        Returns:
            str: The hashed file.
        """
        hashed = None
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(buffer)
                if not data: break
                hashed = ValkyrieTools.getHash(data, hash_type)
        return hashed
    
    @staticmethod
    def getFileSize(file_path: str) -> int:
        """
        Get the size of the given file.
        
        Args:
            file_path (str): The path to the file to get the size of.
            
        Returns:
            int: The size of the file in bytes.
        """
        return os.path.getsize(file_path)
    
    @staticmethod
    def getFileDate(file_path: str) -> str:
        """
        Get the date of the given file.
        
        Args:
            file_path (str): The path to the file to get the date of.
            
        Returns:
            str: The date of the file.
        """
        modified = os.path.getmtime(file_path)
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(modified))
    
    @staticmethod
    def getFileList(path: str) -> list:
        """
        Get a list of all files in the given path, including files in sub-directories.
        
        Args:
            path (str): The path to get the file list from.
            
        Returns:
            list: A list of all files in the given path.
        """
        file_list = list()
        for dirs, sub_dirs, files in os.walk(path):
            if len(files) > 0:
                for file in files:
                    filepath = f"{dirs}/{file}".replace('\\', '/')
                    file_list.append(filepath)
        return file_list


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
    
    # get unique hardware ID
    print(f"Unique HWID: {ValkyrieTools.generateHwid()}")  # Returns a unique hardware ID
    
    # generate code
    print(f"Random Code: {ValkyrieTools.generateCode()}")  # Returns a random code
    
    # markdown to html
    print(f"Markdown to HTML: {ValkyrieTools.markdownHtml('**Hello** *World*!')}")  # Returns <b>Hello</b> <i>World</i>!
    print(f"Markdown to HTML: {ValkyrieTools.markdownHtml('```*italic* **bold**```')}")  # Returns <pre><code>*italic* **bold**</code></pre>
