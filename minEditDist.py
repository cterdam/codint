# Input: Two strings
# Task: Compute the minimum edit distance between the two

def minEditDist(s1, s2):

    dp = [[-1 for i in range(len(s1) + 1)] for j in range(len(s2) + 1)]

    for i in range(len(s2) + 1):
        for j in range(len(s1) + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s2[i-1] == s1[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1

    return dp[-1][-1]
