from src.chord import Node

n1 = Node(1)
n1.join(n1)

n2 = Node(2)
n2.join(n1)

n18 = Node(18)
n18.join(n1)

n1.print_finger_table()
n2.print_finger_table()
n18.print_finger_table()
