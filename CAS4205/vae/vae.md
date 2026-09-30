# Autoencoder
- x -> Encoder -> z -> Decoder -> x*, loss = |x-x*|^2
- bottleneck feature
    - latent feature를 추출한다
    - 없으면 그냥 항등함수를 만들면 되기 때문
- encoder만 따로 떼어서 feature extractor로 사용할 수 있음
- decoder로 생성?
    - z를 뽑아야 한다 -> z가 우리가 아는 확률 분포를 가진다고 가정하면? -> 거기서 뽑아서 decoder에 보낸다.
    - $`z \sim \mathcal{N}(0;I)`$를 학습하게 한다 -> 근데 어케하노
    - $`z \sim \mathcal{N}(\mu, \sigma^2)`$에서 $`\mu`$와 $`\sigma`$를 학습 가능하게 한다.
    - encoder -> mu, sigma -> sample -> decoder
        - 이때 sampling 시 그냥 하면 미분이 불가능하기 때문에 reparametrization trick을 사용한다.
        - $`\mu + \varepsilon\sigma`$ where $`\varepsilon \sim \mathcal{N}(0, I)`$
    - $`\mathcal{N}(\mu, \sigma^2)`$가 $`\mathcal{N}(0, I)`$과 비슷해져야 한다.
        - KL divergence를 이용한다
        - 항상 0보다 큰데, Jensen 부등식을 사용해서 증명할 수 있다.
        - latent vector의 각 원소는 독립을 가정 ($`\mathcal{N}(0,I)`$).
    - $`\sigma`$는 보통 $`\exp{l/2}`$처럼 무조건 양수가 나오게 할 수 있다.
        - 덤으로 KL loss 계산 시 log variance가 공짜

# ELBO and Amortized Variational Inference
Latent variable의 확률분포 추론
- example1: biased coin -> 어떤 동전을 던졌는지 알려주지 않는다.
- example2: 두 gaussian이 주어졌고, 어떤 샘플이 주어졌을 때, 샘플이 어느 gaussian에서 나왔을까?
- Harder Example:
    - Given the features, and we have the noisy image.
    - Which combination of the features built the image?.
    - features are all fixed and has bernoulli prior p(z)=0.5
    - The problem is that it is too hard to compute the normalization constant of posterior distribution.
        - We use amortized variational inference here.
        - Choose a simple distribution $`q(z)`$, which will be optimized to resemble $`p(z|x)`$.
        - 여기서 q와 p의 KL divergence $`KL[q(z) \| p(z|x)]`$를 최소화 할 때 나오는 $`\mathbb{E}[\log{p(x|z)p(z) - \log{q(z)}}]`$ ELBO라고 한다.
        