import math, time

CITY_NUM = 25  # C_0부터 C_24까지

DIST = [1] * 24

# 출발지와 목적지는 숙박비 0, 나머지는 모두 1
PRICE = [0] + [1] * 23 + [0]

MAX_DIST = 5


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
    
    memo = [-1 for _ in range(CITY_NUM)]
    memo[0] = 0

    return inner(n, memo)

def best_sch_dp(n):
    """
    Return the cheapest expense from C_0 to C_n
    Uses memoization
    memo[k] -> cheapest expense from C_0 to C_k
    """


if __name__ == "__main__":
    start = time.perf_counter()
    sol1 = best_sch_no_memo(CITY_NUM - 1)
    no_memo_time = time.perf_counter() - start

    start = time.perf_counter()
    sol2 = best_sch_memo(CITY_NUM - 1)
    memo_time = time.perf_counter() - start

    start = time.perf_counter()
    sol3 = best_sch_dp(CITY_NUM - 1)
    dp_time = time.perf_counter() - start

    print(f"without memoization: {sol1}, {no_memo_time:.6f}s")
    print(f"with memoization:    {sol2}, {memo_time:.6f}s")
    print(f"with DP:             {sol3}, {dp_time:.6f}s")