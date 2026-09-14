# Multivariate Gaussian Distribution
def: $`p(x;\mu,\Sigma) =\frac{1}{(2\pi)^{d/2}}\frac{1}{|\Sigma^{1/2}|}\exp{\left(-\frac{1}{2}(x-\mu)^\top\Sigma^{-1}(x-\mu)\right)}`$

## Unique property of multivariate Gaussian
- cov = 0 guarantees independence of two Gaussian variables
- joint distribution of Gaussian variables are Gaussian.
- conditional distribution is also Guassian.
- marginal distribution is again a Gaussian.

# Gaussian Mixture Model
- $`p(x, z) = p(x|z)p(z)`$
- $`p(x|z=j)=\mathcal{N}(x;\mu_j,\sigma^2_j)`$
- $`p(z)=Cat(\phi)`$ where $`\phi`$ is a probability vector

## Supervised GMM
Closed solution exists.

## GMM (latent variable model)
No closed solution -> EM Algorithm
$`p(x)`$ -> z가 있다고 가정한 후 z에 대해 적분 (marginalize)

MLE of: $`\sum_{i=1}^N\log{\sum_{j=1}^K\phi_jN(x^{(i)};\mu_j,\Sigma_j)}`$
-> $`\phi`$, $`\mu`$, $`\Sigma`$ 에 대해서 미분을 하고 closed from solution을 구할 수가 없다. Unknown paramter들로 해가 나타나기 때문 (구해야 하는 값으로 최적 해를 구해야 하는 순환)

### EM Algorithm: Expectation-Maximization algorithm
SGD를 마음대로 못 쓰는 이유 -> Constraint 때문에 마음대로 사용할 수가 없다 (Covariance Matrix는 PSD, 확률은 0에서 1사이여야 하고...). (Riemannian Optimization...?)

- E Step: latent variable의 posterior distribution을 계산해주고, 각 데이터가 각 클러스터에 속할 확률들을 계산해준다. (soft guess)
- M Step: 계산한 latent variable에 속할 확률들을 이용해서 parameter들을 갱신
반복 적용