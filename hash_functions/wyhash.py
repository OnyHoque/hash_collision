def hash_string(s):
    data = s.encode("utf-8")

    mask = 0xFFFFFFFFFFFFFFFF
    secret = (
        0xa0761d6478bd642f,
        0xe7037ed1a0b428db,
        0x8ebc6af09c88c6e3,
        0x589965cc75374cc3,
    )

    def wyr8(b):
        return int.from_bytes(b, "little")

    def wyr4(b):
        return int.from_bytes(b, "little")

    def wymum(a, b):
        product = (a * b) & ((1 << 128) - 1)
        return ((product >> 64) ^ product) & mask

    def mix(a, b):
        return wymum(a ^ secret[0], b ^ secret[1])

    n = len(data)
    seed = n & mask
    i = 0

    while n >= 16:
        a = wyr8(data[i:i+8])
        b = wyr8(data[i+8:i+16])
        seed = mix(a ^ seed, b)
        i += 16
        n -= 16

    if n >= 8:
        a = wyr8(data[i:i+8])
        b = wyr8(data[i+n-8:i+n])
        return mix(a ^ seed ^ secret[2], b ^ seed ^ secret[3])

    if n >= 4:
        a = wyr4(data[i:i+4])
        b = wyr4(data[i+n-4:i+n])
        return mix((a | (b << 32)) ^ seed ^ secret[2], n ^ secret[3])

    if n > 0:
        tail = 0
        for j in range(n):
            tail |= data[i+j] << (j * 8)
        return mix(tail ^ seed ^ secret[2], n ^ secret[3])

    return mix(seed ^ secret[2], secret[3])