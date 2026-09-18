import math, time

N = 8 # there are n + 1 cities: C[0] to C[n]

DIST = [2, 3, 1, 9, 8, 3, 5, 7] # DIST[i] is the distance from C[i] to C[i + 1]
PRICE = [0, 2, 5, 9, 2, 7, 3, 4, 0] # PRICE[i] is the price for C[i]; The first and last must be 0
MAX_DIST = 9

def best_sch_no_memo(n):
    """
    Return the cheapest expense from C_0 to C_n
    Uses only the recursive calls
    """
    if n == 0:
        return 0
    sol = math.inf
    dist = 0
    for i in reversed(range(n)):
        dist += DIST[i]
        if dist <= MAX_DIST:
            sol = min(sol, best_sch_no_memo(i) + PRICE[n])
    return sol

def best_sch_memo(n):
    """
    Return the cheapest expense from C_0 to C_n
    Uses memoization
    """
    def inner(n, memo):
        if n == 0:
            return 0
        if memo[n] != -1:
            return memo[n]
        sol = math.inf
        dist = 0
        for i in reversed(range(n)):
            dist += DIST[i]
            if dist <= MAX_DIST:
                sol = min(sol, inner(i, memo) + PRICE[n])

        memo[n] = sol
        return sol
    
    memo = [-1 for _ in range(n + 1)]
    memo[0] = 0

    return inner(n, memo)

def best_sch_dp(n):
    """
    Return the cheapest expense from C_0 to C_n
    Dynamic Programming
    dp[k] -> cheapest expense from C_0 to C_k
    """
    dp = [math.inf] * (n + 1)
    dp[0] = 0
    for k in range(1, n + 1):
        m = math.inf
        dist = 0
        for i in reversed(range(k)):
            # dist는 C_i부터 C_k까지의 거리 합
            dist += DIST[i]
            if dist <= MAX_DIST:
                m = min(m, dp[i])
        dp[k] = m + PRICE[k]
    return dp[n]


if __name__ == "__main__":
    start = time.perf_counter()
    sol1 = best_sch_no_memo(N)
    no_memo_time = time.perf_counter() - start

    start = time.perf_counter()
    sol2 = best_sch_memo(N)
    memo_time = time.perf_counter() - start

    start = time.perf_counter()
    sol3 = best_sch_dp(N)
    dp_time = time.perf_counter() - start

    print(f"without memoization: {sol1}, {no_memo_time:.6f}s")
    print(f"with memoization:    {sol2}, {memo_time:.6f}s")
    print(f"with DP:             {sol3}, {dp_time:.6f}s")