# Complex Arithmetics
# Vector Spaces
...

atan 말고 atan2 함수를 사용하는 게 좋다.
```python
from math import degrees, atan2
a = atan2(y, x)
```
## Vector Overlap
Two unit vectors' inner product -> geometrically the size of projection of one vector onto another vector 

# Hilbert Space
Definition of **Hilbert space**
- vector space with inner product
- complete

# Complex Vector Space
braket notation $`\bra{a}, \ket{b}`$
- bra is a row vector, and a ket is a column vector
- Suppose $`\ket{x} = (a, b)^\top`$. Then, $`\bra{x} = (a^*, b^*)`$
- inner product $`\braket{a|b} = (a^*)^\top b`$
    - properties of inner product
    - Conjugate symmetric: $`\braket{a|b} = (\braket{b|a})^*`$
    - Distributive: $`\braket{a_1 + a_2|b} = \braket{a_1|b} + \braket{a_2|b}`$ and $`\braket{a|b_1 + b_2} = \braket{a|b_1} + \braket{a|b_2}`$
    - Sesqui-linearity: $`\braket{\alpha a|b} = \alpha^* \braket{a|b}`$ and $`\braket{a|\alpha b} = \alpha \braket{a|b}`$
    - Semi-definite: $`\braket{a|a} \geq 0`$ with equality only when $`a=0`$.