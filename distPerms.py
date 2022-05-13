# Input: a string with only capital English letters
# Task: return a list of all distinct permutations of this string


def distPerms(line):

    def insert(s, c, n):
        # For string s, char c, number n:
        # Returns a list of different strings, each string a result of
        # inserting n copies of c into the original string s, without changing
        # the internal order of s.
        if s == "":
            return [c * n]
        if n == 0:
            return [s]
        elif n == 1:
            buildup = []
            for i in range(len(s)+1):
                buildup.append(s[:i] + c + s[i:])
            return buildup
        else:
            buildup = []
            for k in range(n+1):
                for p in insert(s[1:], c, n-k):
                    buildup.append(c*k + s[0] + p)
            return buildup

    def distPermsHelper(tally):
        if len(tally) == 0:
            return [""]
        if len(tally) == 1:
            return [c * tally[c] for c in tally]
        else:
            # For each char, first permute the rest. Then insert the right
            # number of this char into the permutations of the rest.
            currChar = list(tally.keys())[0]
            currCount = tally[currChar]
            del tally[currChar]
            buildup = []
            for p in distPermsHelper(tally):
                buildup += insert(p, currChar, currCount)
            return buildup

    tally = {c: line.count(c) for c in set(line)}
    return distPermsHelper(tally)
