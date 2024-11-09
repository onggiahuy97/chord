# author: Pedro Garcia Lopez, PhD

import random
import hashlib

k = 5
MAX = 2**k



def id():
    return long(random.uniform(0,2**k))


def decr(value,size):
    if size <= value:
        return value - size
    else:
        return MAX-(size-value)
        

def between(value,init,end):
    if init == end:
        return True
    elif init > end :
        shift = MAX - init
        init = 0
        end = (end +shift)%MAX
        value = (value + shift)%MAX
    return init < value < end

def Ebetween(value,init,end):
    if value == init:
        return True
    else:
        return between(value,init,end)

def betweenE(value,init,end):
    if value == end:
        return True
    else:
        return between(value,init,end)

def hash(key):
    return int(hashlib.sha1(key.encode()).hexdigest(), 16) % (2 ** k)
    
class Node:
    def __init__(self,id):
        self.id = id
        self.finger = {}
        self.start = {}
        self.message = {}
        for i in range(k):
            self.start[i] = (self.id+(2**i)) % (2**k)

    def successor(self):
        return self.finger[0]
    
    def find_successor(self,id):  
        if betweenE(id,self.predecessor.id,self.id):
            return self
        n = self.find_predecessor(id)
        return n.successor()
    
    def find_predecessor(self,id):
        if id == self.id:
            return self.predecessor
        n1 = self
        while not betweenE(id,n1.id,n1.successor().id):
            n1 = n1.closest_preceding_finger(id)
        return n1
    
    def closest_preceding_finger(self,id):
        for i in range(k-1,-1,-1):
            if between(self.finger[i].id,self.id,id):
                return self.finger[i]
        return self
        
    
    def join(self,n1):
        if self == n1:
            for i in range(k):
                self.finger[i] = self
            self.predecessor = self
        else:
            self.init_finger_table(n1)
            self.update_others()  
           # Move keys !!! 
            
    def init_finger_table(self,n1):
        self.finger[0] = n1.find_successor(self.start[0])
        self.predecessor = self.successor().predecessor
        self.successor().predecessor = self
        self.predecessor.finger[0] = self
        for i in range(k-1):
            if Ebetween(self.start[i+1],self.id,self.finger[i].id):
                self.finger[i+1] = self.finger[i]
            else :
                self.finger[i+1] = n1.find_successor(self.start[i+1])

    def update_others(self):
        for i in range(k):
            prev  = decr(self.id,2**i)
            p = self.find_predecessor(prev)
            if prev == p.successor().id:
                p = p.successor()
            p.update_finger_table(self,i)
            
    def update_finger_table(self,s,i):
        if Ebetween(s.id,self.id,self.finger[i].id) and self.id!=s.id:
                self.finger[i] = s
                p = self.predecessor
                p.update_finger_table(s,i)

    def update_others_leave(self):
        for i in range(k):
            prev  = decr(self.id,2**i)
            p = self.find_predecessor(prev)
            p.update_finger_table(self.successor(),i)
    # not checked 
    def leave(self):
        self.successor().predecessor = self.predecessor
        self.predecessor.setSuccessor(self.successor())
        self.update_others_leave()
        
    def setSuccessor(self,succ):
        self.finger[0] = succ

    def put(self, key, value):
        target_node = self.find_successor(hash(key))
        target_node.message[key] = value
        print(f"Hash: '{hash(key)}' Key '{key}' with value '{value}' stored at Node {target_node.id}")
        



# Test to create nodes and form the Chord ring
def test_chord_ring():
    # Create nodes
    nodes = []
    existing_ids = set()
    for i in range(10):  # Creating 5 nodes
        while True:
            node_id = random.randint(0, MAX - 1)
            if node_id not in existing_ids:
                break
        existing_ids.add(node_id)
        new_node = Node(node_id)
        if nodes:
            new_node.join(nodes[0])  # Join using the first node as the bootstrap
        else:
            new_node.join(new_node)  # First node joins itself to form the initial ring
        nodes.append(new_node)
        print(f"Node {new_node.id} joined the ring")
        print_finger_table(new_node)
        print("====================")

        # Verify key-value pairs are stored at the correct node
        # for key in keys:
        #     target_node = nodes[0].find_successor(hash(key))
        #     print(f"Key '{key}' is stored at Node {target_node.id} with value '{target_node.message.get(key, 'Not found')}'")
    
    # Test storing key-value pairs
    keys = ["apple", "banana", "cherry", "date", "elderberry"]
    values = ["red", "yellow", "red", "brown", "purple"]
    for key, value in zip(keys, values):
        nodes[0].put(key, value)

    pretty_print_chord(nodes)

# Helper function to print the finger table for a node
def print_finger_table(node):
    print(f"Finger table for Node {node.id}:")
    for i in range(k):
        print(f"Start {node.start[i]} -> Finger {i}: Node {node.finger[i].id}")
    print("Predecessor:", node.predecessor.id)

def pretty_print_chord(nodes):
    import matplotlib.pyplot as plt
    import numpy as np

    # Sort nodes by their ID in ascending order
    nodes = sorted(nodes, key=lambda x: x.id)
    node_ids = [node.id for node in nodes]
    num_nodes = len(node_ids)

    # Create a circle
    circle = plt.Circle((0, 0), 1, fill=False, linewidth=2)

    fig, ax = plt.subplots()
    ax.add_artist(circle)
    ax.set_aspect('equal')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)

    # Plot nodes on the circle in counter-clockwise order
    for i, node_id in enumerate(node_ids):
        angle = 2 * np.pi * (num_nodes - i) / num_nodes  # Counter-clockwise
        x = np.cos(angle)
        y = np.sin(angle)
        ax.plot(x, y, 'o', markersize=10)
        ax.text(x * 1.1, y * 1.1, f'P{node_id}', fontsize=12, ha='center', va='center')

    # Remove x and y axis coordinates
    ax.axis('off')

    # Print sorted nodes on the console
    ring_representation = " -> ".join(f"[{node_id}]" for node_id in node_ids)
    print(f"Chord Ring: {ring_representation} -> [{node_ids[0]}] (to complete the ring)")

    plt.title('Chord Ring')
    plt.show()

if __name__ == "__main__":
    test_chord_ring()
