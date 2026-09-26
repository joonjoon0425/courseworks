# Curse of Dimensionality
차원이 커지면 커질수록 parameter들 개수가 급격히 많아진다. -> 감당 불가
# Autoregressive Models
Chain rule을 사용해서 차원의 저주를 회피?; $`p(x)=p(x_1)p(x_2|x_1)p(x_3|x_1,x_2)\cdots p(x_d|x_1,\dots, x_{d-1})`$
-> 착각하면 안 되는 게, Chain rule이 모델이 배울 수 있는 구조를 제한하는 게 아니다. 모든 확률 분포는 chain rule로 분해 가능하다.
조건부 확률에 특정 조건이 걸리면 naive한 표현보다 파라미터 개수를 팍 줄일 수 있다. eg. Markov Property

생성에 유리한 이유
- 이전 토큰만 필요로 하므로 이전 토큰만 생성하면 그 다음 토큰을 만들 수 있다. 미래 토큰이 필요하면 미래의 것을 미리 생성해 둬야 한다. 대가는 순차적 샘플링.
- 정확한 liklihood가 보장된다. 항상 분해 가능하기 때문.

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
linear input 말고 one layer neural network를 사용한다. 그런데 parameter 개수가 d^2이 되어버려서 비효율적 -> parameter sharing; 이전 함수의 parameter들을 공유해서 사용한다.

문제점: training을 할 때 (d pixels에 대해) forward를 d번 반복해야 함.

## MADE: Masked Autoencoder for Distribution Estimation
그 문제점을 해결하려고 나온 모델.
i번쨰 hidden unit에는 0부터 i번째 입력까지만 관여한다. 앞이 뒤에 관여 못하게.
Weight mask를 적용한다.

시험 문제에 뭐 dimesion이 뭐냐, shape이 뭐냐 출제할 수 있다고 하심.

## RNN: Recurrent Nerual Network
hidden state를 input에 넣어줘서 과거 상태를 기억
- $`a_t = W_x x_t + W_h h_{t-1}`$
- $`h_t = \tanh(a_t)`$
- $`y_t = W_oh_t`$

### PixelRNN
Hidden state를 직전 입력이 아니라 위 옆으로부터 받아옴 (Raster scanning order)
#### RNN 문제점
- Sequential Generation for training and inference (시간이 오래 걸림)
- hidden state가 이전의 모든 정보를 보존하는게 사실상 어려움
- exploding/vanishing grads
    - hidden unit의 gradient가 W_h의 반복된 곱으로 표현된다.
    - 최대 고윳값이 1보다 작으면 소실, 1보다 크면 폭발

## CNN
### WaveNet
1-D convolution을 여러 개 쌓아 올려서 receptive field를 늘린다
- 선형적으로 늘어난다. -> dilation을 exponential하게 적용해서 팍팍늘림
- autoregressiveness를 보존하기 위해 현재 이전의 값들에만 convolution 적용. (일반 CNN과 다르게.)

### PixelCNN
- Masked convolution을 사용한다.

- (impl detail) Conv1D(C, 1, 1) 는 그냥 linear layer와 같음

## Masked Attention

### KV Cache
key값과 value를 저장해둔다. 반복 계산을 피하는 대신 메모리를 많이 사용. KV Cache의 압축도 여러 방법이 있음.

자세한 건 직접 구현하면서 알아보자.
- 구현해 보았다. KV Cache가 유용한 이유는 샘플링할 때 계속 같은 값을 계산하게 되기 때문이다.
- 이전 토큰들을 넣어서 다음 토큰을 예측하고 그걸 이어붙이는 과정을 반복하는데, 이 이전 토큰들은 변하지 않는다.
- 즉, 이전 토큰들에 대한 K, V가 계속 계산되고, 심지어 query는 이전 query가 필요 없는데도 계속 계산된다.
- 그래서 query는 저장하지 않고, K와 V를 이전 토큰들에 대해 저장해 둔다.
- 이는 masked이기 때문에 가능한 구조이다. masked가 아니라면 token이 추가될 때마다 행렬 값이 바뀐다.