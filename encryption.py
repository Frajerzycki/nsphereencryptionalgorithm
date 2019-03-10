

def string_to_int_arr(str):
    return [ord(x) for x in str]


def int_arr_to_string(int_arr):
    return ''.join(chr(x) for x in int_arr)


def encrypt(message, password):
    m = string_to_int_arr(message)
    p = string_to_int_arr(password)
    a = [p[i % len(p)] - x for i, x in enumerate(m)]
    b = sum(x*x for x in a)
    c = sum(x*a[i] for i, x in enumerate(m))
    return [(b*x - a[n]*c*2) for n, x in enumerate(m)], b


def decrypt(encrypted, password):
    e, b = encrypted[0], encrypted[1]
    p = string_to_int_arr(password)
    f = [b*p[i % len(p)] - x for i, x in enumerate(e)]
    g = sum(x*x for x in f)
    h = sum(x*f[i] for i, x in enumerate(e))
    return int_arr_to_string((g*x-2*f[n]*h)//(g*b) for n, x in enumerate(e))


password = "Niezłamywalne hasełko!@#"
print(decrypt(encrypt("Nic tutaj nie ma i nie będzie!@#", password), password))
