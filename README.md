# Chord DHT Project

This project implements a Chord Distributed Hash Table (DHT) with additional features such as leader election and timestamped operations.

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
│   ├── network_node.py
│   ├── timestamp_node.py
├── test/
│   ├── playground.py
│   ├── test.py
│   ├── test_bully_leader_election.py
│   ├── test_chord.py
│   ├── test_network_broadcast.py
└── __pycache__/
```

## Prerequisites

- Python 3.12 or higher
- `pip` (Python package installer)

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/chord-dht.git
cd chord-dht
```

### 2. Create a Virtual Environment

It is recommended to create a virtual environment to manage dependencies:

```sh
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python packages using `pip`:

```sh
pip install -r requirements.txt
```

### 4. Install the Package

Install the package in editable mode:

```sh
pip install -e .
```

## Running the Project

### 1. Start the Chord DHT Node

Run the main application to start a Chord DHT node:

```sh
python main.py
```

The server will start on `http://localhost:5001` by default.

### 2. Using Docker (Optional)

You can also run the project using Docker:

```sh
docker build -t chord-dht .
docker run -p 5001:5001 chord-dht
```

## Running Tests

You can run all tests using the `Makefile`:

```sh
make test-all
```

Or run individual test files:

```sh
make test-chord
make test-broadcast
make test-leader-election
```

## Cleaning Up

To clean up any processes running on ports between 5000 and 5010, you can use the `cleanup_port.py` script:

```sh
python cleanup_port.py
```

## Project Components

### 1. Chord DHT

The main implementation of the Chord DHT is in the [`src/chord.py`](src/chord.py) file.

### 2. Network Connector

Network communication is handled by the [`src/connector.py`](src/connector.py) file.

### 3. Timestamped Node

Timestamped operations are implemented in the [`src/timestamp_node.py`](src/timestamp_node.py) file.

### 4. Leader Election

Leader election logic is tested in the [`test/test_bully_leader_election.py`](test/test_bully_leader_election.py) file.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
