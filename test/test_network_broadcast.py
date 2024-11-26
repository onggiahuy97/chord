import unittest
from src.chord import Node
import time

class TestChordBroadcast(unittest.TestCase):
    def setUp(self):
        
        # Create and start nodes (same as in main())
        self.n1 = Node(1)
        self.n2 = Node(2)
        self.n3 = Node(3)
        self.n4 = Node(4)
        self.n5 = Node(5)

        self.nodes = [self.n1, self.n2, self.n3, self.n4, self.n5]

        print("\n=====Starting nodes and their servers=====\n")
        for node in self.nodes:
            node.connector.start_server()
            time.sleep(0.1)

        print("\n=====Creating a Chord ring and joining=====\n")
        # Create Chord ring
        self.n1.join(self.n1)
        for node in self.nodes[1:]:
            node.join(self.n1)

        print("\n=====Register node into their peer=====\n")
        # Register network information 
        for node in self.nodes: 
            for peer in self.nodes:
                if node != peer:
                    node.connector.register_peer(peer.id, peer.connector.host, peer.connector.port)

        time.sleep(0.5)

    def tearDown(self):
        # Stop servers (same as end of main())
        print("\n=====Stopping the server of each node=====\n")
        for node in self.nodes: 
            node.connector.stop_server()

    def test_broadcast(self):
        """Test broadcast functionality between two nodes"""
        # Send test message
        print("\n=====Starting broadcasting message=====\n")
        test_message = "Test broadcast message"
        message_id = f"{self.n1.id}_test"
        self.n1.connector.broadcast_message(test_message, message_id=message_id)

        # Wait for message propagation
        time.sleep(1)

        # Verify all nodes received the message 
        for node in self.nodes: 
            received = len(node.connector.received_broadcasts) > 0 
            self.assertTrue(received, f"Node {node.id} did not receive the broadcast")

if __name__ == "__main__":
    unittest.main()
