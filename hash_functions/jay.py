def hash_string(message):
    salt = 'MichaelLangston'

    message_len = len(message)
    salt_len = len(salt)

    def xorstrings(s1, s2):
        return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

    def pad_or_trim(s, length):
        return (s * (length // len(s) + 1))[:length]

    retun = salt

    padded_message = pad_or_trim(message, salt_len * ((message_len // salt_len) + 1))

    for index in range((message_len + salt_len - 1) // salt_len):
        chunk = padded_message[index * salt_len: index * salt_len + salt_len]
        xors = xorstrings(salt, chunk)
        retun = xorstrings(xors, retun)

    return int(retun.encode().hex(), 16)