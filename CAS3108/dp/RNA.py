"""
Defn: A primary structure B of an RNA molecule is defined by a sequence of n symbols b_1, ..., b_n
where each symbol is one of the four: A, G, C, U. We say B has length n if it consists of n symbols.

Defn: A secondary structure on a primary structure B of length n is S subset {1,...,n} times {1,...,n} satisfying the following conditions:
    1. if (i, j) is in S, then i < j - 4.
    2. if (i,j) is in S, they have to be complementary. -> {b_i, b_j} must be either {A, U} or {C, G}
    3. (matching) no index appears more then once in S
    4. (noncrossing) (i,j), (k,l) in S, we cannot have i < k < j < l.

Problem:
   Given the primary structure B, find the secondary structure that maximizes the number of pairs. 
"""

def complementary(c1, c2):
    if {c1, c2} == {'A', 'U'} or {c1, c2} == {'C', 'G'}:
        return True
    else:
        return False

def RNASecondaryStructure(primary):
    """
    dp[i][j]: length of optimal sec structure of b_i,...,b_j
    dp[i][j] = 
       |- dp[i,j-1]
    max|
       |- max_{i <= k < j - 4 and {b_j, b_k} is complementary} (dp[i][k-1] + dp[k+1][j-1] + 1) 
    """
    primary = ' ' + primary
    n = len(primary)
    dp = [[0] * n for _ in range(n)]
    for row in reversed(range(1, n)):
        for col in range(1, n):
            m = 0
            for k in range(row, col - 4):
                if complementary(primary[col], primary[k]):
                    m = max(m, dp[row][k - 1] + dp[k + 1][col - 1] + 1)
            dp[row][col] = max(dp[row][col - 1], m)
    
    return dp[1][n - 1]

RNA = 'ACCGGUAGU'
sol = RNASecondaryStructure(RNA)
print(sol)