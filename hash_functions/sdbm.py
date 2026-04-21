def hash_string(s):
    h = 0
    for ch in s:
        h = ord(ch) + (h << 6) + (h << 16) - h
    return h & 0xFFFFFFFFFFFFFFFF