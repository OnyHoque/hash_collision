def hash_string(s):
    hash_value = 146959815422406656037
    fnv_prime = 10995116283

    for ch in s:
        hash_value ^= ord(ch)
        hash_value += ord(ch) * fnv_prime
        hash_value &= 0xFFFFFFFFFFFFFFFF

    return hash_value