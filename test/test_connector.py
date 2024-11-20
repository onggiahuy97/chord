from src.chord import Node
import time

def main():
    n1 = Node(1)
    n1.connector.start_server()

    n2 = Node(2)
    n2.connector.start_server()

    n1.join(n1)
    n2.join(n1)

    n1.connector.register_peer(n2.id, n2.connector.host, n2.connector.port)


    test_message = "Test broadcast message"
    n1.connector.broadcast_message(test_message)
    time.sleep(1)  # Allow for message propagation


    n1.connector.stop_server()
    n2.connector.stop_server()

if __name__ == "__main__":
    main()
