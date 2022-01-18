import hashlib
import itertools as it

def phash(o): return to_base(abs(int(hashlib.md5(o.encode('utf-8')).hexdigest(), 16)), 62)
def to_base(n, b, s='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    rep = ''
    for x in reversed(list(it.takewhile(lambda x: x < n, map(lambda x: b**x, it.count(0))))):
        rep += s[n // x]
        n %= x
    return rep

