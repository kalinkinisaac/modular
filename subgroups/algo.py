def factor(n):
    divisors = dict()
    d = 2
    while d*d <= n:
        while (n % d) == 0:
            if d not in divisors:
                divisors[d] = 1
            else:
                divisors[d] += 1  # supposing you want multiple factors repeated
            n //= d
        d += 1
    if n > 1:
       divisors[n] = 1
    return divisors

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
    _gcd = gcd(a, b)
    c = gcd_ex(_gcd, N)[1]
    return _diophantine(a // _gcd, b // _gcd, c)


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

# def __find_any_solution (int a, int b, int c, int & x0, int & y0, int & g)
# 	g = gcd (abs(a), abs(b), x0, y0);
# 	if (c % g != 0)
# 		return false;
# 	x0 *= c / g;
# 	y0 *= c / g;
# 	if (a < 0)   x0 *= -1;
# 	if (b < 0)   y0 *= -1;
# 	return true;
