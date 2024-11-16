test-chord:
	python3 test/test_chord.py

test-network:
	python3 test/test_network.py

test-broadcast:
	python3 test/test_node_broadcast.py 

test-leader-selection:
	python3 test/test_select_new_leader.py 

test-all: test-chord test-network test-broadcast test-leader-selection
