#!/usr/bin/python3

import unittest
import numpy as np
from encoding_and_encryption.character_encoder import CharacterEncoder

class TestCharacterEncoder(unittest.TestCase):

    def setUp(self):
        #True Positive Test Cases
        self.encoder_string_binary = CharacterEncoder('Hello', 'string', 'binary') 
        self.encoder_string_ascii = CharacterEncoder('He ll0w', 'string', 'ascii') 
        self.encoder_ascii_binary = CharacterEncoder('72 101 108 108 111', 'ascii', 'binary')
        self.encoder_ascii_string = CharacterEncoder('118 101 115 116 105  98 117 108 101  83', 'ascii', 'string') 
        self.encoder_binary_ascii = CharacterEncoder('01110011 01101101 01100001 01110011 01101000 00110011 01100100', 'binary', 'ascii')
        self.encoder_binary_string = CharacterEncoder('01110011 01101101 01100001 01110011 01101000 00110011 01100100', 'binary', 'string')

    def test_string_to_binary(self):
        binary_values = self.encoder_string_binary.string_to_binary()
        expected_binary = np.array(['01001000 01100101 01101100 01101100 01101111'])
        self.assertTrue(np.array_equal(binary_values, expected_binary))

    def test_string_to_ascii(self):
        ascii_values = self.encoder_string_ascii.string_to_ascii()
        expected_ascii = np.array([72, 101, 32, 108, 108, 48, 119])
        self.assertTrue(np.array_equal(ascii_values, expected_ascii))

    def test_ascii_to_binary(self):
        binary_values = self.encoder_ascii_binary.ascii_to_binary()
        expected_binary = np.array(['01001000 01100101 01101100 01101100 01101111'])
        self.assertTrue(np.array_equal(binary_values, expected_binary))
        
    def test_ascii_to_string(self):
        string_value = self.encoder_ascii_string.ascii_to_string()
        expected_string = 'vestibuleS'
        self.assertTrue(np.array_equal(string_value, expected_string))

    def test_binary_to_ascii(self):
        ascii_values = self.encoder_binary_ascii.binary_to_ascii()
        expected_ascii = np.array([115, 109,  97, 115, 104,  51, 100])
        self.assertTrue(np.array_equal(ascii_values, expected_ascii))

    def test_binary_to_string(self):
        string_value = self.encoder_binary_string.binary_to_string()
        expected_string = 'smash3d'
        self.assertTrue(np.array_equal(string_value, expected_string))

if __name__ == '__main__':
    unittest.main()

## From 'tutorials' directory, run 'python -m unittest discover tests' to execute unit tests.