#!/usr/bin/python
import os
from datetime import datetime
import argparse
from cryptography.hazmat.backends import default_backend 
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


class AsymmetricEncryption: 
    
    def __init__(self, input_phrase, action): 
        self.input_phrase = input_phrase.encode('utf-8')
        self.action = action
        self.snapshotdate = datetime.today().strftime('%d-%m-%Y')
        self.snapshotdatetime = datetime.today().strftime('%d-%m-%Y_%H-%M-%S')
        self.private_key_filepath = f'credentials/private_key_{self.snapshotdate}.pem'

    def generate_keypair(self):
        # Generate a private-public key pair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
            )
        # Save private key
        self.save_private_key(private_key)
        # Extract the public key
        public_key = private_key.public_key()
        return public_key

    def save_private_key(self, private_key): 
        # Save private key to file
        with open(self.private_key_filepath, 'wb') as f:
            f.write(private_key.private_bytes (
                encoding=serialization.Encoding.PEM,
                # format=serialization.PrivateFormat.PKCS8,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        print('\nPrivate key written to credentials directory.')

    def access_private_key(self):
        # Load private key from the file
        with open(self.private_key_filepath, 'rb') as f:
            private_key_data = f.read()
        private_key = serialization.load_pem_private_key(
            private_key_data,
            password=None,
            backend=default_backend()
            )
        return private_key

    def encrypt_message(self, public_key): 
        # Encrypt the message using the public key
        encrypted_text = public_key.encrypt(
            self.input_phrase,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
                )
            )
        return encrypted_text

    def decrypt_message(self, private_key):
        # Update encoding
        encrypted_text = self.input_phrase.decode('unicode-escape').encode('ISO-8859-1')
        # Decrypt the ciphertext using private key
        decrypted_message = private_key.decrypt(
            encrypted_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
                )
            )
        decrypted_plaintext = decrypted_message.rstrip(b'\x00')
        return decrypted_plaintext

        
    def perform_cryptography(self):
        if self.action == 'encrypt':
            public_key = self.generate_keypair()
            encrypted_message = self.encrypt_message(public_key)
            print(f"\nEncrypted message: {encrypted_message}")
            return encrypted_message
        elif self.action == 'decrypt':
            private_key = self.access_private_key()
            # Print information about the private key
            # print("\nPrivate Key Information:")
            # print(f"Key Size: {private_key.key_size}")
            # print(f"Key Format: {private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())}")
            decrypted_message = self.decrypt_message(private_key)
            print(f"\nDecrypted message: '{decrypted_message.decode('utf-8')}'\n")
            return decrypted_message.decode('utf-8')
        else: 
            print('Invalid input.')
            

def main(): 
    parser = argparse.ArgumentParser(description="Asymmetric Encryption & Decryption.")
    parser.add_argument("input_phrase", type=str, help="Input value (str).")
    parser.add_argument("-a", "--action", type=str, choices=['encrypt', 'decrypt'], help="Specify cryptographic action.")
    args = parser.parse_args()
    
    cryptography = AsymmetricEncryption(args.input_phrase, args.action)
    cryptography.perform_cryptography()

    
if __name__ == '__main__': 
    main()

