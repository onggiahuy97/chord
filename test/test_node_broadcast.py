import unittest
from src.network_node import NetworkNode
import time
import threading
from typing import Dict, Set

class TestNetworkBroadcast(unittest.TestCase):
    def setUp(self):
        """Set up test nodes."""
        # Create nodes
        self.n1 = NetworkNode(1, 'localhost', 5001)
        self.n2 = NetworkNode(2, 'localhost', 5002)
        self.n3 = NetworkNode(3, 'localhost', 5003)
        self.n4 = NetworkNode(4, 'localhost', 5004)
        self.n5 = NetworkNode(5, 'localhost', 5005)
        
        self.nodes = [self.n1, self.n2, self.n3, self.n4, self.n5]
        
        # Start all nodes
        for node in self.nodes:
            node.start_server()
            time.sleep(0.1)
        
        # Create Chord ring
        self.n1.join(self.n1)  # Leader
        for node in self.nodes[1:]:
            node.join(self.n1)
        
        # Register network information
        for node in self.nodes:
            for peer in self.nodes:
                if node != peer:
                    node.register_peer(peer.id, peer.host, peer.port)
        
        time.sleep(0.5)  # Allow for network setup

    def tearDown(self):
        """Clean up after tests."""
        for node in self.nodes:
            node.clear_broadcast_history()
            node.stop_server()
        time.sleep(0.5)

    def test_single_broadcast(self):
        """Test that a single broadcast reaches all nodes."""
        test_message = "Test broadcast message"
        self.n1.broadcast_message(test_message)
        time.sleep(1)  # Allow for message propagation
        
        # Verify all nodes received the message
        for node in self.nodes:
            received = len(node.received_broadcasts) > 0
            self.assertTrue(received, f"Node {node.id} did not receive the broadcast")
                           

if __name__ == '__main__':
    unittest.main(verbosity=2)