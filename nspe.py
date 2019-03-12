from sys import argv


def string_to_int_arr(str):
    return [ord(x) for x in str]


def sum_of_products(a, b):
    return sum(x*b[i] for i, x in enumerate(a))


def encrypt(message, password):
    m, p = string_to_int_arr(message), string_to_int_arr(password)
    k = len(p)
    a = [p[i % k] - x for i, x in enumerate(m)]
    b, c = sum_of_products(a, a), sum_of_products(a, m) << 1
    e = [(b*x - a[n]*c + p[n % k] % k) for n, x in enumerate(m)]
    return [x % b for x in e], [x // b for x in e], b


def decrypt(encrypted, password):
    b, p = encrypted[2], string_to_int_arr(password)
    k = len(p)
    e = [b*encrypted[1][i] + x - p[i % k] %
         k for i, x in enumerate(encrypted[0])]
    f = [b*p[i % k] - x for i, x in enumerate(e)]
    g, h = sum_of_products(f, f), sum_of_products(f, e) << 1
    d = g*b
    return ''.join(chr((g*x-f[n]*h)//d) for n, x in enumerate(e))


def parse_int_arr(str):
    return [int(x) for x in str[
        1:-1].split(',')]


if len(argv) < 2 or (argv[1] not in ['-e', '-d']):
    print('python3 nspe.py [-e|-d]\n-e encrypt\n-d decrypt')
else:
    mode = argv[1]
    if mode == '-e':
        encrypted = encrypt(
            input('Podaj wiadomość do zaszyfrowania:\t'), input('Podaj hasło:\t'))
        print("r = {}\nq = {}\nb = {}".format(
            encrypted[0], encrypted[1], encrypted[2]))
    else:
        print("Wiadomość:\t{}".format(decrypt((parse_int_arr(input('r = ')), parse_int_arr(
            input('q = ')), int(input('b = '))), input('Podaj hasło:\t'))))
