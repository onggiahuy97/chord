import random
import hashlib
from typing import Optional

k = 4
MAX = 2**k

def id():
    return long(random.uniform(0,2**k))

def decr(value,size):
    if size <= value:
        return value - size
    else:
        return MAX-(size-value)
        
def between(value,init,end):
    if init == end:
        return True
    elif init > end :
        shift = MAX - init
        init = 0
        end = (end +shift)%MAX
        value = (value + shift)%MAX
    return init < value < end

def Ebetween(value,init,end):
    if value == init:
        return True
    else:
        return between(value,init,end)

def betweenE(value,init,end):
    if value == end:
        return True
    else:
        return between(value,init,end)

def hash(key):
    return int(hashlib.sha1(key.encode()).hexdigest(), 16) % (2 ** k)
    
class Node:
    def __init__(self,id):
        self.id = id
        self.finger = {}
        self.start = {}
        self.messages = {}
        for i in range(k):
            self.start[i] = (self.id+(2**i)) % (2**k)

    def successor(self):
        return self.finger[0] 

    def find_successor(self,id):  
        if betweenE(id,self.predecessor.id,self.id):
            return self
        n = self.find_predecessor(id)
        return n.successor()
    
    def find_predecessor(self,id):
        if id == self.id:
            return self.predecessor
        n1 = self
        while not betweenE(id,n1.id,n1.successor().id):
            n1 = n1.closest_preceding_finger(id)
        return n1
    
    def closest_preceding_finger(self,id):
        for i in range(k-1,-1,-1):
            if between(self.finger[i].id,self.id,id):
                return self.finger[i]
        return self
        
    
    def join(self,n1):
        if self == n1:
            for i in range(k):
                self.finger[i] = self
            self.predecessor = self
        else:
            self.init_finger_table(n1)
            self.update_others()  
            self.move_keys() 
        
    def move_keys(self):
        """Transfer keys from successor to this node for which this node is now responsible."""
        # Get the current successor
        successor = self.successor()
        
        # Identify the range of keys this node should take responsibility for
        keys_to_move = {}
        
        # Transfer keys in the interval (predecessor.id, self.id]
        for hashed_key, (key, value) in successor.messages.items():
            if betweenE(hashed_key, self.predecessor.id, self.id):
                keys_to_move[hashed_key] = (key, value)
        
        # Move keys to the new node's storage
        self.messages.update(keys_to_move)
        
        # Remove moved keys from the successor
        for hashed_key in keys_to_move:
            del successor.messages[hashed_key]
        
        print(f"Node {self.id} has moved {len(keys_to_move)} keys from Node {successor.id}")
            
    def init_finger_table(self,n1):
        self.finger[0] = n1.find_successor(self.start[0])
        self.predecessor = self.successor().predecessor
        self.successor().predecessor = self
        self.predecessor.finger[0] = self
        for i in range(k-1):
            if Ebetween(self.start[i+1],self.id,self.finger[i].id):
                self.finger[i+1] = self.finger[i]
            else :
                self.finger[i+1] = n1.find_successor(self.start[i+1])

    def update_others(self):
        for i in range(k):
            prev  = decr(self.id,2**i)
            p = self.find_predecessor(prev)
            if prev == p.successor().id:
                p = p.successor()
            p.update_finger_table(self,i)
            
    def update_finger_table(self,s,i):
        if Ebetween(s.id,self.id,self.finger[i].id) and self.id!=s.id:
                self.finger[i] = s
                p = self.predecessor
                p.update_finger_table(s,i)

    def update_others_leave(self):
        for i in range(k):
            prev  = decr(self.id,2**i)
            p = self.find_predecessor(prev)
            p.update_finger_table(self.successor(),i)

    def leave(self):
        """Transfer keys to successor and update the ring to remove this node."""
        successor = self.successor()
        predecessor = self.predecessor
        
        # Step 1: Transfer all keys in this node's `messages` to the successor
        if successor:
            successor.messages.update(self.messages)  # Transfer all keys to successor
            print(f"Node {self.id} transferred {len(self.messages)} keys to Node {successor.id}")
        
        # Step 2: Update predecessor and successor pointers to remove this node
        if successor and predecessor:
            successor.predecessor = predecessor  # Successor's predecessor now points to this node's predecessor
            predecessor.setSuccessor(successor)  # Predecessor's successor now points to this node's successor
        
        # Step 3: Clear this node's messages and finger table to detach it from the ring
        self.messages.clear()
        self.finger.clear()
        self.predecessor = None
        
        # Notify the rest of the ring about the departure if the finger table is populated
        if self.finger:
            self.update_others_leave()
        
        print(f"Node {self.id} has left the ring")

    # not checked 
    # def leave(self):
    #     self.successor().predecessor = self.predecessor
    #     self.predecessor.setSuccessor(self.successor())
    #     self.update_others_leave()
        
    def setSuccessor(self,succ):
        self.finger[0] = succ

    def put(self, key, value):
        hashed_key = hash(key)
        target_node = self.find_successor(hashed_key)
        target_node.messages[hashed_key] = (key, value)
        print(f"Hash: '{hash(key)}' Key '{key}' with value '{value}' stored at Node {target_node.id}")
        