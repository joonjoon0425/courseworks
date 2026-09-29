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