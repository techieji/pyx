import string
from hashlib import md5

HASH_CHARS = string.digits + string.ascii_letters

def phash(o):
    return to_base(int(md5(bytes(o, encoding='utf-8')).hexdigest(), 16), len(HASH_CHARS))

def to_base(n, b, s=HASH_CHARS):
    powers = [1]
    while powers[-1] < n:
        powers.append(powers[-1] * b)
    powers = reversed(powers[:-1])
    rep = ""
    for x in powers:
        i, n = divmod(n, x)
        rep += s[i]
    return rep
