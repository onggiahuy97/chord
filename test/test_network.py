import unittest
import requests
import time
import random
import string
import statistics
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Tuple
import json

class TestChordNetwork(unittest.TestCase):
    """Test cases for the networked Chord implementation."""
    
    BASE_URL = "http://127.0.0.1:5000"
    MAX_NODES = 32  # 2^5 since m=5
    
    def test_network(self):
        # Create 10 nodes first
        for _ in range(10):
            response = requests.post(f"{self.BASE_URL}/join")
        
        for i in range(30):
            headers = {"Content-Type": "application/json"}
            data = {
                "key": f"{i}",
                "value": f"{i}"
            }
            response = requests.post(f"{self.BASE_URL}/insert",json=data,headers=headers)
        
        response = requests.get(f"{self.BASE_URL}/nodes")
        print(response)

if __name__ == '__main__':
    unittest.main(verbosity=2)