import math


def numDistPerms(line):

    # A function to determine the number of ways to fit n balls into k
    # buckets, with indistinguishable balls and distinguishable buckets
    def bucketfit(n, k):
        return math.comb(n+k-1, k-1)

    # Determine unique characters and repeated characters (with frequency)
    uniqueChars = set()
    repeatedChars = {}
    for c in set(line):
        freq = line.count(c)
        if freq == 1:
            uniqueChars.add(c)
        else:
            repeatedChars[c] = freq

    # First form basic permutations based on unique characters
    # Then for each repeated character, find ways to insert them into the string
    currLen = len(uniqueChars)
    currPerms = math.factorial(currLen)
    for c in repeatedChars:
        thisLen = repeatedChars[c]
        currPerms *= bucketfit(thisLen, currLen+1)
        currLen += thisLen

    return currPerms


if __name__ == '__main__':
    print(numDistPerms(input()))
