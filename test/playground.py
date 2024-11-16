from src.chord import Node

n1=Node(1)
n12=Node(12)
n24=Node(24)
n18=Node(18)
n9=Node(9)
n1.join(n1)
n12.join(n1)
n24.join(n1)
n18.join(n1)
n9.join(n1)

print(n1.leader_id)
n1.start_election()
print(n1.leader_id)

# n1.print_finger_table()
print(n9.leader_id)