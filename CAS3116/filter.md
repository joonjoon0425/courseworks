# Noise
- Impulse: only white dots
- Salt and pepper: white + black dots
- Gaussian noise: variations in intensity drawn from gaussian distribution

## Reducing noise
Assumptions:
- Expect pixels to be like their neighbors
- Noise process is independent from pixels to pixels
- Noise process follows an identical pattern (가우시안이면 계속 같은 분포의 가우시안)
Methods
- Moving average: $`\frac{\sum_i^n p_i}{n}`$
- Weighted moving average: $`\frac{\sum_i^n w_i p_i}{\sum_i^n w_i}`$ -> why sum the weights? it amplifies the average if we don't do so

# Image Filtering
Compute a function of local neighborhood at eacg pixel image
- Filter (mask) -> how to combine nearby values
- Elementwise application of filter to image patch

Used at
- Image enhance: denoise, smoothing, resize
- Extract info: texture, edge
- Detect pattern: template matching

## Corrlation Filtering
Non-weighted averaging filter. Window size is $`(2k + 1)(2k + 1)`$.
- $`G[i, j] = \frac{1}{(2k+1)^2}\sum_{u=-k}^k\sum_{v=-k}^kF[i + u, j+ v]`$
- Just a 2D local average
Generalization: weighted averaging filter are allowed;
- $`G[i, j] = \sum_{u=-k}^k\sum_{v=-k}^kH[u,v]F[i + u, j+ v]`$
- This is called **cross-correlation**, denoted as $`G = H \otimes F`$
- 행렬에 음수 row, col이 들어가는데 중심을 (0, 0)으로 잡고 하면 된다. (그냥 표기 관례 정도) 아마 실제 implement 시에는 k + 1을 더하겠지용?
- Why square? -> fairly account the neighbors (actually, the neighbor should be circle, precisely -> Gaussian filter?)

### Gaussian Filtering
Use Gaussian distribution for the filter.
- Removes high-frequency components from the image ('low pass filter')
- Parameters
    - size of the mask
    - the std ($`\sigma`$) -> 작으면 좁은 영역만 고려, 크면 넓은 영역을 고려
    - common convenstion of kernel size: $`2 \text{ceil}(3\sigma) + 1`$

## Convolutional Filtering
Flip the filter in both dimensions
- $`G[i, j] = \sum_{u=-k}^k\sum_{v=-k}^kH[u,v]F[i - u, j - v]`$
- Denoted as $`G = H \star F`$
Some facts
- Convolution and cross corrleation is identical for the Guassian kernel.
- Convolution is commutative, and associative. Efficient for computation in frequency space.
- Cross corrleation is not.

## Properties of Smoothing Filters
- Values positive
- Sum to 1 -> intensity stays same
- Smoothing instensity ctrlb
- 'loss pass filter'

## Sharpening Filter
Subtract the detail = (original - smoothed image) from the original picture. (필터에 음수가 들어가게 되기는 한다 (this is only for smoothin filters) + noise도 강화하게 된다)

## Filters for computing gradients
Slope, gradients -> '경계'를 찾을 수 있는 듯 하다. eg. vertical edges detection filter: $`\begin{bmatrix}1 & 0 & -1 \\ 2 & 0 & -2 \\ 1 & 0 & -1 \end{bmatrix}`$

## Median filter
No numerical kernels: just the sizes. Replace the center value with the median of the values in the box. eg. $`\begin{bmatrix} 10 & 15 & 20 \\ 23 & 90 & 27 \\ 33 & 31 & 30 \end{bmatrix}`$ -> center value changes to 27, since from [10 15 20 23 27 30 31 33 90], 27 is the median.
- Removes spikes: impulse, salt & pepper noise suppression
- Non-linear

## Boundary Issues
Size of the outputs
- full: output size is larger than that of input
- same: same.
What about the values near the egde? Several methods exists
- clip (treat outer additional values as 0) -> zero padding. most commonly used
- wrap around -> take the opposite side of the piture and attach it
- copy edge -> copy edge
- reflect across edge -> put a mirror!