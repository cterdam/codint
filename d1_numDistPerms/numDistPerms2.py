import math


def numDistPerms(line):
    tally = [line.count(c) for c in set(line)]
    base = math.factorial(len(line))
    for count in tally:
        base //= math.factorial(count)
    return base


if __name__ == '__main__':
    print(numDistPerms(input()))
