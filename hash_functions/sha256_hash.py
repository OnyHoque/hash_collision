import hashlib

def hash_string(s):
    return int(hashlib.sha256(s.encode("utf-8")).hexdigest(), 16)