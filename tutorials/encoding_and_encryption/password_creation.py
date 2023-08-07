#!/usr/bin/python3

import os
import argparse
import argon2
from argon2 import PasswordHasher
from hash_functions import HashLib


class PasswordCreation: 
    def __init__(self, input_string, algorithm='sha256', digest_size=32, salt_length=16):
        self.input_string = input_string 
        self.algorithm = algorithm
        self.digest_size = digest_size
        self.salt_length = salt_length
        
    def generate_salt(self):
        salt = os.urandom(self.salt_length)
        return salt.hex()
        
    def generate_password(self):
        if self.algorithm == 'argon': 
            ph = PasswordHasher(time_cost=2, memory_cost=102400, parallelism=2,hash_len=self.digest_size)
            password = ph.hash(self.input_string)
            salt_value = self.generate_salt()
            hashed_password = password + salt_value
            hash_list = [self.input_string, self.algorithm, password, salt_value, hashed_password]
        else:    
            transformer = HashLib(self.input_string, self.algorithm, self.digest_size)
            hash_list = transformer.compute_hash()
            salt_value = self.generate_salt()
            hashed_password = hash_list[2] + salt_value
            hash_list.append(salt_value)
            hash_list.append(hashed_password)
        return hash_list
            


def main():
    parser = argparse.ArgumentParser(description="Password Creator", formatter_class=argparse.MetavarTypeHelpFormatter)
    parser.add_argument("input_string", type=str, help="Alphanumeric input string (e.g., string: 'H3l-l0H')")
    parser.add_argument("-a", "--algorithm", type=str, default="sha256", help='Select a hashing algorithm for encryption (options: "md5", "sha1", "sha256", "sha3", "sha3_256", "sha3_384", "sha3_512", "blake2", "blake2b", "blake2s", "bcrypt", "argon")')
    parser.add_argument("-d", "--digest_size", type=int, default=32, help="Select length (int) of the output ( e.g., 32 [32 bytes -> 256 bits; 64 (64 bytes -> 512 bits])")
    parser.add_argument("-s", "--salt_length", type=int, default=16, help="Select length (int) of the output (e.g., 16-32)")

    args = parser.parse_args()
    
    password_encryption = PasswordCreation(args.input_string, args.algorithm, args.digest_size, args.salt_length)
    output = password_encryption.generate_password()
    print(output)


if __name__ == "__main__":
    main()