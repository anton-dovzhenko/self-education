import math


def get_price_with_binomial(otype, oclass, asset, sigma, ir, strike, dt, steps, print_details=True):
    if otype not in ['C', 'P']:
        raise ValueError("otype must be 'C' or 'P'")
    if oclass not in ['eu', 'us']:
        raise ValueError("oclass must be 'eu' or 'us'")

    discount = math.exp(-ir * dt)
    u = discount + math.exp((ir + sigma ** 2) * dt)
    u = 0.5 * (u + (u ** 2 - 4) ** 0.5)
    v = 1 / u
    p = (math.exp(ir * dt) - v) / (u - v)

    tree = [[asset]]
    for i in range(steps):
        tree.append([p * v for p in tree[-1]] + [tree[-1][-1] * u])

    prices = [[_payoff(p, strike, otype) for p in tree[-1]]]
    for i in range(steps):
        previous = []
        for j in range(len(prices[-1]) - 1):
            if otype == 'eu':
                previous.append(discount * (p * prices[-1][j + 1] + (1 - p) * prices[-1][j]))
            else:
                previous.append(
                    max(
                        discount * (p * prices[-1][j + 1] + (1 - p) * prices[-1][j]),
                        _payoff(tree[steps - i - 1][j], strike, otype)
                    ))
        prices.append(previous)
    prices.reverse()

    if print_details:
        print("u=%s, v=%s, p=%s" % (u, v, p))
        print("tree = %s" % tree)
        print("prices = %s" % prices)

    return prices[0][0]


def _payoff(price, strike, otype):
    if otype == 'C':
        return max(0, price - strike)
    elif otype == 'P':
        return max(0, strike - price)
    else:
        raise ValueError("'C' or 'P' otype was expected, but '%s' received" % otype)


# print(get_price_with_binomial('C', 'eu', 100, 0.2, 0.1, 100, 1 / 12, 4, print_details=False))
# print(get_price_with_binomial('P', 'eu', 100, 0.2, 0.1, 100, 1 / 12, 4, print_details=False))
# print(get_price_with_binomial('C', 'us', 100, 0.2, 0.1, 100, 1 / 12, 4, print_details=False))
# print(get_price_with_binomial('P', 'us', 100, 0.2, 0.1, 100, 1 / 12, 4, print_details=False))


# print(get_price_with_binomial('C', 'eu', 100, 0.2, 0.06, 99, 1 / 50, 50, print_details=False))
# print(get_price_with_binomial('P', 'eu', 100, 0.2, 0.06, 99, 1 / 50, 50, print_details=False))
# print(get_price_with_binomial('C', 'us', 100, 0.2, 0.06, 99, 1 / 50, 50, print_details=False))
# print(get_price_with_binomial('P', 'us', 100, 0.2, 0.06, 99, 1 / 50, 50, print_details=False))

print(get_price_with_binomial('C', 'us', 63, 0.09523809523809523, 0.04, 61, 1 / 4, 2, print_details=False))
print(get_price_with_binomial('P', 'us', 63, 0.09523809523809523, 0.04, 61, 1 / 4, 2, print_details=False))

