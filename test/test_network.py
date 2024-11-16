from src.network_node import NetworkNode
# Create and start leader node
leader = NetworkNode(1, 'localhost', 5001)
leader.start_server()

# Create and start other nodes
node2 = NetworkNode(2, 'localhost', 5002)
node2.start_server()
node2.join_network(1, 'localhost', 5001)

node3 = NetworkNode(3, 'localhost', 5003)
node3.start_server()
node3.join_network(1, 'localhost', 5001)

# Test put and get
# node2.put("key1", "value1")
# result = node3.get("key1")
# print(f"Retrieved value: {result}")

# Clean up
leader.stop_server()
node2.stop_server()
node3.stop_server()