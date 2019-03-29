from sys import argv
from re import sub
from secrets import randbits


def string_to_int_arr(str):
    return [ord(x) for x in str]


def sum_of_products(a, b):
    return sum(x*b[i] for i, x in enumerate(a))


def encrypt(m, p, w):
    k = len(p)
    d = len(w)
    a = [p[i % k] - x for i, x in enumerate(m)]
    b, c = sum_of_products(a, a), sum_of_products(a, m) << 1
    e = [b*x - a[n]*c for n, x in enumerate(m)]
    return [(x // b, x % b + w[i % d]) for i, x in enumerate(e)], b


def decrypt(q, b, p, w):
    k = len(p)
    d = len(w)
    e = [b*x[0] + x[1] - w[i % d] for i, x in enumerate(q)]
    f = [b*p[i % k] - x for i, x in enumerate(e)]
    g, h = sum_of_products(f, f), sum_of_products(f, e) << 1
    d = g*b
    return ''.join(chr((g*x-f[n]*h)//d) for n, x in enumerate(e))


def parse_tuple_int_arr(str):
    return [tuple(int(y) for y in sub("\\(|\\)", '', x).split(',')) for x in str.replace(' ', '')[
        1:-1].split('),')]


def parse_int_arr(str):
    return [int(x) for x in str[
        1:-1].split(',')]


def generate_w(length):
    def f(x):
        if x == 1:
            return 1
        return -1
    return [f(randbits(1)) * randbits(10) for _ in range(0, length)]



def check(m, p):
    k = len(p)
    for i, x in enumerate(m):
        if x != p[i % k]:
            return True
    return False


if len(argv) < 2 or (argv[1] not in ['-e', '-d', '-gp']):
    print('python3 nspe.py [-e|-d|-gp] [length (if -gp)] \n-e - encrypt\n-d - decrypt\n-gp - generates one part of password')
else:
    mode = argv[1]
    if mode == '-e':
        m = string_to_int_arr(input('Enter a message:\t'))
        p = parse_int_arr(input('Enter the first part of key (as list of numbers):\t'))
        w = parse_int_arr(input('Enter the second part of key (as list of numbers):\t'))

        if not check(m, p):
            print(
                "Message and firt part of password have to have at least one different letter.")
        else:
            encrypted = encrypt(m, p, w)
            print("Encrypted message:\t{}\nb = {}".format(
                encrypted[0], encrypted[1]))
    elif mode == '-d':
        q = parse_tuple_int_arr(input('Enter the encrypted message:\t'))
        p = parse_int_arr(input('Enter the first part of key (as list of numbers):\t'))
        w = parse_int_arr(input('Enter the second part of key (as list of numbers):\t'))
        b = int(input('b = '))
        print("Message:\t{}".format(decrypt(q, b, p, w)))
    elif mode == '-gp':
        print(generate_w(int(argv[2])))
