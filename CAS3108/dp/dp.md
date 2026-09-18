# Dynamic Programming
동적 계획법.
1. subproblem으로 나눈다.
    - subproblem은 최적 부분 구조를 가져야 한다. (큰 문제의 최적해가 작은 문제들의 최적해로 이루어질 수 있어야 한다.)
2. subproblem들을 해결해서 최종 정답을 찾는다. subproblem의 답을 기록해 둔 뒤 사용하는 것이 효율성을 높인다. memoization, tabular method 등등