import math

"""
Problem:
Given a sequence of numbers {P_1, ..., P_n}, find the length of longest strictly increasing subsequence starting from the first element (longest rising trend).
"""

def rt(arr):
    """
    opt(i) = the longest rising trend ending at i
    init opt(i) = -inf, opt(1) = 1
    max {empty set} = -inf

    opt(i) = max_{r_1 <= r_k < r_i} opt(k) + 1
    """

    opt = [-math.inf] * len(arr)
    opt[0] = 1

    for i in range(1, len(arr)):
        m = -math.inf
        for k in range(i):
            if arr[0] <= arr[k] < arr[i]:
                m = max(m, opt[k] + 1)
        opt[i] = m
    return max(opt)

arr = [10, 120, 11, 12, 13, 11, 10, 15, 19]
sol = rt(arr)
print(sol)