from .algo import factor


def one2many(one, fact=None):
    a, b, N = one
    many = []
    if not fact:
        fact = factor(N)

    for divisor in fact:
        n = divisor ** fact[divisor]
        many.append([a % n, b % n, [divisor, fact[divisor]]])
    return many

def many2one(many):
    a = 0
    b = 0
    N = 1

    for a_i, b_i, [p_i, m_i] in many:
        N *= p_i ** m_i

    for a_i, b_i, [p_i, m_i] in many:
        a += a_i * (N // p_i ** m_i) ** ((p_i - 1) * p_i ** (m_i - 1))
        b += b_i * (N // p_i ** m_i) ** ((p_i - 1) * p_i ** (m_i - 1))

    return [a % N, b % N, N]
