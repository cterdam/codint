def perms(line):

    def permsHelper(l, lo, hi):
        if lo == hi:
            print("".join(l))
        else:
            for i in range(lo, hi):
                l[lo], l[i] = l[i], l[lo]
                permsHelper(l, lo+1, hi)
                l[lo], l[i] = l[i], l[lo]

    permsHelper(list(line), 0, len(line))


if __name__ == '__main__':
    perms(input())
