import unittest
from src.chord import Node, hash

class TestChordNodeLeave(unittest.TestCase):
    def setUp(self):
        """Set up the initial Chord ring with a few nodes for testing."""
        self.k = 4  # Number of bits in the identifier space
        # Initialize nodes
        self.node1 = Node(1)
        self.node2 = Node(8)
        self.node3 = Node(15)
        
        # Set up initial Chord ring
        self.node1.join(self.node1)  # Start with node1
        self.node2.join(self.node1)  # node2 joins the ring
        self.node3.join(self.node1)  # node3 joins the ring

    def test_leave_node(self):
        """Test that a node leaving the ring transfers keys and updates pointers correctly."""
        
        # Step 1: Insert some keys into the ring
        self.node1.put("key1", "value1")
        self.node1.put("key2", "value2")
        self.node2.put("key3", "value3")
        
        # Verify keys are stored on the correct nodes
        hashed_key1 = hash("key1")
        hashed_key2 = hash("key2")
        hashed_key3 = hash("key3")
        
        self.assertIn(hashed_key1, self.node1.find_successor(hashed_key1).messages)
        self.assertIn(hashed_key2, self.node1.find_successor(hashed_key2).messages)
        self.assertIn(hashed_key3, self.node2.find_successor(hashed_key3).messages)

        # Step 2: Make node2 leave the ring
        self.node2.leave()

        # Verify node2 no longer holds any keys
        self.assertEqual(len(self.node2.messages), 0, "Node2 should have transferred all keys upon leaving.")

        # Verify node2's keys were transferred to its successor
        successor = self.node2.successor()
        self.assertIn(hashed_key3, successor.messages, "Node2's keys should have been transferred to its successor.")
        self.assertEqual(successor.messages[hashed_key3], ("key3", "value3"), "Transferred key should match original value.")

        # Step 3: Verify ring structure
        # Node1's successor should now be node3, as node2 left the ring
        self.assertEqual(self.node1.successor().id, self.node3.id, "Node1's successor should be Node3 after Node2 leaves.")
        # Node3's predecessor should now be node1
        self.assertEqual(self.node3.predecessor.id, self.node1.id, "Node3's predecessor should be Node1 after Node2 leaves.")

    def tearDown(self):
        """Clean up after each test."""
        self.node1 = None
        self.node2 = None
        self.node3 = None

if __name__ == "__main__":
    unittest.main()
