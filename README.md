# Chord DHT Project

This project implements a Chord Distributed Hash Table (DHT) with additional features such as leader election and networking with broadcast/gossip mechanism.

## Project Structure
```
.
├── .gitignore
├── Dockerfile
├── Makefile
├── README.md
├── cleanup_port.py
├── main.py
├── requirements.txt
├── setup.py
├── chord.egg-info/
├── src/
│   ├── chord.py
│   ├── connector.py
├── test/
│   ├── playground.py
│   ├── test_failure_detector.py
│   ├── test_bully_leader_election.py
│   ├── test_chord.py
│   ├── test_network_broadcast.py
│   ├── test_gossiping.py
└── __pycache__/
```

## Prerequisites
- Python 3.12 or higher
- `pip` (Python package installer)

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/onggiahuy97/chord.git
cd chord
```

### 2. Create a Virtual Environment (Optional)
```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Install the Package
```sh
pip install -e .
```

## Running the Project

### 1. Start the Chord DHT Node
```sh
python main.py
```
The server will start on `http://localhost:5000` by default.

### 1.1 Run Simulator of Chord DHT (Optional)
```sh
git clone https://github.com/onggiahuy97/chord_swiftui_protocol
```
You will need macOS (macbook) to run the application.

## API Endpoints

### List All Nodes
```http
GET /nodes
```
**Response Example:**
```json
{
    "nodes": [
        {
            "id": 8,
            "successor": 15,
            "messagesCount": 1
        }
    ]
}
```

### Join Node
```http
POST /join
```
**Response Example:**
```json
{
    "message": "Node joined",
    "node_id": 8
}
```
**Error Response (400):**
```json
{
    "error": "The Chord ring is full"
}
```

### Get Hash
```http
GET /hash?key=<key>
```
**Response Example:**
```json
{
    "hash": 23,
    "successor": 8
}
```

### Insert Key-Value
```http
POST /insert
Content-Type: application/json
```
**Request Body:**
```json
{
    "key": "test",
    "value": "success"
}
```
**Response Example:**
```json
{
    "message": "Key 'test' with value 'success' has been inserted",
    "key": "test",
    "value": "success",
    "hash_id": 27,
    "stored_at_node": 8
}
```

### Get Value
```http
GET /get/<key>
```
**Response Example:**
```json
{
    "key": "test",
    "value": "success",
    "hash_id": 27,
    "stored_at_node": 8
}
```
**Error Response (404):**
```json
{
    "message": "Key not found"
}
```

### Node Leave
```http
POST /leave/<id>
```
**Response Example:**
```json
{
    "message": "Node '25' successfully left the ring."
}
```

### Node Info
```http
GET /info/<id>
```
**Response Example:**
```json
{
    "id": 8,
    "successor": 15,
    "messages": [
        {
            "hash_id": 7,
            "key": "genre1",
            "value": "Rock"
        }
    ]
}
```

## Running Tests
Run all tests:
```sh
make test-all
```

Run individual tests:
```sh
make test-chord
make test-broadcast
make test-leader-election
make test-failure-detector
make test-gossiping
```

## Cleaning Up
Clean up processes on ports 5000-5010:
```sh
python cleanup_port.py
```

## Docker Support
```sh
docker build -t chord .
docker run -p 5000:5000 chord
```

## Project Components
- Chord DHT: [`src/chord.py`](src/chord.py)
- Network Connector: [`src/connector.py`](src/connector.py)
- Leader Election: [`test/test_bully_leader_election.py`](test/test_bully_leader_election.py)
- Broadcast peer-to-peer: [`test/test_network_broadcast.py`](test/test_network_broadcast.py)
- Gossip: [`test/test_gossiping`](test/test_gossiping.py)
- Failure Detector: [`test/test_failure_detector`](test/test_failure_detector.py)

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.
