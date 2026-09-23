"""
Obtain the length of longest non-decreasing subsequence
"""

def LNDS(arr):
    """
    dp[k] = the length of LNDS when the last element is arr[k]
    """
    dp = [0] * len(arr)
    dp[0] = 1
    for k in range(len(arr)):
        m = 0
        for i in range(k):
            if arr[i] <= arr[k]:
                m = max(m, dp[i])
        dp[k] = m + 1
    return max(dp)

if __name__ == "__main__":
    arr = [2, 1, 2, 4, 5, 3]
    sol = LNDS(arr)
    print(sol)