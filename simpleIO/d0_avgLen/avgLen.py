def avgLen(line):
    linesplit = line.split()

    if len(linesplit) == 0:
        return 0

    lens = [len(x) for x in linesplit]
    ans = round((sum(lens) / len(lens)), 2)

    return int(ans) if ans == int(ans) else ans


if __name__ == '__main__':
    print(avgLen(input()))
