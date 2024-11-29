import unittest
from chord import Node
import time

class TestFailureDetection(unittest.TestCase):
    def setUp(self):
         # Create and start nodes (same as in main())
        self.n1 = Node(2)
        self.n2 = Node(3)
        self.n3 = Node(4)

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

    def test_heartbeat(self):
        print("\n=====Start Heartbeating=====\n")
        self.n1.start_heartbeat() # ping the successor
        time.sleep(5)  # Allow some heartbeats to be sent
        self.n2.leave() # node 2 failed and leave server
        time.sleep(5)  # Allow failure detection to occur
        # Check if node1 handled the failure
        self.assertNotEqual(self.n1.successor().id, self.n2.id)

        self.n2.join(self.n1) # node 2 reboot and join the server again
        time.sleep(5)
        self.assertEqual(self.n1.successor().id, self.n2.id)

if __name__ == "__main__":
    unittest.main()
