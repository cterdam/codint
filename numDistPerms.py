# Input: a string with only capital English letters
# Task: return the number of distinct permutations of this string

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


def numDistPerms2(line):
    tally = [line.count(c) for c in set(line)]
    base = math.factorial(len(line))
    for count in tally:
        base //= math.factorial(count)
    return base
