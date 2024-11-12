import random 
from src.chord import Node 

k = 5

# Test to create nodes and form the Chord ring
def test_chord_ring():
    # Create nodes
    nodes = []
    existing_ids = set()
    for i in range(5):  # Creating 5 nodes
        while True:
            node_id = random.randint(0, 2 ** k)
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