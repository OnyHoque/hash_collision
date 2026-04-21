import hashlib

def hash_string(s):
    return int(hashlib.md5(s.encode("utf-8")).hexdigest(), 16)