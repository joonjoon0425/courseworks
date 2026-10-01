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

def LNDS_with_answer(arr):
    """
    LNDS with the solution array
    Since dp[k] is the length fo LNDS when the last element is arr[k], we can record the index when using it, as prev.
    """
    dp = [0] * len(arr)
    prev = [-1] * len(arr)
    dp[0] = 1
    for k in range(len(arr)):
        m = 0
        for i in range(k):
            if arr[i] <= arr[k]:
                if m < dp[i]:
                    m = dp[i]
                    prev[k] = i
        dp[k] = m + 1

    # retrieve the solution array
    val, idx = 0, 0
    for last in range(len(arr)):
        if val < dp[last]:
            val = dp[last]
            idx = last

    ans = []

    while True:
        if idx == -1:
            break
        ans.insert(0, arr[idx])
        idx = prev[idx]
    
    return val, ans

if __name__ == "__main__":
    arr = [0, 1, 0, 2, 1, 2, 4, 5, 3]
    sol, ans = LNDS_with_answer(arr)
    print(sol)
    print(ans)