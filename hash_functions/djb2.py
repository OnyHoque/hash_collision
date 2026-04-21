def hash_string(s):
    h = 5381
    for ch in s:
        h = ((h << 5) + h) + ord(ch)   # h * 33 + ord(ch)
    return h & 0xFFFFFFFFFFFFFFFF