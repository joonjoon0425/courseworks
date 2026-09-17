import numpy as np

class FVSBN:
    def __init__(self, dim):
        # w will be a upper-trianguler matrix
        self.w = np.zeros((dim, dim))
        self.b = np.zeros((dim,))
        # why masking the (0, 0) too? -> the bias fills in the place of w_1 
        self.mask = np.triu(np.ones((dim, dim)), k=1)

    def forward(self, data):
        v = data @ self.w + self.b
        return 1. / (1. + np.exp(-v))

    def nll(self, data):
        p = self.forward(data)
        return -(data * np.log(p) + (1 - data) * np.log(1 - p)).sum(axis=1).mean()

    def grad(self, x):
        N = x.shape[0]
        probs = self.forward(x)
        g = (probs - x) / N
        dw = (x.T @ g) * self.mask
        db = g.sum(axis=0)

        return dw, db

    def fit(self, x, epochs=10000, lr=0.05):
        for _ in range(epochs):
            dw, db = self.grad(x)
            self.w -= lr * dw
            self.b -= lr * db
        return self


class MADE:
    def __init__(self, dim, n_hidden):
        pass
    
if __name__ == "__main__":
    a = FVSBN(3)
    data = np.array([
        [1, 0, 0],
        [0, 1, 1],
        [1, 0, 0],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 0],
        [0, 1, 1],
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
        [1, 0, 0],
        [0, 1, 1],
        [1, 0, 0],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 0],
        [0, 1, 1],
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
        [1, 0, 0],
        [0, 1, 1],
        [1, 0, 0],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 0],
        [0, 1, 1],
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
        [1, 1, 1]
    ])
    a.fit(data, epochs=3000, lr=0.5)
    print(a.nll(data))
    print(a.w)
    print(a.b)