test-chord:
	python3 test/test_chord.py

test-broadcast:
	python3 test/test_network_broadcast.py 

test-leader-election:
	python3 test/test_bully_leader_election.py 

test-all: test-chord test-broadcast test-leader-selection
