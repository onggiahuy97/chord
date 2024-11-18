from src.network_node import NetworkNode
import time

def main():
    # Create two nodes
    node1 = NetworkNode(id=1, host="localhost", port=5001)
    node2 = NetworkNode(id=2, host="localhost", port=5002)

    node1.join(node1)
    node2.join(node1)
    
    try:
        # Start both nodes
        print("Starting nodes...")
        node1.start_server()
        node2.start_server()
        
        # Give servers time to start
        time.sleep(1)
        
        # Register the nodes with each other
        print("\nRegistering peers...")
        node1.register_peer(node2.id, "localhost", 5002)
        node2.register_peer(node1.id, "localhost", 5001)  # Add this line
        
        # Print peer information
        print(f"\nNode 1 peers: {node1.peers}")
        print(f"Node 2 peers: {node2.peers}")
        
        # # Print finger table information
        # print(f"\nNode 1 successor: {node1.successor().id if node1.successor() else 'None'}")
        # print(f"Node 2 successor: {node2.successor().id if node2.successor() else 'None'}")
        
        # Test broadcast
        print("\nTesting broadcast...")
        try:
            node1.broadcast_message("Hello from Node 1!")
        except Exception as e:
            print(f"Broadcast error: {e}")
        
        # Wait to see the broadcast propagate
        time.sleep(2)
        
        # Test another broadcast from node 2
        print("\nTesting second broadcast...")
        try:
            node2.broadcast_message("Hello from Node 2!")
        except Exception as e:
            print(f"Second broadcast error: {e}")
            
        # Wait to see the second broadcast
        time.sleep(2)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        print("\nStopping nodes...")
        node1.stop_server()
        node2.stop_server()

if __name__ == "__main__":
    main()