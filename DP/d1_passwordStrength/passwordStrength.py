def passwordStrength(s):
    lastAppear = {c: -1 for c in 'abcdefghijklmnopqrstuvwxyz'}
    score = 0
    toAdd = 0
    for i in range(len(s)):
        toAdd += i - lastAppear[s[i]]
        score += toAdd
        lastAppear[s[i]] = i
    return score


if __name__ == '__main__':
    s = input()
    print(passwordStrength(s))
