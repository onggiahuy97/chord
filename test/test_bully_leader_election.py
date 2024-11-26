import unittest
import time
from src.chord import Node

class TestChordLeaderElection(unittest.TestCase):
    def setUp(self):
        """Set up a Chord ring with multiple nodes before each test."""
        print("\n=== Setting up test nodes ===")
        self.n1 = Node(1)
        self.n12 = Node(12)
        self.n24 = Node(24)
        self.n18 = Node(18)
        self.n9 = Node(9)

        # Create the ring
        print("Creating Chord ring...")
        self.n1.join(self.n1)
        time.sleep(0.1)
        self.n12.join(self.n1)
        time.sleep(0.1)
        self.n24.join(self.n1)
        time.sleep(0.1)
        self.n18.join(self.n1)
        time.sleep(0.1)
        self.n9.join(self.n1)
        time.sleep(0.2)  # Additional time for ring stabilization
        
        # Store all nodes in a list for easy access
        self.nodes = [self.n1, self.n12, self.n24, self.n18, self.n9]
        print("Ring setup complete")

    def test_initial_leader_state(self):
        """Test that nodes start with no leader."""
        print("\n=== Testing initial leader state ===")
        for node in self.nodes:
            self.assertIsNone(node.leader_id, f"Node {node.id} should start with no leader")
        time.sleep(0.1)

    def test_leader_election_from_lowest_id(self):
        """Test leader election starting from node with lowest ID."""
        print("\n=== Testing election from lowest ID (Node 1) ===")
        self.n1.start_election()
        time.sleep(0.3)  # Allow election to complete
        
        # Node with highest ID (24) should be elected leader
        for node in self.nodes:
            self.assertEqual(node.leader_id, 24, 
                           f"Node {node.id} should recognize node 24 as leader")
        print("Election from lowest ID completed")

    def test_leader_election_from_middle_id(self):
        """Test leader election starting from node with middle ID."""
        print("\n=== Testing election from middle ID (Node 12) ===")
        self.n12.start_election()
        time.sleep(0.3)  # Allow election to complete
        
        # Node with highest ID (24) should still be elected leader
        for node in self.nodes:
            self.assertEqual(node.leader_id, 24, 
                           f"Node {node.id} should recognize node 24 as leader")
        print("Election from middle ID completed")

    def test_leader_election_from_highest_id(self):
        """Test leader election starting from node with highest ID."""
        print("\n=== Testing election from highest ID (Node 24) ===")
        self.n24.start_election()
        time.sleep(0.3)  # Allow election to complete
        
        # Node with highest ID (24) should be elected leader
        for node in self.nodes:
            self.assertEqual(node.leader_id, 24, 
                           f"Node {node.id} should recognize node 24 as leader")
        print("Election from highest ID completed")

    def test_multiple_sequential_elections(self):
        """Test multiple elections started by different nodes sequentially."""
        print("\n=== Testing multiple sequential elections ===")
        
        # First election
        print("Starting first election from Node 9...")
        self.n9.start_election()
        time.sleep(0.3)  # Allow first election to complete
        
        for node in self.nodes:
            self.assertEqual(node.leader_id, 24, 
                           "First election should elect node 24")
        print("First election completed")

        # Reset leader_id for all nodes
        print("Resetting leader IDs...")
        for node in self.nodes:
            node.leader_id = None
        time.sleep(0.2)

        # Second election
        print("Starting second election from Node 1...")
        self.n1.start_election()
        time.sleep(0.3)  # Allow second election to complete
        
        for node in self.nodes:
            self.assertEqual(node.leader_id, 24, 
                           "Second election should elect node 24 again")
        print("Second election completed")

    def test_ring_connectivity_during_election(self):
        """Test that the ring is properly connected during election."""
        print("\n=== Testing ring connectivity during election ===")
        # Track visited nodes during election
        visited = set()
        
        def track_announcement(self, leader_id):
            visited.add(self.id)
            self.leader_id = leader_id
            if self.successor().id not in visited:
                self.successor().announce_leader(leader_id)
            time.sleep(0.1)  # Small delay to make announcement trace visible

        # Replace announce_leader temporarily
        original_announce = Node.announce_leader
        Node.announce_leader = track_announcement

        try:
            print("Starting election from Node 9...")
            self.n9.start_election()
            time.sleep(0.3)  # Allow election to complete
            
            # All nodes should be visited during announcement
            self.assertEqual(len(visited), len(self.nodes), 
                           "Election should visit all nodes in the ring")
            print(f"Visited nodes: {visited}")
        finally:
            # Restore original announce_leader
            Node.announce_leader = original_announce

    def test_correct_successor_chain(self):
        """Test that the successor chain is correct before election."""
        print("\n=== Testing successor chain ===")
        # Check if each node's successor is correct
        expected_chain = {
            1: 9,    # Node 1's successor should be 9
            9: 12,   # Node 9's successor should be 12
            12: 18,  # Node 12's successor should be 18
            18: 24,  # Node 18's successor should be 24
            24: 1    # Node 24's successor should be 1
        }
        
        for node_id, expected_successor in expected_chain.items():
            node = next(n for n in self.nodes if n.id == node_id)
            self.assertEqual(node.successor().id, expected_successor,
                           f"Node {node_id}'s successor should be {expected_successor}")
            print(f"Node {node_id} -> Node {expected_successor} (✓)")
            time.sleep(0.1)

    def tearDown(self):
        """Clean up after each test."""
        print("\n=== Cleaning up test ===")
        # Reset leader_id for all nodes
        for node in self.nodes:
            node.leader_id = None
        time.sleep(0.1)
        print("Cleanup complete")

if __name__ == '__main__':
    unittest.main(verbosity=2)