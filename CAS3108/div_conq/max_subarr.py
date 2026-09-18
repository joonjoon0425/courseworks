"""
Problem: Given an integer sequence, find the maximum sum of contiguous subsequences.
Empty subsequence is possible, and the sum is 0.
"""

def qubic_solution(arr):
    """
    naive solution
    time complexity: O(n^3)
    """
    sol = 0
    n = len(arr)
    for i in range(n):
        for j in range(i, n):
            summation = 0
            for k in range(i, j + 1):
                summation += arr[k]
            if sol < summation:
                sol = summation

    return sol

def quadratic_solution(arr):
    """
    slightly modified solution
    saves the summations of other cases
    time complexity: O(n^2)
    """
    sol = 0
    n = len(arr)
    for i in range(n):
        summation = 0
        for j in range(i, n):
            summation += arr[j]
            if sol < summation:
                sol = summation

    return sol

def div_conquer_solution(arr):
    """
    divide-and-conquer solution
    divide the array in half and get the solution for left half, right half, and the summation of array which contains the midpoint
    then, compare three candidates
    time complexity: O(nlogn)
    """
    if len(arr) == 0:
        return 0
    elif len(arr) == 1:
        if arr[0] < 0:
            return 0
        else:
            return arr[0]
    else:
        m = len(arr) // 2
        sol1 = div_conquer_solution(arr[:m])
        sol2 = div_conquer_solution(arr[m:])

        sol3_left = 0
        sol3_right = 0

        summation = 0
        for i in reversed(range(m)):
            summation += arr[i]
            if sol3_left < summation:
                sol3_left = summation
        summation = 0
        for j in range(m, len(arr)):
            summation += arr[j]
            if sol3_right < summation:
                sol3_right = summation

        sol3 = sol3_left + sol3_right

        sol = sol1
        if sol < sol2:
            sol = sol2
        if sol < sol3:
            sol = sol3

        return sol

def linear_solution(arr):
    """
    linear-time O(n) solution
    """
    if len(arr) == 0:
        return 0
    sol = [0 for _ in range(len(arr))]
    sol[0] = max(arr[0], 0)
    for index in range(1, len(arr)):
        if sol[index - 1] + arr[index] < 0:
            sol[index] = 0
        else:
            sol[index] = sol[index - 1] + arr[index]
    return max(sol)

def main():
    test_cases = [
        [5, -1, -1, 5],            # 좌측 접두사/접미사 혼동 -> 잘못하면 9 (정답 8)
        [3, 1, 1, 4],              # elif 버그: sol2 > sol1일 때 sol3 무시 -> 5 (정답 9)
        [5, -100, 3],              # n^2에서 검사 위치가 밖이면 3 (정답 5)
        [1, 2, -100, 3],           # 위와 짝. 우연히 맞는 케이스 (정답 3)
        [-2, 1, -3, 4, -1, 2, 1, -5, 4],  # 교과서 표준 예제 (정답 6, [4,-1,2,1])
        [-3, -1, -7, -2],          # 전부 음수. 빈 구간 허용이면 0, 불허면 -1
        [4],                       # 단일 원소 양수 (정답 4)
        [-9],                      # 단일 원소 음수. 정의 차이가 드러남 (0 또는 -9)
        [2, 3, 1, 4],              # 전부 양수 -> 전체 합 (정답 10)
        [1, -1, 1, -1, 1, -1, 1],  # 부호 교대, 중앙 걸침이 답이 아님 (정답 1)
        [100, -50, -60, 30, -10, 40, 5, 45, -2, 1] # 수업에서 제공해준 예제
    ]

    for arr in test_cases:
        print(f"array: {arr}")
        print(f"{"naive:":<22}{qubic_solution(arr)}")
        print(f"{"n2:":<22}{quadratic_solution(arr)}")
        print(f"{"divide and conquer:":<22}{div_conquer_solution(arr)}")
        print(f"{"linear:":<22}{linear_solution(arr)}")

if __name__ == "__main__":
    main()