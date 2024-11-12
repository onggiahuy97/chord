import hashlib

# m is the fixed number of bits
def hash(key):
    return int(hashlib.sha1(key.encode()).hexdigest(), 16) % (2 ** m)
    