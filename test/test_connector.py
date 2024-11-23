import unittest
from src.chord import Node
import time

class TestChordBroadcast(unittest.TestCase):
    def setUp(self):
        # Create and start nodes (same as in main())
        self.n1 = Node(1)
        self.n1.connector.start_server()
        self.n2 = Node(2)
        self.n2.connector.start_server()
        self.n3 = Node(3)
        self.n3.connector.start_server()

    def tearDown(self):
        # Stop servers (same as end of main())
        self.n1.connector.stop_server()
        self.n2.connector.stop_server()
        self.n3.connector.stop_server()

    def test_broadcast(self):
        """Test broadcast functionality between two nodes"""
        # Create ring (same as in main())
        self.n1.join(self.n1)
        self.n2.join(self.n1)
        self.n3.join(self.n1)

        # Register peers to form the complete ring
        self.n1.connector.register_peer(self.n2.id, self.n2.connector.host, self.n2.connector.port)
        self.n2.connector.register_peer(self.n3.id, self.n3.connector.host, self.n3.connector.port)
        self.n3.connector.register_peer(self.n1.id, self.n1.connector.host, self.n1.connector.port)

        # Send test message
        test_message = "Test broadcast message"
        message_id = f"{self.n1.id}_test"
        self.n1.connector.broadcast_message(test_message, message_id=message_id)

        # Wait for message propagation
        time.sleep(1)

        # Verify all nodes received the broadcast
        self.assertIn(message_id, self.n1.connector.received_broadcasts,
                     "Node 1 didn't receive the broadcast")
        self.assertIn(message_id, self.n2.connector.received_broadcasts,
                     "Node 2 didn't receive the broadcast")
        self.assertIn(message_id, self.n3.connector.received_broadcasts,
                     "Node 3 didn't receive the broadcast")

        # Verify ring formation
        self.assertEqual(self.n1.successor().id, 2,
                        "Node 1's successor should be Node 2")
        self.assertEqual(self.n2.successor().id, 3,
                        "Node 2's successor should be Node 3")
        self.assertEqual(self.n3.successor().id, 1,
                        "Node 3's successor should be Node 1")


if __name__ == "__main__":
    unittest.main()
