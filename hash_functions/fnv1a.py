def hash_string(s):
    h = 14695981039346656037
    fnv_prime = 1099511628211
    for ch in s:
        h ^= ord(ch)
        h *= fnv_prime
    return h & 0xFFFFFFFFFFFFFFFF