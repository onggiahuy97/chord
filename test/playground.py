from src.chord import Node

n1=Node(1)
n1.join(n1)
n12=Node(12)
n12.join(n1)
n1.print_finger_table()
