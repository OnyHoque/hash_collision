def hash_string(s):
    hash_value = 572636423275723626223
    prev_ch_int = 1

    for ch in s:
        ch_int = ord(ch)
        hash_value *= ch_int
        hash_value *= prev_ch_int
        prev_ch_int = ch_int

    return hash_value