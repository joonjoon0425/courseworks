# = vs =?
x = y
- logical statement
- PROOF에서만 쓰인다?
- Proved with tactics
- THeorem statements에서 쓰임

x =? y
- Boolean expr
- PROGRAM에서 쓰임
- Compute로 계산될 수 있는 것.

# Fixpoint vs Definition
Fixpoint는 recursion 허용. Definition은 허용하지 않는다. Fixpoint가 잘 만들어지려면 strutural recursion rule을 지켜야 한다. (그냥 재귀 잘 정의되야한다는 뜻) -> collatz 추측같은거 넣으면 안 된다

Function들은 모두 terminate 해야 한다. -> 예제로 loop : False by loop := loop이 proof of false라는데 뭔소리인지는 일단 모르겠다.

