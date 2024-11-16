import unittest
import time
from src.chord import Node, hash_int, m, MAX

class TestChord(unittest.TestCase):
    """Test cases for the local Chord implementation."""
    
    def test_nodes_join(self):
        """Test joining multiple nodes to the Chord ring and verify the ring structure."""
        print("\n=== Testing Node Join Operations ===")
        
        # Create initial node (node 1)
        print("\nCreating and initializing Node 1...")
        n1 = Node(1)
        n1.join(n1)  # First node joins itself to create the ring
        time.sleep(0.2)  # Allow time for initialization

        # Create and join node 14
        print("\nCreating and joining Node 14...")
        n14 = Node(14)
        n14.join(n1)
        time.sleep(0.2)  # Allow time for join operation

        # Create and join node 27
        print("\nCreating and joining Node 27...")
        n27 = Node(27)
        n27.join(n1)
        time.sleep(0.2)  # Allow time for join operation

        print("\nCurrent ring structure (finger tables):")
        n1.print_finger_table()
        time.sleep(0.1)

        print("\nStoring test data...")
        keys = ["apple", "banana", "cherry", "date", "elderberry"]
        values = ["red", "yellow", "red", "brown", "purple"]
        for key, value in zip(keys, values):
            n1.put(key, value)
            time.sleep(0.1)  # Space out put operations

        print("\nVerifying node connections...")
        # Test finger table entries
        # Test node 1's connections
        self.assertEqual(n1.successor().id, 14, "Node 1's successor should be node 14")
        self.assertEqual(n1.predecessor.id, 27, "Node 1's predecessor should be node 27")
        print("Node 1 connections verified ✓")
        time.sleep(0.1)

        # Test node 14's connections
        self.assertEqual(n14.successor().id, 27, "Node 14's successor should be node 27")
        self.assertEqual(n14.predecessor.id, 1, "Node 14's predecessor should be node 1")
        print("Node 14 connections verified ✓")
        time.sleep(0.1)

        # Test node 27's connections
        self.assertEqual(n27.successor().id, 1, "Node 27's successor should be node 1")
        self.assertEqual(n27.predecessor.id, 14, "Node 27's predecessor should be node 14")
        print("Node 27 connections verified ✓")
        
        print("\nJoin operations test completed successfully")
        print("==========================================")
        time.sleep(0.2)
    
    def test_nodes_leave(self):
        """Test node departure and message transfer."""
        print("\n=== Testing Node Leave Operations ===")
        
        print("\nSetting up initial ring...")
        n1 = Node(1)
        n1.join(n1)
        time.sleep(0.2)

        print("\nJoining Node 14...")
        n14 = Node(14)
        n14.join(n1)
        time.sleep(0.2)

        print("\nJoining Node 27...")
        n27 = Node(27)
        n27.join(n1)
        time.sleep(0.2)

        print("\nStoring test data...")
        keys = ["apple", "banana", "cherry", "date", "elderberry"]
        values = ["red", "yellow", "red", "brown", "purple"]
        for key, value in zip(keys, values):
            n1.put(key, value)
            time.sleep(0.1)

        initial_message_count = len(n1.messages) + len(n14.messages) + len(n27.messages)
        print(f"\nInitial message distribution:")
        print(f"Node 1: {len(n1.messages)} messages")
        print(f"Node 14: {len(n14.messages)} messages")
        print(f"Node 27: {len(n27.messages)} messages")
        
        self.assertEqual(initial_message_count, len(keys), 
                        "All messages should be stored")
        time.sleep(0.2)
        
        print("\nNode 27 leaving the network...")
        n27.leave()
        time.sleep(0.3)  # Allow time for message transfer
        
        remaining_messages = len(n1.messages) + len(n14.messages)
        print(f"\nMessage distribution after Node 27 left:")
        print(f"Node 1: {len(n1.messages)} messages")
        print(f"Node 14: {len(n14.messages)} messages")
        
        self.assertEqual(remaining_messages, len(keys), 
                        "Node 27 leave and should transfer all message to its successor")
        time.sleep(0.2)

        print("\nNode 1 leaving the network...")
        n1.leave()
        time.sleep(0.3)  # Allow time for message transfer

        print(f"\nFinal message count in Node 14: {len(n14.messages)} messages")
        self.assertEqual(len(n14.messages), len(keys), 
                        "Node 1 leave and should transfer all message to its successor")
        
        print("\nLeave operations test completed successfully")
        print("==========================================")
        time.sleep(0.2)

if __name__ == '__main__':
    unittest.main(verbosity=2)