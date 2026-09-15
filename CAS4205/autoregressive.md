# Curse of Dimensionality
차원이 커지면 커질수록 parameter들 개수가 급격히 많아진다. -> 감당 불가
# Autoregressive Models
Chain rule을 사용해서 차원의 저주를 회피?; $`p(x)=p(x_1)p(x_2|x_1)p(x_3|x_1,x_2)\cdots p(x_d|x_1,\dots, x_{d-1})`$  
조건부 확률에 특정 조건이 걸리면 naive한 표현보다 파라미터 개수를 팍 줄일 수 있다. eg. Markov Property

## Fully visible sigmoid belif network
각 conditional distribution을 (sigmoid) 함수로 만들고 그 함수의 paramter를 조정. Slide 참조할 것.
- $`w_1 \in \mathbb{R}^1`$
- $`w_2 \in \mathbb{R}^1`$ and $`b_2 \in \mathbb{R}^1`$
- $`w_3 \in \mathbb{R}^2`$ and $`b_3 \in \mathbb{R}^1`$
- $`w_d \in \mathbb{R}^{d-1}`$ and $`b_d \in \mathbb{R}^1`$

각 함수들의 parameter를 logistic regression으로 최적값 구하기

Sampling할 때 (Ancestral Sampling)
- x_1 샘플링
- 정해진 x_1값을 실제 함수에 넣은 후 x_2 샘플링
- repeat
Sampling이 바로 Generate하는 것.

한계점은 결국 linear model이라는 것

## NADE: Neural Autoregressive Density Estimation
linear input 말고 one layer neural network를 사용한다. 그런데 parameter 개수가 d^2이 되어버려서 비효율적 -> parameter sharing; 이전 함수의 parameter들을 그대로 쓴다.