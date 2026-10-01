# Feature
## Problems with pixel rep
- Not invariant to small changes
    - 회전, 이동, 대칭, 빛 등등
- Do not know which information is more important
- Use local features

## Local features
- Usually exploit image gradient -> to focus more on the structure itself
- Feature ~= vector of gradient statistics inside given window
    - 적절한 window size
    - 적절한 window location

- desired properties
    - locality
        - 좁은 구역에서 뽑아낼 수 있어야 하며, 강건성이 있어야 함
    - repeat & flex
        - repeat: literally
        - flex: robustness to geom transform & photometric transform
    - distinctive
        - should be able to distinguish somewhat similar features?
        - minimize the wrong matches
    - compact & efficient

## Interest points
- interest point = keypoint (= features, sometimes)
    - choice of interest point
        - easy to describe
        - less ambiguous
        - unique
    - examples of interest point
        - corner
        - blob
### Corner
- Shifting in any direction gives a big change in intensity.
    - Flat region won't give any change
    - Edge would give only the change in one direction
    - Corner gives change to all direction
- Harris Detector
    - Window-averaged squared change of intensity
    - $`E(u, v)=\sum_{row-k}^{row+k}\sum_{j=col-k}^{col+k}[I(i + u, j+ v)-I(i, j)]^2`$. Here, window size is 2k+1 and the matrix E is called Energy matrix -> window size와 같은.
    - 그냥 주어진 candidate (row, col)에 대해 주변에서 window 흔들어보고 기존 intensity와의 차이를 제곱한 것의 총합.
    - Autocorrelation surface의 근사
    - $`E(u,v)=[u,v]M\begin{bmatrix}u // v\end{bmatrix}`$ where M is image derivative.
    - Measure of corner reponse: R = det M - k (trac M)^2
        - det M = M의 두 eigenvalue 곱
        - trace M = M의 두 eigenvalue 합
        - k는 0.04에서 0.06 사이의 값
    - Non maximum supression window? What is it
### Properties: Invariance and Covariance
- Invariance: f(transformed x) = f(x)
- Convariance: f(transformed x) = transformed f(x)