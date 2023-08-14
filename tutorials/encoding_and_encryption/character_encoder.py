#!/usr/bin/python3

import base58
import base64
import numpy as np
import argparse

class CharacterEncoder: 
    def __init__(self, input_value, input_format, output_format): 
        self.input_value = input_value
        self.output_format = output_format
        self.input_format = input_format
    
    def string_to_ascii(self):
        ascii_values = np.array([ord(char) for char in self.input_value])
        return ascii_values

    def string_to_binary(self):
        binary_values = np.array([' '.join(format(ord(char), '08b') for char in self.input_value)])
        return binary_values
    
    def string_to_base64(self): 
        base64_value = base64.b64encode(self.input_value.encode('utf-8'))
        return base64_value.decode('utf-8')
    
    def string_to_base58(self): 
        base58_value = base58.b58encode(self.input_value.encode('utf-8'))
        return base58_value.decode('utf-8')

    def ascii_to_binary(self):
        input_values = [int(value) for value in self.input_value.split()]
        binary_segments = np.array([' '.join([format(value, '08b') for value in input_values])])
        return binary_segments

    def binary_to_string(self): 
        binary_segments = self.input_value.split()
        string = ''.join([chr(int(binary, 2)) for binary in binary_segments])
        return string
        
    def ascii_to_string(self):  
        input_values = [int(value) for value in self.input_value.split()]
        string = ''.join(chr(value) for value in input_values) 
        return string
    
    def base64_to_string(self):
        string_value = base64.b64decode(self.input_value)
        if self.output_format == 'binary':
            binary_string = [' '.join(format(byte, '08b') for byte in string_value)]
            return binary_string
        elif self.output_format == 'string':
            string = string_value.decode('utf-8')
            return string
        else: 
            ascii_string = np.array([ord(char) for char in string_value.decode('utf-8')])
            return ascii_string
    
    def base58_to_string(self):
        string_value = base58.b58decode(self.input_value)
        if self.output_format == 'binary':
            binary_string = [' '.join(format(byte, '08b') for byte in string_value)]
            return binary_string
        elif self.output_format == 'string':
            return string_value.decode('utf-8')
        else: 
            ascii_string = np.array([ord(char) for char in string_value.decode('utf-8')])
            return ascii_string
        
    def binary_to_ascii(self): 
        binary_segments = self.input_value.split()
        ascii_values = np.array([int(binary, 2) for binary in binary_segments])
        return ascii_values

    def extract_encoding(self): 
        if self.input_format == 'string': 
            if self.output_format == 'binary':
                output = self.string_to_binary()
            elif self.output_format == 'ascii':
                output = self.string_to_ascii()
            elif self.output_format == 'base64': 
                output = self.string_to_base64()
            elif self.output_format == 'base58': 
                output = self.string_to_base58()
            else: 
                raise ValueError("Invalid output format specified.") 
        elif self.input_format == 'ascii': 
            if self.output_format == 'binary':
                output = self.ascii_to_binary()
            elif self.output_format == 'string':
                output = self.ascii_to_string()
            else: 
                raise ValueError("Invalid output format specified.") 
        elif self.input_format == 'binary': 
            if self.output_format == 'ascii':
                output = self.binary_to_ascii()
            elif self.output_format == 'string':
                output = self.binary_to_string()
            else: 
                raise ValueError("Invalid output format specified.") 
        elif self.input_format == 'base64': 
            if self.output_format in ['string', 'ascii', 'binary']:
                output = self.base64_to_string()  
            else:  
                raise ValueError("Invalid output format specified.")   
        elif self.input_format == 'base58': 
            if self.output_format in ['string', 'ascii', 'binary']:
                output = self.base58_to_string()
            else:  
                raise ValueError("Invalid output format specified.") 
        else: 
            raise ValueError("Invalid input specified.")
        return output

def main():
    parser = argparse.ArgumentParser(description="Character Encoder: String, Binary and ASCII", formatter_class=argparse.MetavarTypeHelpFormatter)
    parser.add_argument("input_value", type=str, help="Alphanumeric input string (e.g., string: 'hello'; ascii: '104 101 108 108 111'; binary: '01101000 01100101 01101100 01101100 01101111')")
    parser.add_argument("-i", "--input_format", type=str, help="Input format ('string', 'binary', 'ascii')")
    parser.add_argument("-o", "--output_format", type=str, help="Output format ('string', 'binary', 'ascii')")

    args = parser.parse_args()
    
    transformer = CharacterEncoder(args.input_value,args.input_format,args.output_format)
    results = transformer.extract_encoding()
    print(f'\nInput Value ("{args.input_format}"): {args.input_value}')
    print(f'Output Value ("{args.output_format}"): {results}\n')    

if __name__ == "__main__":
    main()