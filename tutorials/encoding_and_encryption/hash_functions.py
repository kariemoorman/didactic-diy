#!/usr/bin/python3

import hashlib 
import argparse

class HashLib: 
    def __init__(self, input_string, algorithm='sha256', digest_size=32):
        self.input_string = input_string 
        self.algorithm = algorithm
        self.digest_size = digest_size
        
    def compute_hash(self):
        if self.algorithm == 'md5':
            hash_obj = hashlib.md5()
        elif self.algorithm == 'sha1':
            hash_obj = hashlib.sha1()
        elif self.algorithm == 'sha3':
            hash_obj = hashlib.sha3_384()
        elif self.algorithm == 'sha3_256':
            hash_obj = hashlib.sha3_256()
        elif self.algorithm == 'sha3_384':
            hash_obj = hashlib.sha3_384()
        elif self.algorithm == 'sha3_512':
            hash_obj = hashlib.sha3_512()
        # elif self.algorithm == 'shake':
        #     hash_obj = hashlib.shake_256()
        # elif self.algorithm == 'shake256':
        #     hash_obj = hashlib.shake_256()
        # elif self.algorithm == 'shake128':
        #     hash_obj = hashlib.shake_128()
        elif self.algorithm == 'sha256':
            hash_obj = hashlib.sha256()
        elif self.algorithm == 'sha384':
            hash_obj = hashlib.sha384()
        elif self.algorithm == 'sha512':
            hash_obj = hashlib.sha512()
        elif self.algorithm == 'blake2':
            hash_obj = hashlib.blake2b(digest_size=self.digest_size)
        elif self.algorithm == 'blake2b':
            hash_obj = hashlib.blake2b(digest_size=self.digest_size)
        elif self.algorithm == 'blake2s':
            hash_obj = hashlib.blake2s(digest_size=self.digest_size)
        else: 
            raise ValueError("Invalid algorithm specified.")
        #Encode input string
        hash_obj.update(self.input_string.encode('utf-8'))
        #Get hexidecimal representation
        hash_result = hash_obj.hexdigest()
        hash_list = [self.input_string, self.algorithm, (hash_result)]
        return hash_list

def main(): 
    parser = argparse.ArgumentParser(description="String Hashing Algorithm", formatter_class=argparse.MetavarTypeHelpFormatter)
    parser.add_argument("input_string", type=str, help="Alphanumeric input string (e.g., 'i-h8t3_Mondayz*'; 'hello, World')")
    parser.add_argument("-a", "--algorithm", type=str, default="sha256", help='Select a hashing algorithm for encryption (options: "md5", "sha1", "sha256", "sha3", "sha3_256", "sha3_384", "sha3_512", "blake2", "blake2b", "blake2s")')
    parser.add_argument("-d", "--digest_size", type=int, default=32, help="Select length (int) of the output( e.g., 32 [32 bytes -> 256 bits; 64 (64 bytes -> 512 bits])")

    args = parser.parse_args()
    
    hasher = HashLib(args.input_string, args.algorithm, args.digest_size)
    hash_value = hasher.compute_hash()
    
    print(f"\nInput string: '{hash_value[0]}'")
    print(f"Hash value ({hash_value[1]}): {hash_value[2]} \n")
    print("Output:", hash_value,"\n")
    
if __name__ == "__main__":
    main()