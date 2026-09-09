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

## Unsupervised GMM
No closed solution -> EM Algorithm
$`p(x)`$ -> z가 있다고 가정한 후 z에 대해 적분 (marginalize)
