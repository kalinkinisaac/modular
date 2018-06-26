# TODO: this solution is not optimal. Should be replaced with faster one
def factor(n):
    divisors = dict()
    d = 2

    while d*d <= n:
        while (n % d) == 0:

            if d not in divisors:
                divisors[d] = 1
            else:
                divisors[d] += 1

            n //= d
        d += 1

    if n > 1:
       divisors[n] = 1

    return list(zip(divisors.keys(), divisors.values()))


def inv_element(a, N):
    g, x, y = gcd_ex(a, N)
    if g != 1:
        return -1
    else:
        return (x % N + N) % N

def gcd_ex(a, b):
    if a == 0:
        return b, 0, 1

    d, x1, y1 = gcd_ex(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y

def gcd(a, b):
    return gcd_ex(a, b)[0]


def get_xy(a, b, N):
    g = gcd(a, b)
    c = gcd_ex(g, N)[1]
    return _diophantine(a // g, b // g, c)


def _diophantine(a, b, c):
    g, x_0, y_0 = gcd_ex(abs(a), abs(b))

    if g == 0 or c % g != 0:
        return -1

    x_0 *= c // g
    y_0 *= c // g

    if (a < 0):
        x_0 *= -1
    if (b < 0):
        y_0 *= -1

    return [x_0, y_0]
