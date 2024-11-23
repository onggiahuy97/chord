import hashlib
from src.connector import Connector
from tabulate import tabulate

m = 5
MAX = 2**m

def decrease_with_wraparound(value,size):
    """Decreases value by size with wraparound at MAX, used for finger table predecessor calculation"""
    if size <= value:
        return value - size
    else:
        return MAX-(size-value)

def between(value,start,end):
    """Check if value lies in range [start, end] with wraparound support for Chord ring topology"""
    if start == end:
        return True
    elif start > end :
        shift = MAX - start
        start = 0
        end = (end +shift)%MAX
        value = (value + shift)%MAX
    return start < value < end

def between_include_start(value,start,end):
    """Check if a value is between start and end (exclusive) OR equal to start."""
    if value == start:
        return True
    else:
        return between(value,start,end)

def between_include_end(value,start,end):
    """"Check if a value is between start and end (exclusive) OR equal to end."""
    if value == end:
        return True
    else:
        return between(value,start,end)

def hash_int(key):
    """Hash given key into integer between 0 and 2**m"""
    return int(hashlib.sha1(key.encode()).hexdigest(), 16) % (2 ** m)

class Node:
    """
        Initializes a new node in the Chord ring.

        Args:
            id (int): The identifier of the node in the ring.

        Initializes the node's finger table, start entries, and other attributes
        required for the Chord protocol. The finger table will be populated when
        the node joins the ring.

        Attributes:
            id (int): The node's identifier in the ring.
            finger (dict): The node's finger table mapping indices to successor nodes.
            start (dict): The start positions for each entry in the finger table.
            messages (dict): Key-value storage for the node.
            leader_id (int): The identifier of the leader node (used in leader election).
            connector (Connector): A connector for simulating node communication.
    """
    def __init__(self,id):
        self.id = id
        self.finger = {}
        self.start = {}
        self.messages = {}
        self.leader_id = None
        for i in range(m):
            self.start[i] = (self.id+(2**i)) % (2**m)

        # init Connector for networking
        self.connector = Connector(self)

    def successor(self):
        """Returns the immediate successor of the node"""
        return self.finger[0]

    def find_successor(self,id):
        """
        Finds the successor node responsible for the given identifier.

        Returns:
            Node: the successor node responsible for the given id.

        The method checks if the id falls between the current node's predecessor and itself,
        in which case the current node is responsible. Otherwise, it finds closest predecessor
        of the id and returns its successor.
        """
        if between_include_end(id,self.predecessor.id,self.id):
            return self
        n = self.find_predecessor(id)
        return n.successor()

    def find_predecessor(self,id):
        """
        Finds the predecessor node of a given id.

        returns:
            Node: The predecessor node of the given id.

        The method traverses the Chord ring using the finger table entries, moving to the
        closest preceding node until it find a node n1 such that id is between n1 and n1.successor()
        """
        if id == self.id:
            return self.predecessor
        n1 = self
        while not between_include_end(id,n1.id,n1.successor().id):
            n1 = n1.closest_preceding_finger(id)
        return n1

    def closest_preceding_finger(self,id):
        """
        Returns the closest preceding node to a given id.

        Returns:
            Node

        The method interates over the finger table entries in reverse order and returns
        the first finger whose node ID is between the current node's ID and the given ID
        if no such node is found, return current node itself.
        """
        for i in range(m-1,-1,-1):
            if between(self.finger[i].id,self.id,id):
                return self.finger[i]
        return self


    def join(self,leader_node):
        """
        Joins the Chord ring, init node's finger table and updating other nodes

        If the node is the first node in the ring, it init itself.
        Otherwise, it init finger table by contacting its finger table
        and update other nodes
        """
        if self == leader_node:
            for i in range(m):
                self.finger[i] = self
            self.predecessor = self
            print(f"Node {self.id} has joined itself")
        else:
            self.init_finger_table(leader_node)
            self.update_others()
            self.move_keys()
            print(f"Node {self.id} has joined node {leader_node.id}")

    def move_keys(self):
        """Transfer keys from successor to this node for which this node is now responsible."""
        # Get the current successor
        successor = self.successor()

        # Identify the range of keys this node should take responsibility for
        keys_to_move = {}

        # Transfer keys in the interval (predecessor.id, self.id]
        for hashed_key, (key, value) in successor.messages.items():
            if between_include_end(hashed_key, self.predecessor.id, self.id):
                keys_to_move[hashed_key] = (key, value)

        # Move keys to the new node's storage
        self.messages.update(keys_to_move)

        # Remove moved keys from the successor
        for hashed_key in keys_to_move:
            del successor.messages[hashed_key]

        # print(f"Node {self.id} has moved {len(keys_to_move)} keys from Node {successor.id}")

    def init_finger_table(self,n1):
        """
        Init finger table of given node

        This method sets up the finger table entries for the current node by querying
        the existing ring via node n1. It also sets the predecessor of the node and
        updates the successor's predecessor to point back to this node.
        """
        self.finger[0] = n1.find_successor(self.start[0])
        self.predecessor = self.successor().predecessor
        self.successor().predecessor = self
        self.predecessor.finger[0] = self
        for i in range(m-1):
            if between_include_start(self.start[i+1],self.id,self.finger[i].id):
                self.finger[i+1] = self.finger[i]
            else :
                self.finger[i+1] = n1.find_successor(self.start[i+1])

    def update_others(self):
        for i in range(m):
            prev  = decrease_with_wraparound(self.id,2**i)
            p = self.find_predecessor(prev)
            if prev == p.successor().id:
                p = p.successor()
            p.update_finger_table(self,i)

    def update_finger_table(self,s,i):
        if between_include_start(s.id,self.id,self.finger[i].id) and self.id!=s.id:
                self.finger[i] = s
                p = self.predecessor
                p.update_finger_table(s,i)

    def update_others_leave(self):
        for i in range(m):
            prev  = decrease_with_wraparound(self.id,2**i)
            p = self.find_predecessor(prev)
            p.update_finger_table(self.successor(),i)

    def leave(self):
        """Transfer keys to successor and update the ring to remove this node."""
        successor = self.successor()
        predecessor = self.predecessor

        # Step 1: Transfer all keys in this node's `messages` to the successor
        if successor:
            successor.messages.update(self.messages)  # Transfer all keys to successor
            print(f"Node {self.id} transferred {len(self.messages)} keys to Node {successor.id}")

        # Step 2: Update predecessor and successor pointers to remove this node
        if successor and predecessor:
            successor.predecessor = predecessor  # Successor's predecessor now points to this node's predecessor
            predecessor.setSuccessor(successor)  # Predecessor's successor now points to this node's successor

        # Step 3: Clear this node's messages and finger table to detach it from the ring
        self.messages.clear()
        self.finger.clear()
        self.predecessor = None

        # Notify the rest of the ring about the departure if the finger table is populated
        if self.finger:
            self.update_others_leave()

        print(f"Node {self.id} has left the ring")

    def setSuccessor(self,succ):
        self.finger[0] = succ

    def put(self, key, value):
        """Stores a key-value pair in the Chord ring."""
        # Hash key to know which successor will store the message
        hashed_key = hash_int(key)
        target_node = self.find_successor(hashed_key)
        target_node.messages[hashed_key] = (key, value)
        print(f"Hash: '{hash_int(key)}' Key '{key}' with value '{value}' stored at Node {target_node.id}")

    def get(self, key):
        """Retrieves the value associated with key from the Chord ring"""
        hashed_key = hash_int(key)
        target_node = self.find_successor(hashed_key)
        if hashed_key in target_node.messages:
            return target_node.messages[hashed_key]
        else:
            return None

    # Helper function to print the finger table for a node
    def print_finger_table(self, seen=None):
        headers = ["Finger", "Node"]
        rows = []
        for k, n in enumerate(self.finger):
            c1 = f"N{self.id} + {2**k}"
            c2 = f"N{self.finger[n].id}"
            rows.append([c1, c2])

        print(f"Finger table of Node {self.id}")
        print(tabulate(rows, headers, tablefmt="grid"))


    def start_election(self):
        """Initiates the leader election process."""
        print(f"Node {self.id} starts election.")
        self.forward_election(self.id)

    def forward_election(self, candidate_id, seen=False):
        """
        Forwards the election message to the successor with the highest candidate ID.
        Uses the Chang-Roberts algorithm for ring-based leader election.

        Args:
            candidate_id: The ID of the current candidate
            seen: Boolean indicating if this candidate_id has completed a full circle
        """
        # Case 1: Message has made a full circle and returned to initiator
        if self.id == candidate_id and seen:
            print(f"Node {self.id} wins election!")
            self.announce_leader(self.id)

        # Case 2: First time the initiator sees its own ID
        elif self.id == candidate_id and not seen:
            print(f"Node {self.id} forwarding own id with seen=True")
            self.successor().forward_election(candidate_id, True)

        # Case 3: Current node's ID is less than candidate_id
        elif self.id < candidate_id:
            print(f"Node {self.id} forwards larger candidate {candidate_id}")
            self.successor().forward_election(candidate_id, seen)

        # Case 4: Current node's ID is greater than candidate_id
        elif self.id > candidate_id:
            print(f"Node {self.id} replaces candidate {candidate_id} with own larger id")
            # This node becomes the new candidate
            self.successor().forward_election(self.id, False)

    def announce_leader(self, leader_id):
        """Announces the leader to all nodes in the ring."""
        self.leader_id = leader_id
        print(f"Node {self.id} acknowledges leader {leader_id}.")
        if self.successor().id != leader_id:  # Continue propagation
            self.successor().announce_leader(leader_id)

