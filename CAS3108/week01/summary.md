# How to prove that the algorithms is correct
1. Show that the algorithm produces the right answer when the algorithm terminates.
2. Show that the algorithm always terminates.

For example, the maximum subarray solution (solution with time complexity $O(n^2)$), can be proved by showing that the $\text{sum}_{i,j} = \sum_{i=1}^j a_i$ when algorithm terminates, and then showing the algorithm always terminates.

# Proof of time complexity of maxmimum subarray solutions
The base calculation is summation here. The length of the array is $n$.
- Naive Solution: $O(n^3)$
    - $\sum_{i=1}^n\sum_{j=i}^n(j-i+1)=\frac{n(n+1)(n+2)}{6}$
- Modified Solution: $O(n^2)$
    - $\sum_{i=1}^n\sum_{j=1}^n 1=\frac{n(n+1)}{2}$