from src.network_node import NetworkNode
import time

def demonstrate_network_chord():
    print("\n=== Starting NetworkChord Demonstration ===\n")
    
    # Create and start nodes
    print("1. Creating and starting nodes...")
    n1 = NetworkNode(1, 'localhost', 5001)
    n2 = NetworkNode(2, 'localhost', 5002)
    n3 = NetworkNode(3, 'localhost', 5003)
    n4 = NetworkNode(4, 'localhost', 5004)
    n5 = NetworkNode(5, 'localhost', 5005)
    
    nodes = [n1, n2, n3, n4, n5]
    for node in nodes:
        node.start_server()
        time.sleep(0.1)  # Small delay to ensure proper startup
    
    print("\n2. Joining nodes to the network...")
    # Join nodes to create ring
    n1.join(n1)  # Leader node
    n2.join(n1)
    n3.join(n1)
    n4.join(n1)
    n5.join(n1)
    time.sleep(0.5)  # Allow time for joins to complete
    
    print("\n3. Testing data storage and retrieval...")
    # Store some key-value pairs
    test_data = {
        "Apple": "Green",
        "Mango": "Yellow",
        "Sky": "Blue"
    }
    
    print("\nStoring data...")
    for key, value in test_data.items():
        n1.put(key, value)
        time.sleep(0.1)  # Small delay between puts
    
    print("\nRetrieving data from different nodes...")
    for node in nodes:
        for key in test_data.keys():
            result = node.get(key)
            print(f"Node {node.id} getting '{key}': {result}")
        print()
    
    print("\n=== Cleaning up ===")
    # Stop all nodes
    for node in nodes:
        node.stop_server()
    print("All nodes stopped")

if __name__ == "__main__":
    demonstrate_network_chord()