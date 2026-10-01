"""
Edit distance

Let {x_1, ..., x_m} and {y_1, ..., y_n} be the sets of input strings.

We say $M subset {1,...,m} times {1,...,n}$ is matching if no item appears more then once in $M$.
((1, 2) after (1, 1) is not allowed)

We say a matching between {1,...,m} and {1,...,n} is an alignment if there are no crossing pairs
-> there must not exist two pairs (i, j) and (u, v) where i < u, j > v.

The cost of an alignment is defined as; gap penalty + mismatch cost 
- gap penalty: for each unmatched position, delta.
- mismatch cost: for each (i, j) in M, if x_i != y_j, alpha_pq where p = x_i, q = y_i.
Both delta and alpha are part of the input parameters.

Problem: Given two strings, find the minumum cost of alignment between two strings.
"""

def edit_distance(str1, str2, delta, alpha):
    """
    for all i >= 1, j >= 1,

    dp[i][j] is the minimum cost of alignment between {x_1,...,x_i} and {y_1,...,y_j}
    if (i, j) in M:
        dp[i][j] = dp[i-1][j-1] + alpha_ij
    elif (i, j) not in M:
        # note that if one of i or j is paired, the other is not paired
        if i participates:
            dp[i][j] = dp[i][j-1] + delta
        elif j participates:
            dp[i][j] = dp[i-1][j] + delta
    """
    dp = [[0 for _ in range(len(str2) + 1)] for _ in range(len(str1) + 1)]

    for i in range(len(str1) + 1):
        dp[i][0] = i * delta
    for j in range(len(str2) + 1):
        dp[0][j] = j * delta

    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            dp[i][j] = min(dp[i-1][j-1] + alpha, dp[i][j-1] + delta, dp[i-1][j] + delta)
    
    return dp[len(str1)][len(str2)]

s1 = "Hello"
s2 = "Hell"

sol = edit_distance(s1, s2, 0.2, 0.1)
print(sol)