import torch
import torch.nn as nn
import math

from torch.utils.data import DataLoader
from torchvision import datasets, transforms, utils
from tqdm import tqdm

# hyperparameters and configurations
DATASET_PATH = "./data"
SAMPLE_PATH = "./MADE/sample"
MODEL_PATH = "./MADE/model"
BATCH_SIZE = 256
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
EPOCHS = 90
LR = 1e-3

def to_binary(img):
    """
    transform given data into binary data
    """
    # scales to [0.0, 1.0]
    x = transforms.ToTensor()(img)
    x = (x > 0.5).long()
    x = x.view(-1) # flatten to [784]
    return x

class MaskedLinear(nn.Linear):
    def __init__(self, in_features, out_features, mask):
        super().__init__(in_features, out_features)

        self.register_buffer("mask", mask)

    def forward(self, x):
        # torch의 linear는 weight을 transpose 해서 곱한다. 주의할 것!
        return torch.nn.functional.linear(x, self.weight * self.mask, self.bias)

class MADE(nn.Module):
    def __init__(self, dim):
        super().__init__()
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

        inp = torch.zeros(num_samples, 784, device=DEVICE)
        sampled_pixels = torch.zeros(num_samples, 784, device=DEVICE)

        for t in range(784):
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
        return sampled_pixels.view(num_samples, 1, 28, 28)

def train(model, opt, loader):
    model.train()
    total_loss = 0.0
    total_pixels = 0
    for x, _ in tqdm(loader, desc="Training"):
        x = x.float().to(DEVICE, non_blocking=True)

        logits = model.forward(x)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, x)

        opt.zero_grad()
        loss.backward()
        opt.step()
        total_loss += loss.item() * x.numel()
        total_pixels += x.numel()
    train_loss = total_loss / total_pixels

    return train_loss

@torch.no_grad()
def evaluate(model, loader):
    model.eval()
    total_loss = 0.0
    total_pixels = 0

    for x, _ in tqdm(loader, desc="Evaluating"):
        x = x.float().to(DEVICE, non_blocking=True)

        logits = model.forward(x)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, x)

        total_loss += loss.item() * x.numel()
        total_pixels += x.numel()

    avg_bce = total_loss / total_pixels
    bpd = avg_bce / math.log(2)

    return avg_bce, bpd


def get_dataloader():
    train_set = datasets.MNIST(
        root=DATASET_PATH,
        train=True,
        download=True,
        transform=to_binary
    )
    test_set = datasets.MNIST(
        root=DATASET_PATH,
        train=False,
        download=True,
        transform=to_binary
    )

    train_loader = DataLoader(
        train_set,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=1,
        pin_memory=torch.cuda.is_available(),
    )

    test_loader = DataLoader(
        test_set,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=1,
        pin_memory=torch.cuda.is_available()
    )

    return train_loader, test_loader

if __name__ == "__main__":
    torch.manual_seed(10)

    made = MADE(784)
    train_loader, test_loader = get_dataloader()

    made.to(DEVICE)

    opt = torch.optim.Adam(made.parameters(), lr=LR)

    initial_bce, initial_bpd = evaluate(made, test_loader)
    print(f"Before training: test BCE: {initial_bce}, test BPD: {initial_bpd}")
    train_losses = []
    test_bces = [initial_bce]
    test_bpds = [initial_bpd]
    for i in range(EPOCHS):
        train_loss = train(made, opt, train_loader)
        test_bce, test_bpd = evaluate(made, test_loader)

        train_losses.append(train_loss)
        test_bces.append(test_bce)
        test_bpds.append(test_bpd)

        print(
            f"Epoch: {i:02d} | "
            f"train loss: {train_loss:.6f} | "
            f"test BCE: {test_bce:.6f} | "
            f"test BPD: {test_bpd:.4f}"
        )

        if i % 10 == 0:
            samples = made.sample(25).cpu()
            utils.save_image(samples, SAMPLE_PATH + f"/epoch_{i}.png", nrow=5, padding=2)

    torch.save(made.state_dict(), MODEL_PATH + f"binary_mnist_MADE.pt")