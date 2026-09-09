import math

test_cases = [
    # 1. 가장 단순한 경우
    [(0, 0), (3, 4)],

    # 2. 일반적인 작은 케이스
    [(0, 0), (5, 5), (2, 1), (9, 3), (2, 2)],

    # 3. 가까운 두 점이 명확한 경우
    [(0, 0), (10, 10), (20, 20), (5, 5), (5.1, 5.1)],

    # 4. 음수 좌표 포함
    [(-5, -5), (-1, -1), (-2, -2), (3, 4), (10, 10)],

    # 5. 모든 점의 x좌표가 같음
    [(2, 0), (2, 10), (2, 3), (2, 3.5), (2, 20)],

    # 6. 모든 점의 y좌표가 같음
    [(0, 5), (10, 5), (3, 5), (3.2, 5), (20, 5)],

    # 7. 중복 점
    [(0, 0), (1, 1), (2, 2), (1, 1), (5, 5)],

    # 8. 격자 형태
    [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
        (2, 0), (2, 1), (2, 2),
    ],

    # 9. 가까운 점 쌍이 중앙 분할선을 가로지르는 경우
    [
        (-10, 0),
        (-5, 10),
        (-0.1, 3),
        (0.1, 3.05),
        (5, -5),
        (10, 8),
    ],

    # 10. strip 안에 여러 점이 몰려 있는 경우
    [
        (-0.4, 0),
        (0.4, 0.7),
        (-0.3, 1.4),
        (0.3, 2.1),
        (-0.2, 2.8),
        (0.2, 3.5),
        (-0.1, 4.2),
        (0.1, 4.9),
        (-10, 10),
        (10, 10),
    ],

    # 11. 큰 좌표
    [
        (1_000_000, 1_000_000),
        (2_000_000, 2_000_000),
        (1_000_001, 1_000_001),
        (-1_000_000, -1_000_000),
    ],

    # 12. 실수 좌표
    [
        (0.1, 0.2),
        (1.3, 4.7),
        (0.1001, 0.2001),
        (-2.5, 3.7),
        (10.2, -4.8),
    ],

    # 13. 정렬되지 않은 입력
    [
        (8, 3),
        (-4, 7),
        (100, 100),
        (0, 0),
        (-4.1, 7.1),
        (3, -8),
    ],

    # 14. 여러 쌍이 같은 최소 거리를 가짐
    [
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0),
        (4, 0),
    ],

    # 15. 중앙선 바로 양쪽의 점이 정답
    [
        (-100, 100),
        (-50, -50),
        (-1, 0),
        (1, 0),
        (50, 50),
        (100, -100),
    ],
]

def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def naive(points):
    if len(points) == 2:
        return dist(points[0], points[1])
    if len(points) == 3:
        return min(dist(points[0], points[1]), dist(points[1], points[2]), dist(points[2], points[0]))
    n = len(points) // 2

    sol1 = naive(points[:n])
    sol2 = naive(points[n:])

    # find two points: one from left, one from right with smallest dist
    sol3 = math.inf
    for p1 in points[:n]:
        for p2 in points[n:]:
            d = dist(p1, p2)
            if sol3 > d:
                sol3 = d
    return min(sol1, sol2, sol3)

def divide_conquer(points):
    def recursion(sorted_points):
        # base cases
        if len(sorted_points) == 2:
            return dist(sorted_points[0], sorted_points[1])
        if len(sorted_points) == 3:
            return min(dist(sorted_points[0], sorted_points[1]), dist(sorted_points[1], sorted_points[2]), dist(sorted_points[2], sorted_points[0]))

        n = len(sorted_points) // 2
        # find solutions from left and right subsets
        l = sorted_points[:n]
        r = sorted_points[n:]
        delta0 = recursion(l)
        delta1 = recursion(r)
        # now we examine the strip (x - delta, x + delta)
        delta = min(delta0, delta1)
        x = l[-1][0]
        strip = []
        for point in sorted_points:
            if x - delta < point[0] < x + delta:
                strip.append(point)
        # sort about y coordinates
        strip = sorted(strip, key=lambda z: z[1])

        sol = math.inf
        for i in range(len(strip)):
            k = 12 if i + 11 < len(strip) else len(strip) - i
            for j in range(1, k):
               if sol > dist(strip[i], strip[i + j]):
                   sol = dist(strip[i], strip[i + j])
        
        return min(delta, sol)

    # sort about x coordinates
    sorted_points = sorted(points, key=lambda p: p[0])
    return recursion(sorted_points)
    

if __name__ == "__main__":
    for test_case in test_cases:
        sol1 = naive(test_case)
        sol2 = divide_conquer(test_case)
        print(f"naive: {str(sol1):<25} div_conq: {str(sol2):<25} equals: {sol1 == sol2}")

