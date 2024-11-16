import socket
import json
import threading
from typing import Dict, Any
from .chord import Node, hash_int

class NetworkNode(Node):
    def __init__(self, id: int, host: str, port: int):
        super().__init__(id)
        self.host = host
        self.port = port
        self.peers: Dict[int, tuple] = {}  # {node_id: (host, port)}
        self.server_socket = None
        self.is_running = False
        
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
        
        if msg_type == 'join':
            node_id = message['node_id']
            host = message['host']
            port = message['port']
            self.peers[node_id] = (host, port)
            if self.id == 1:  # If this is the leader
                self.join(self)  # Initialize leader
            return {'status': 'ok', 'message': f'Node {node_id} joined'}
            
        elif msg_type == 'put':
            key = message['key']
            value = message['value']
            super().put(key, value)  # Use the parent class's put method
            return {'status': 'ok', 'message': 'Put successful'}
            
        elif msg_type == 'get':
            key = message['key']
            hashed_key = hash_int(key)
            if hashed_key in self.messages:
                return {'status': 'ok', 'value': self.messages[hashed_key][1]}
            return {'status': 'error', 'message': 'Key not found'}
            
        return {'status': 'error', 'message': 'Unknown message type'}
        
    def join_network(self, id, leader_host: str, leader_port: int):
        """Join the Chord network through a leader node."""
        message = {
            'type': 'join',
            'node_id': self.id,
            'host': self.host,
            'port': self.port
        }
        
        # Connect to leader
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((leader_host, leader_port))
                s.send(json.dumps(message).encode())
                response = s.recv(4096)
                print(f"Join response: {response.decode()}")
                
                    
            except Exception as e:
                print(f"Error joining network: {e}")