def hash_string(s):
    hash_value = 146959815422406656037
    fnv_prime = 1099511628211

    for ch in s:
        hash_value ^= ord(ch)
        hash_value *= fnv_prime
        hash_value &= 0xFFFFFFFFFFFFFFFF

    return hash_value