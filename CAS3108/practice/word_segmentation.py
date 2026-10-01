import math

"""
Word segmentation 테스트용 quality 함수.

- WORDS에 있는 문자열: 지정한 양수 값 (단어가 길수록 대체로 큼)
- 그 외 모든 문자열: -3 * len(x)  (사전에 없는 블록은 길수록 손해)

TESTS의 각 항목은 (입력 문자열, 기대 최댓값, 기대 분할) 이며,
기대값은 전수 탐색으로 계산했고 최적 분할이 유일함을 확인했다.
"""

WORDS = {
    'a': 1, 'i': 1,
    'me': 3, 'he': 3, 'at': 4, 'ye': 2, 'be': 3,
    'the': 5, 'eat': 5, 'ate': 4, 'tea': 4, 'you': 6, 'hey': 3,
    'meet': 8, 'they': 6, 'even': 5, 'vent': 5, 'thee': 2,
    'eight': 9, 'youth': 9, 'event': 8,
}

def quality(x: str) -> int:
    return WORDS.get(x, -3 * len(x))

TESTS = [
    ("meetateight",   21, ["meet", "at", "eight"]),
    ("theyouthevent", 22, ["the", "youth", "event"]),
    ("eventea",        9, ["even", "tea"]),
    ("xmeetx",         2, ["x", "meet", "x"]),
    ("a",              1, ["a"]),
]       

def best_segmentation(string):
    """
    opt[i]: best segmentation from x_i...x_n
    """
    n = len(string)
    opt = [-1] * (n + 1)
    opt[n] = 0
    next_seg = [-1] * (n + 1)

    for i in reversed(range(n)):
        m = -math.inf
        for k in range(i, n):
            candidate = opt[k + 1] + quality(string[i : k + 1])
            m = max(m, candidate)
            if m == candidate:
                next_seg[i] = k + 1
        opt[i] = m

    i = 0
    r = next_seg[i]
    li = []
    while True:
        if r == -1:
            break
        li.append(string[i:r])
        i = r
        r = next_seg[i]

    return opt[0], li

for test in TESTS:
    string, score, segmentation = test
    opt, li = best_segmentation(string)
    print(f"opt: {opt}, ans: {score}.\nCorrectness: {opt == score}")
    print(f"segmentation: {li}, ans: {segmentation}.\nCorrectness: {li == segmentation}")