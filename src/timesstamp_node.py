from src.chord import Node, hash_int


'''

This implementation adds logical timestamps to the Chord system with these key features:

1. **Lamport Logical Clocks**:
   - Each node maintains its own logical clock 
   - Clocks are synchronized based on message passing
   - Ensures causal ordering of events

2. **Timestamped Operations**:
   - All PUT and GET operations are timestamped
   - Messages include sender ID and operation type
   - Maintains operation history with timestamps

3. **Event Logging**:
   - Tracks all operations in an event log
   - Can view sorted history of all events
   - Helps debug and understand system behavior

Example usage:

```python
# Create nodes with timestamps
node1 = TimestampNode(1)
node2 = TimestampNode(2)
node3 = TimestampNode(3)

# Join nodes to create ring
node2.join(node1)
node3.join(node1)

# Perform operations
node1.put("key1", "value1")
node2.put("key2", "value2")
node3.get("key1")
node1.get("key2")

# View event history
node1.print_event_history()
```

The output might look like:
```
Timestamp | Node | Operation | Key | Value
--------------------------------------------------
1         | 1    | PUT       | key1| value1
2         | 2    | PUT       | key2| value2
3         | 3    | GET       | key1| -
4         | 1    | GET       | key2| -
```

This implementation helps:
- Track the order of operations across nodes
- Debug distributed operations
- Ensure consistent event ordering
- Understand system behavior

Would you like me to explain any part in more detail or show how to test specific timing scenarios?
'''

class TimestampNode(Node):
    def __init__(self, id):
        super().__init__(id)
        self.logical_clock = 0  # Lamport clock
        self.message_history = []  # Store message history with timestamps
        self.event_log = []  # Log of all events with timestamps
        
    def increment_clock(self):
        """Increment the logical clock and return new value."""
        self.logical_clock += 1
        return self.logical_clock
        
    def update_clock(self, received_time):
        """Update logical clock based on received message timestamp."""
        self.logical_clock = max(self.logical_clock, received_time) + 1
        
    def put(self, key, value):
        """Put with timestamp."""
        timestamp = self.increment_clock()
        
        # Create timestamped message
        timestamped_msg = {
            'key': key,
            'value': value,
            'timestamp': timestamp,
            'sender_id': self.id,
            'operation': 'PUT'
        }
        
        # Log the event
        self.event_log.append(timestamped_msg)
        
        # Call original put with additional timestamp info
        hashed_key = hash_int(key)
        target_node = self.find_successor(hashed_key)
        target_node.receive_message(timestamped_msg)
        
        print(f"PUT - Key: {key}, Value: {value}, Timestamp: {timestamp}, Node: {target_node.id}")
        
    def get(self, key):
        """Get with timestamp."""
        timestamp = self.increment_clock()
        
        # Create timestamped request
        timestamped_msg = {
            'key': key,
            'timestamp': timestamp,
            'sender_id': self.id,
            'operation': 'GET'
        }
        
        # Log the event
        self.event_log.append(timestamped_msg)
        
        # Perform the get operation
        hashed_key = hash_int(key)
        target_node = self.find_successor(hashed_key)
        result = target_node.receive_message(timestamped_msg)
        
        print(f"GET - Key: {key}, Timestamp: {timestamp}, Node: {target_node.id}")
        return result
        
    def receive_message(self, message):
        """Handle received messages with timestamps."""
        # Update local clock
        self.update_clock(message['timestamp'])
        
        # Process message based on operation type
        if message['operation'] == 'PUT':
            hashed_key = hash_int(message['key'])
            self.messages[hashed_key] = (message['key'], message['value'])
            self.message_history.append(message)
            return True
            
        elif message['operation'] == 'GET':
            hashed_key = hash_int(message['key'])
            return self.messages.get(hashed_key, (None, None))[1]
            
    def get_event_history(self):
        """Return sorted history of events."""
        sorted_history = sorted(self.event_log, 
                              key=lambda x: (x['timestamp'], x['sender_id']))
        return sorted_history
        
    def print_event_history(self):
        """Print the sorted event history."""
        history = self.get_event_history()
        print("\nEvent History:")
        print("Timestamp | Node | Operation | Key | Value")
        print("-" * 50)
        for event in history:
            print(f"{event['timestamp']:9} | {event['sender_id']:4} | "
                  f"{event['operation']:9} | {event['key']:3} | "
                  f"{event.get('value', '-')}")
            
