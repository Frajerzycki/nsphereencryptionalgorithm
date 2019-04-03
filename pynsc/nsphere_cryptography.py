from sys import argv
from re import sub
from secrets import randbelow



def sum_of_products(a, b):
    return sum(x*b[i] for i, x in enumerate(a))


def encrypt(message, key1, key2):
    key1_length, key2_length, m = len(key1), len(
        key2), [ord(char) for char in message]
    a = [key1[i % key1_length] - x for i, x in enumerate(m)]
    b, c = sum_of_products(a, a), sum_of_products(a, m) << 1
    e = [b*x - a[i]*c for i, x in enumerate(m)]
    encrypted_last = len(m) << 1
    encrypted = (encrypted_last + 1)*[0]
    for j, i in enumerate(range(1, encrypted_last, 2)):
        encrypted[i - 1] = int(e[j] / b)
        encrypted[i] = e[j] - encrypted[i-1]*b + key2[j % key2_length]
    encrypted[encrypted_last] = b
    return encrypted


def decrypt(encrypted_message, key1, key2):
    key1_length, key2_length, b = len(key1), len(key2), encrypted_message[-1]
    e = [b*encrypted_message[i-1] + encrypted_message[i] - key2[j % key2_length]
         for j, i in enumerate(range(1, len(encrypted_message) - 1, 2))]
    f = [b*key1[i % key1_length] - x for i, x in enumerate(e)]
    g, h = sum_of_products(f, f), sum_of_products(f, e) << 1
    d = g*b
    return ''.join(chr((g*x-f[n]*h)//d) for n, x in enumerate(e))


def generate_key(length, min_inclusive, max_exclusive):
    return [randbelow(max_exclusive-min_inclusive)+min_inclusive for _ in range(0, length)]

key1 = [-445, -271, 707, -632, 477, -281, -572, 964, 889, -882]
key2 = [-36, 530, 986, 313, -957, -353, -456, 957, 116, 480]
print(encrypt("kiti",key1, key2))
