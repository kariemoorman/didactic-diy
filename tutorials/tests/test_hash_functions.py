#!/usr/bin/python3

import numpy as np
import unittest
from encoding_and_encryption.hash_functions import HashLib


class TestHashLib(unittest.TestCase): 
    def setUp(self):
        #True Positive Test Cases
        self.string_to_md5 = HashLib('pasSw0rd_po#?er', algorithm='md5')
        self.string_to_sha1 = HashLib('pasSw0rd_po#?er', algorithm='sha1')
        self.string_to_sha3 = HashLib('pasSw0rd_po#?er', algorithm='sha3')
        self.string_to_sha3_256 = HashLib('pasSw0rd_po#?er', algorithm='sha3_256')
        self.string_to_sha3_384 = HashLib('pasSw0rd_po#?er', algorithm='sha3_384')
        self.string_to_sha3_512 = HashLib('pasSw0rd_po#?er', algorithm='sha3_512')
        self.string_to_sha256 = HashLib('pasSw0rd_po#?er', algorithm='sha256')
        self.string_to_sha384 = HashLib('pasSw0rd_po#?er', algorithm='sha384')
        self.string_to_sha512 = HashLib('pasSw0rd_po#?er', algorithm='sha512')
        self.string_to_blake2_a = HashLib('pasSw0rd_po#?er', algorithm='blake2')
        self.string_to_blake2_b = HashLib('pasSw0rd_po#?er', algorithm='blake2', digest_size=64)
        self.string_to_blake2b_a = HashLib('pasSw0rd_po#?er', algorithm='blake2b')
        self.string_to_blake2b_b = HashLib('pasSw0rd_po#?er', algorithm='blake2b', digest_size=64)
        self.string_to_blake2s_a = HashLib('pasSw0rd_po#?er', algorithm='blake2s')
        self.string_to_blake2s_b = HashLib('pasSw0rd_po#?er', algorithm='blake2s', digest_size=24)
        
        
    def test_string_to_md5(self):
        hash_value = self.string_to_md5.compute_hash()
        expected_output = 'c39dd7fe747eddee11aeb90202f9f11e'
        expected_len = 32
        self.assertTrue(np.array_equal(hash_value[2], expected_output))
        self.assertTrue(np.array_equal(len(hash_value[2]), expected_len))

    def test_string_to_sha1(self):
        hash_value = self.string_to_sha1.compute_hash()
        expected_output = 'a40bd21063b53ec263dd81792b9d71622a35547a'
        expected_len = 40
        self.assertTrue(np.array_equal(hash_value[2], expected_output))
        self.assertTrue(np.array_equal(len(hash_value[2]), expected_len))

    def test_string_to_sha3(self):
        hash_value = self.string_to_sha3.compute_hash()
        expected_output = 'ab03716e5e2d85b10bd3313d0771548226b1c6bd3fbc1313edfebe8ad3db4173ff4c0907f20065589dae0b2b3550c6a3'
        expected_len = 96
        self.assertTrue(np.array_equal(hash_value[2], expected_output))
        self.assertTrue(np.array_equal(len(hash_value[2]), expected_len))

    def test_string_to_sha3_256(self):
        hash_value = self.string_to_sha3_256.compute_hash()
        expected_output = '4120cf86bd5dbd4a836a68a9eeba829019c41db09e6bd670952a9ec78e5ccdef'
        expected_len = 64
        self.assertTrue(np.array_equal(hash_value[2], expected_output))
        self.assertTrue(np.array_equal(len(hash_value[2]), expected_len))
        
    def test_string_to_sha3_384(self):
        hash_value = self.string_to_sha3_384.compute_hash()
        expected_output = 'ab03716e5e2d85b10bd3313d0771548226b1c6bd3fbc1313edfebe8ad3db4173ff4c0907f20065589dae0b2b3550c6a3'
        expected_len = 96
        self.assertTrue(np.array_equal(hash_value[2], expected_output))
        self.assertTrue(np.array_equal(len(hash_value[2]), expected_len))       

    def test_string_to_sha3_512(self):
        hash_value = self.string_to_sha3_512.compute_hash()
        expected_output = 'dce1339aba426abbef07912ac2e34b8c9cb3b174f37f7209c62e103389eab24e5b4cd28a9d0281c614d1911569119a4cf35c024294c5a62ee56b652c69082e51'
        expected_len = 128
        self.assertTrue(np.array_equal(hash_value[2], expected_output))
        self.assertTrue(np.array_equal(len(hash_value[2]), expected_len))       

    def test_string_to_blake2_a(self):
        hash_value = self.string_to_blake2_a.compute_hash()
        expected_output = '9e0813bde3254e155ee2eba8b67fc525ad75a8bef91653413ae02ab6d22c1275'
        expected_len = 64
        self.assertTrue(np.array_equal(hash_value[2], expected_output))
        self.assertTrue(np.array_equal(len(hash_value[2]), expected_len))  

    def test_string_to_blake2_b(self):
        hash_value = self.string_to_blake2_b.compute_hash()
        expected_output = '26a70c3d9d5bf1deb72773155a53a01a176d7ef09baa9d97de8f872f295445c849a1a05e2b7b451d7aeed5134162900cc4f93d5dad40d59589fe839cefe29f02'
        expected_len = 128
        self.assertTrue(np.array_equal(hash_value[2], expected_output))
        self.assertTrue(np.array_equal(len(hash_value[2]), expected_len)) 

    def test_string_to_blake2b_a(self):
        hash_value = self.string_to_blake2b_a.compute_hash()
        expected_output = '9e0813bde3254e155ee2eba8b67fc525ad75a8bef91653413ae02ab6d22c1275'
        expected_len = 64
        self.assertTrue(np.array_equal(hash_value[2], expected_output))
        self.assertTrue(np.array_equal(len(hash_value[2]), expected_len))  

    def test_string_to_blake2b_b(self):
        hash_value = self.string_to_blake2b_b.compute_hash()
        expected_output = '26a70c3d9d5bf1deb72773155a53a01a176d7ef09baa9d97de8f872f295445c849a1a05e2b7b451d7aeed5134162900cc4f93d5dad40d59589fe839cefe29f02'
        expected_len = 128
        self.assertTrue(np.array_equal(hash_value[2], expected_output))
        self.assertTrue(np.array_equal(len(hash_value[2]), expected_len)) 

    def test_string_to_blake2s_a(self):
        hash_value = self.string_to_blake2s_a.compute_hash()
        expected_output = 'eb846c338abf3dcb106a8cec503de0911841e4bb3bb04ba0a8e3cc0639e239c6'
        expected_len = 64
        self.assertTrue(np.array_equal(hash_value[2], expected_output))
        self.assertTrue(np.array_equal(len(hash_value[2]), expected_len))  

    def test_string_to_blake2s_b(self):
        hash_value = self.string_to_blake2s_b.compute_hash()
        expected_output = '30c9fc0ae79a00b4071e404311a3f94b1284136e591022e1'
        expected_len = 48
        self.assertTrue(np.array_equal(hash_value[2], expected_output))
        self.assertTrue(np.array_equal(len(hash_value[2]), expected_len)) 

if __name__ == '__main__':
    unittest.main()