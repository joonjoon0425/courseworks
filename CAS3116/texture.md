# Texture
Perception of object, distiguishing objects

## How to detect texture
Use filters look like patterns and consider the magnitude of response.

filter banks to make vector of a responses of each filters

filter scale에 따라 response가 달라진다.
-> 하나의 filter에 대해 여러 개의 scale, orientation을 준비

# Sampling
- subsampling by the factor of 2
    - has aliasing problem
    - Use Nyquist-Shannon Sampling Theorem to choose appropriate sampling frequency
- Anti-aliasing
    - sampling freq >= 2 * max frequency
    - get rid of high frequency -> apply smoothing filter
- Alg for sub sampling by the factor of 2
    - gaussian blur -> sumsample
- Retrieving original image
    - save the (original - blurred) image between smoothing
    