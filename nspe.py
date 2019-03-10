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
    return [(b*x - a[n]*c) for n, x in enumerate(m)], b


def decrypt(encrypted, password):
    e, b, p = encrypted[0], encrypted[1], string_to_int_arr(password)
    k = len(p)
    f = [b*p[i % k] - x for i, x in enumerate(e)]
    g, h = sum_of_products(f, f), sum_of_products(f, e) << 1
    d = g*b 
    return ''.join(chr((g*x-f[n]*h)//d) for n, x in enumerate(e))


if len(argv) < 2 or (argv[1] not in ['-e', '-d']):
    print('python3 nspe.py [-e|-d]\n-e encrypt\n-d decrypt')
else:
    mode = argv[1]
    if mode == '-e':
        encrypted = encrypt(
            input('Podaj wiadomość do zaszyfrowania:\t'), input('Podaj hasło:\t'))
        print("e = {}\nb = {}".format(encrypted[0], encrypted[1]))
    else:
        print("Wiadomość:\t{}".format(decrypt(([int(x) for x in input('e = ')[
              1:-1].split(',')], int(input('b = '))), input('Podaj hasło:\t'))))
