import torch
import torch.nn as nn

class MADE(nn.Module):
    def __init__(self, dim):
        self.mask = torch.triu(torch.ones((dim, dim)))
        self.W1 = torch.randn((dim, dim))
        self.b1 = torch.randn((dim,))
        self.W2 = torch.randn((dim, dim))
        self.b2 = torch.randn((dim,))

    def forward(self, X):
        # shifting을 적용한다.
        # shifting 시 x1 추정량은 weight만 고려하면 항상 0이 되는데, 그걸 bias가 채워줌으로써 항상 0이 나오는 걸 방지한다. FVBSN과 같은 논리.
        # X[:, :-1] -> 배치는 그대로, 마지막 원소들만 잘라냄
        # X[:, :1] -> 배치는 그대로, 앞 원소만 유지 (뒤를 다 버림)
        X = torch.cat([torch.zeros_like(X[:, :1]), X[:, :-1]], dim=-1)
        x1 = X @ (self.W1 * self.mask) + self.b1
        print(self.W1 * self.mask)
        x2 = x1 @ (self.W2 * self.mask) + self.b2
        return x2

if __name__ == "__main__":
    torch.manual_seed(10)

    made = MADE(5)
    mock1 = torch.asarray([[1, 2, 3, 4, 5]], dtype=torch.float)
    mock2 = torch.asarray([[1, -9, 3, 4, 5]], dtype=torch.float)
    f1 = made.forward(mock1)
    f2 = made.forward(mock2)
    print(f1)
    print(f2)