#!/usr/bin/python

import os
from datetime import datetime
import argparse
from cryptography.fernet import Fernet


class SymmetricEncryption: 
    
    def __init__(self, input_phrase, action): 
        self.input_phrase = input_phrase.encode('utf-8')
        self.action = action
        self.snapshotdate = datetime.today().strftime('%d-%m-%Y')
        self.snapshotdatetime = datetime.today().strftime('%d-%m-%Y_%H-%M-%S')
        self.key_filepath = f'credentials/fernet_key_{self.snapshotdate}.key'

    def generate_key(self):
        # Generate a symmetric encryption key
        encryption_key = Fernet.generate_key()
        self.save_key(encryption_key)
        return encryption_key
    
    def save_key(self, encryption_key):
        # Save private key to file
        with open(self.key_filepath, "wb") as key_file:
            key_file.write(encryption_key)
        print('\nEncryption key written to credentials directory.')
        
    def access_fernet_key(self):
        with open(self.key_filepath, "rb") as key_file:
            encryption_key = key_file.read()
        return encryption_key

    def initialize_cipher(self, encryption_key):
        # Initialize the Fernet cipher with the key
        cipher = Fernet(encryption_key)
        return cipher

    def encrypt_message(self, cipher): 
        ciphertext = cipher.encrypt(self.input_phrase)
        return ciphertext
    
    def decrypt_message(self, cipher): 
        ciphertext = self.input_phrase.decode('unicode-escape').encode('ISO-8859-1')
        decrypted_message = cipher.decrypt(ciphertext)
        return decrypted_message

    def perform_cryptography(self):
        print("\nOriginal message:", self.input_phrase)
        if self.action == 'encrypt': 
            key = self.generate_key()
            cipher = self.initialize_cipher(key)
            encrypted_message = self.encrypt_message(cipher)
            print("\nEncrypted message:", encrypted_message.decode('utf-8'))
            return encrypted_message
        elif self.action == 'decrypt': 
            key = self.access_fernet_key()
            cipher = self.initialize_cipher(key)
            decrypted_message = self.decrypt_message(cipher)
            print(f"\nDecrypted message: '{decrypted_message.decode('utf-8')}'\n")
            return decrypted_message
            
def main():
    parser = argparse.ArgumentParser(description="Symmetric Encryption & Decryption.")
    parser.add_argument("input_phrase", type=str, help="Input value (str).")
    parser.add_argument("-a", "--action", type=str, choices=['encrypt', 'decrypt'], help="Specify cryptographic action.")
    args = parser.parse_args()
            
    cryptography = SymmetricEncryption(args.input_phrase, args.action)
    cryptography.perform_cryptography()

if __name__ == '__main__': 
    main()
