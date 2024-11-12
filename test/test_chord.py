# test_chord.py

import unittest
from src.chord import Node, hash, m, MAX

class TestChord(unittest.TestCase):
    """Test cases for the local Chord implementation."""

    def setUp(self):
        """Set up the initial conditions for each test."""
        # Reset any global variables or states if necessary
    
    def test_nodes_join(self):
        """Test joining multiple nodes to the Chord ring and verify the ring structure."""
        # Create initial node (node 1)
        n1 = Node(1)
        n1.join(n1)  # First node joins itself to create the ring

        # Create and join node 11
        n14 = Node(14)
        n14.join(n1)

        # Create and join node 27
        n27 = Node(27)
        n27.join(n1)

        keys = ["apple", "banana", "cherry", "date", "elderberry"]
        values = ["red", "yellow", "red", "brown", "purple"]
        for key, value in zip(keys, values):
            n1.put(key, value)

        # Test finger table entries
        # Test node 1's connections
        self.assertEqual(n1.successor().id, 14, "Node 1's successor should be node 4")
        self.assertEqual(n1.predecessor.id, 27, "Node 1's predecessor should be node 7")

        # Test node 14's connections
        self.assertEqual(n14.successor().id, 27, "Node 14's successor should be node 27")
        self.assertEqual(n14.predecessor.id, 1, "Node 14's predecessor should be node 1")

        # Test node 27's connections
        self.assertEqual(n27.successor().id, 1, "Node 27's successor should be node 1")
        self.assertEqual(n27.predecessor.id, 14, "Node 27's predecessor should be node 14")
        print("==========================================")
    
    def test_nodes_leave(self):
        n1 = Node(1)
        n1.join(n1)  # First node joins itself to create the ring

        # Create and join node 11
        n14 = Node(14)
        n14.join(n1)

        # Create and join node 27
        n27 = Node(27)
        n27.join(n1)

        keys = ["apple", "banana", "cherry", "date", "elderberry"]
        values = ["red", "yellow", "red", "brown", "purple"]
        for key, value in zip(keys, values):
            n1.put(key, value)

        self.assertEqual(len(n1.messages) + len(n14.messages) + len(n27.messages), len(keys), "All messages should be stored")
        
        n27.leave()
        
        self.assertEqual(len(n1.messages) + len(n14.messages), len(keys), "Node 27 leave and should transfer all message to its successor")

        n1.leave()


    def tearDown(self):
        """Clean up after each test."""
        # Reset any changes made during tests

if __name__ == '__main__':
    unittest.main()
