
def calc_rate(n, r):
    return (r * (1+r)**n)/((1+r)**n-1)

def pay(a, n, r):
    return a * 10000 * calc_rate(n, r/12/100)

year=30
total=297
rate=5.1

print(f'{year} years, total {total}w')
while rate > 2.0:
    v=pay(total, year*12, rate)
    print(f'{rate:.1f}%: {v:.2f}')
    rate -= 0.5
