from flask import Flask, request, jsonify
import random
from src.chord import Node, hash

app = Flask(__name__)

# Initialize the Chord DHT with k bits and max nodes
k = 4
MAX = 2**k
nodes = {}

# Create the initial Chord node
initial_node = Node(random.randint(0, MAX-1))
initial_node.join(initial_node)
nodes[initial_node.id] = initial_node

@app.route("/nodes", methods=["GET"])
def list_nodes():
    """List all nodes in the Chord ring"""
    node_list = [{"id": node_id, "successor": node.successor().id if node.successor() else None} for node_id, node in nodes.items()]
    return jsonify({
        "nodes": node_list
    }), 200

@app.route("/join", methods=["POST"])
def join_node():
    """Join a new node to the Chord ring"""
    new_node_id = random.randint(0, MAX-1)
    while new_node_id in nodes:
        new_node_id = random.randint(0, MAX-1)
    
    new_node = Node(new_node_id)
    nodes[new_node_id] = new_node

    new_node.join(initial_node)

    return jsonify({
        "message": "Node joined",
        "node_id": new_node_id
    }), 201

@app.route("/insert", methods=["POST"])
def insert_key():
    # Parse JSON data from the request
    data = request.get_json()
    key = data.get("key")
    value = data.get("value")
    
    if key is None or value is None:
        return jsonify({"error": "Key and value are required"}), 400
    
    initial_node.put(key, value) 

    return jsonify({
        "message": f"Key '{key}' with value '{value}' has been inserted",
        "key": key,
        "value": value,
        "hash_id": hash(key),
        "stored_at_node": initial_node.find_successor(hash(key)).id
    }), 200

@app.route("/get/<key>", methods=["GET"])
def get_value(key):
    hashed_key = hash(key)
    successor = nodes[initial_node.id].find_successor(hashed_key)
    pair = successor.messages.get(hashed_key)

    if pair is None:
        return jsonify({
            "message": "Key not found"
        }), 404
    else:
        return jsonify({
            "key": pair[0],
            "value": pair[1],
            "hash_id": hashed_key,
            "stored_at_node": successor.id 
        }), 200


        
if __name__ == "__main__":
    app.run(debug=True)