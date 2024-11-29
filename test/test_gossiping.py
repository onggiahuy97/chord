import unittest
import time
from chord import Node, hash_int

class TestGossiping(unittest.TestCase):
    def setUp(self):
        # Create and start nodes (same as in main())
        self.n1 = Node(5)
        self.n2 = Node(6)
        self.n3 = Node(7)

        self.nodes = [self.n1, self.n2, self.n3]

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

    def test_gossip(self):
        # Add a key to n1 and start gossiping
        self.n1.put("key1", "value1")

        print("\n=====Start Gossiping=====\n")

        self.n1.start_gossip()
        self.n3.start_gossip()

        time.sleep(8)  # Wait for gossip to propagate

        # Verify that the key was gossiped to n3
        self.assertIn(hash_int("key1"), self.n3.messages)
        self.assertEqual(self.n3.messages[hash_int("key1")], ("key1", "value1"))

if __name__ == "__main__":
    unittest.main()
