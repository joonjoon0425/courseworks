import torch
import torch.nn as nn
import math

from torch.utils.data import DataLoader
from torchvision import datasets, transforms, utils
from tqdm import tqdm

class MaskedLinear(nn.Linear):
    def __init__(self, in_features, out_features, mask):
        super().__init__(in_features, out_features)

        self.register_buffer("mask", mask)

    def forward(self, x):
        # torch의 linear는 weight을 transpose 해서 곱한다. 주의할 것!
        return torch.nn.functional.linear(x, self.weight * self.mask, self.bias)

class MADE(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        dim = cfg.seq_len
        fc1 = MaskedLinear(dim, dim, torch.tril(torch.ones((dim, dim))))
        fc2 = MaskedLinear(dim, dim, torch.tril(torch.ones((dim, dim))))
        fc3 = MaskedLinear(dim, dim, torch.tril(torch.ones((dim, dim))))

        self.net = nn.Sequential(
            fc1,
            nn.ReLU(),
            fc2,
            nn.ReLU(),
            fc3
        )

    def forward(self, X):
        # shifting을 적용한다.
        # shifting 시 x1 추정량은 weight만 고려하면 항상 0이 되는데, 그걸 bias가 채워줌으로써 항상 0이 나오는 걸 방지한다. FVBSN과 같은 논리.
        # X[:, :-1] -> 배치는 그대로, 마지막 원소들만 잘라냄
        # X[:, :1] -> 배치는 그대로, 앞 원소만 유지 (뒤를 다 버림)
        X = torch.cat([torch.zeros_like(X[:, :1]), X[:, :-1]], dim=-1)
        return self.net(X)

    @torch.no_grad()
    def sample(self, num_samples):
        self.eval()

        inp = torch.zeros(num_samples, self.cfg.seq_len, device=self.cfg.device)
        sampled_pixels = torch.zeros(num_samples, self.cfg.seq_len, device=self.cfg.device)

        for t in range(self.cfg.seq_len):
            # sample the pixel using ancestral sampling
            logits = self(inp)
            # get the probability
            # slice할 때 딱 한 원소만 고르면 차원이 사라진다
            # 차원을 유지하려면 [i: i+1] 처럼 쓰면 된다
            probs = torch.sigmoid(logits[:, t])
            # sample the next pixel using the probability
            next_pixel = torch.bernoulli(probs)
            sampled_pixels[:, t] = next_pixel

            inp[:, t] = next_pixel
        # channel이 1인 것을 반영한다
        s = self.cfg.image_size
        return sampled_pixels.view(num_samples, 1, s, s)