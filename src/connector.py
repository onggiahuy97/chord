import socket
import json
import threading
from typing import Dict, Any
import time

class Connector():
    def __init__(self, node):
        self.node = node
        self.id = self.node.id
        self.host = 'localhost'
        self.port = 5000 + self.node.id
        self.peers: Dict[int, tuple] = {}  # {node_id: (host, port)}
        self.server_socket = None
        self.is_running = False
        self.received_broadcasts = set()

    def start_server(self):
        """Start the node's network server."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.is_running = True

        # Start listening for connections in a separate thread
        thread = threading.Thread(target=self._listen)
        thread.daemon = True
        thread.start()

        print(f"Node {self.id} listening on {self.host}:{self.port}")

    def stop_server(self):
        """Stop the node's network server."""
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
        print(f"Node {self.id} has stopped")

    def _listen(self):
        """Listen for incoming connections."""
        while self.is_running:
            try:
                client, addr = self.server_socket.accept()
                thread = threading.Thread(target=self._handle_client, args=(client,))
                thread.daemon = True
                thread.start()
            except Exception as e:
                if self.is_running:
                    print(f"Error accepting connection: {e}")

    def _handle_client(self, client):
        """Handle incoming client connection."""
        try:
            data = client.recv(4096)
            if data:
                message = json.loads(data.decode())
                response = self._handle_message(message)
                if response:
                    client.send(json.dumps(response).encode())
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client.close()

    def _handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle received message and return response."""
        msg_type = message.get('type')

        if msg_type == 'broadcast':
            # Forward the broadcast
            self.broadcast_message(
                message['message'],
                message['originator_id'],
                message['message_id']
            )
            return {'status': 'ok', 'message': 'Broadcast received'}

        elif msg_type == 'peer_info':
            # Store peer information
            node_id = message['node_id']
            host = message['host']
            port = message['port']
            self.peers[node_id] = (host, port)
            return {'status': 'ok', 'message': 'Peer info stored'}
        
        elif msg_type == 'heartbeat':
        # Acknowledge the heartbeat
            return {'status': 'ok', 'message': 'Heartbeat acknowledged'}
        
        elif msg_type == 'gossip':
            if hasattr(self.node, "merge_gossip"):  # Ensure the method exists
                self.node.merge_gossip(message.get('state', {}))
                return {'status': 'ok', 'message': 'Gossip merged'}
            else:
                return {'status': 'error', 'message': 'Gossip merge not supported'}

    def broadcast_message(self, message: str, originator_id: int = None, message_id: str = None):
        """Broadcast a message to all peers in the network."""
        if originator_id is None:
            originator_id = self.id
        if message_id is None:
            message_id = f"{originator_id}_{time.time()}"

        # If we've already seen this broadcast, ignore it
        if message_id in self.received_broadcasts:
            return

        # Mark this broadcast as received
        self.received_broadcasts.add(message_id)
        print(f"Node {self.id} received broadcast: {message}")

        # Get next node in the ring
        next_node = self.node.successor()
        if next_node.id in self.peers:
            host, port = self.peers[next_node.id]
            broadcast_data = {
                'type': 'broadcast',
                'message': message,
                'originator_id': originator_id,
                'message_id': message_id
            }
            self._send_to_peer(host, port, broadcast_data)

    def _send_to_peer(self, host: str, port: int, data: Dict):
        """Send message to a specific peer."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.send(json.dumps(data).encode())
                response = s.recv(4096)
                return json.loads(response.decode())
        except Exception as e:
            print(f"Error sending to peer {host}:{port}: {e}")
            return None

    def register_peer(self, node_id: int, host: str, port: int):
        """Register network information for a peer."""
        self.peers[node_id] = (host, port)
        print(f"Node {self.id} registered peer {node_id} at {host}:{port}")

        # Send our info to the new peer
        message = {
            'type': 'peer_info',
            'node_id': self.id,
            'host': self.host,
            'port': self.port
        }
        self._send_to_peer(host, port, message)

    def clear_broadcast_history(self):
        """Clear the broadcast history to prevent memory buildup."""
        self.received_broadcasts.clear()

    def send_heartbeat(self, target_id):
        if target_id in self.peers:
            host, port = self.peers[target_id]
            data = {'type': 'heartbeat', 'sender_id': self.id}
            response = self._send_to_peer(host, port, data)
            if response and response.get('status') == 'ok':
                print(f"Heartbeat sent from Node {self.id} to Node {target_id} was acknowledged")
            else:
                print(f"Heartbeat failed for Node {target_id}")

    def send_gossip(self, target_id, state):
        """Send gossip state to a target peer."""
        if target_id in self.peers:
            host, port = self.peers[target_id]
            try:
                data = {
                    'type': 'gossip',
                    'state': {
                        'keys': [(int(k), (str(v[0]), str(v[1]))) for k, v in state.get('keys', [])]
                    }
                }
                response = self._send_to_peer(host, port, data)
                if response and response.get('status') == 'ok':
                    print(f"Gossip sent to Node {target_id} successfully")
                else:
                    print(f"Failed to send gossip to Node {target_id}")
            except Exception as e:
                print(f"Error sending gossip to Node {target_id}: {e}")

    