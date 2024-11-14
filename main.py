from flask import Flask, request, jsonify
import random
from random import choice
from src.chord import Node, hash_int

app = Flask(__name__)

# Initialize the Chord DHT with k bits and max nodes
m = 5
MAX = 2**m
nodes = {}

# Create the initial Chord node
leader_node = Node(random.randint(0, MAX-1))
leader_node.join(leader_node)
nodes[leader_node.id] = leader_node

@app.route("/nodes", methods=["GET"])
def list_nodes():
    """List all nodes in the Chord ring"""
    node_list = [
        {
            "id": node_id,
            "successor": node.successor().id if node.successor() else "",
            "messagesCount": len(node.messages)
        } for node_id, node in nodes.items()]
    return jsonify({
        "nodes": node_list
    }), 200

@app.route("/join", methods=["POST"])
def join_node():
    """Join a new node to the Chord ring"""
    # Check if the ring is full
    if len(nodes) >= MAX:
        print("The Chord ring is full.")
        return jsonify({
            "error": "The Chord ring is full"
        }), 400

    new_node_id = random.randint(0, MAX - 1)
    while new_node_id in nodes:
        new_node_id = random.randint(0, MAX - 1)

    new_node = Node(new_node_id)
    nodes[new_node_id] = new_node

    # If nodes is empty, set the initial node
    global leader_node
    if len(nodes) == 1:  # This is the first node joining the ring
        leader_node = new_node
        leader_node.join(leader_node)  # Initial node joins itself
    else:
        new_node.join(leader_node)

    return jsonify({
        "message": "Node joined",
        "node_id": new_node_id
    }), 201

# @app.route("/join/<int:id>", methods="POST")
# def join(id):
#     if id in nodes:
#         return jsonify({
#             "message": f"Node with id '{id} already in the Chord"
#         })

#     new_node = Node(id)
#     new_node.join(initial_node)

#     return jsonify({
#         "message": "Node joined",
#         "node_id": new_node.id
#     }), 201

@app.route("/insert", methods=["POST"])
def insert_key():
    # Parse JSON data from the request
    data = request.get_json()
    key = data.get("key")
    value = data.get("value")

    if key is None or value is None:
        return jsonify({"error": "Key and value are required"}), 400

    if len(nodes) == 0:
        join_node()

    leader_node.put(key, value)

    return jsonify({
        "message": f"Key '{key}' with value '{value}' has been inserted",
        "key": key,
        "value": value,
        "hash_id": hash_int(key),
        "stored_at_node": leader_node.find_successor(hash_int(key)).id
    }), 200

@app.route("/get/<key>", methods=["GET"])
def get_value(key):

    if len(nodes) == 0:
        return jsonify({
            "message": "All servers are down. Please come back sometimes later."
        }), 404

    hashed_key = hash_int(key)
    successor = nodes[leader_node.id].find_successor(hashed_key)
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

@app.route("/leave/<int:id>", methods=["POST"])
def leave(id):
    # Check if the node exists
    if id not in nodes:
        return jsonify({"error": f"Node '{id}' not found in the ring."}), 404

    # Call the leave method on the node
    nodes[id].leave()

     # Check if the leaving node is the initial node
    global leader_node  # Use global keyword to modify the global variable
    if leader_node.id == id:
        # Choose a random node from the remaining nodes as the new initial node
        if len(nodes) > 1:  # Ensure there are nodes left to choose from
            random_node_id = choice(list(nodes.keys()))
            while random_node_id == id:  # Ensure we don't pick the same node
                random_node_id = choice(list(nodes.keys()))
            leader_node = nodes[random_node_id]

    # Remove the node from the nodes dictionary
    del nodes[id]

    return jsonify({
        "message": f"Node '{id}' successfully left the ring."
    }), 200

@app.route("/info/<int:id>", methods=["GET"])
def get_info(id):
    if id not in nodes:
        return jsonify({"error": f"Node '{id}' not found in the ring."}), 404

    # Format messages to be more readable
    # formatted_messages = {
    #     str(hash_id): {
    #         "key": key,
    #         "value": value
    #     }
    #     for hash_id, (key, value) in nodes[id].messages.items()
    # }

    formatted_messages = [
        {
            "hash_id": hash_id,
            "key": key,
            "value": value
        } for hash_id, (key, value) in nodes[id].messages.items()
    ]

    return jsonify({
        "id": id,
        "sucessor": nodes[id].successor().id,
        "messages": formatted_messages
    })


if __name__ == "__main__":
    app.run()
