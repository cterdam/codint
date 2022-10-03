def passwordStrength(s):
    ans = 0
    for i in range(len(s)):
        for j in range(len(s) - i + 1):
            ans += len(set(s[i:i+j]))
    return ans


if __name__ == '__main__':
    s = input()
    print(passwordStrength(s))
