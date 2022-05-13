# Input: a string with only English letters and whitespace
# Task: compute the average word length of this string

def avgLen(line):
    linesplit = line.split()

    if len(linesplit) == 0:
        return 0

    lens = [len(x) for x in linesplit]
    return round((sum(lens) / len(lens)), 2)
