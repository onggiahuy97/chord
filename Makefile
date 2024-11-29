test-all:
	make test-chord test-gossiping test-broadcast test-leader-election test-failure-detector

test-chord:
	python3 test/test_chord.py

test-broadcast:
	python3 test/test_network_broadcast.py

test-leader-election:
	python3 test/test_bully_leader_election.py

test-failure-detector:
	python3 test/test_failure_detector.py

test-gossiping:
	python3 test/test_gossiping.py

