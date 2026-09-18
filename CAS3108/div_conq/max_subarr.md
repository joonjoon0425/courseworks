# How to prove that the algorithms is correct
1. Show that the algorithm produces the right answer when the algorithm terminates.
2. Show that the algorithm always terminates.

For example, the maximum subarray solution (solution with time complexity $`O(n^2)`$), can be proved by showing that the $`\text{sum}_{i,j} = \sum_{k=i}^j a_k`$ when algorithm terminates, and then showing the algorithm always terminates.

# Proof of time complexity of maxmimum subarray solutions
The base calculation is summation here. The length of the array is $n$.
- Naive Solution: $`O(n^3)`$
    - $`\sum_{i=1}^n\sum_{j=i}^n(j-i+1)=\frac{n(n+1)(n+2)}{6}`$
- Modified Solution: $`O(n^2)`$
    - $`\sum_{i=1}^n\sum_{j=i}^n 1=\frac{n(n+1)}{2}`$

# Sketch of proof that there are no algorithms better than O(n)
Suppose there exists. Let $`n`$ be the length of given array. Then there exists a $`0 \leq k \leq n`$ which the algorithm does not accesses.
Now suppose that every maximum subarray has $`a_k`$ as its element. Then, the algorithm would process a wrong answer when $`[a_1, \dots, a_{k-1}, -\infty, a_{k+1}, \dots, a_n]`$ is given.