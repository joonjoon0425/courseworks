import torch
import math
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, utils, transforms
from tqdm import tqdm

from dataclasses import dataclass
from made import MADE
from rnn import MyRNNBlock

# hyperparameters and configurations
DATASET_PATH = "./data"
MODEL_NAME = "rnn"
SAMPLE_PATH = f"./{MODEL_NAME}/sample"
MODEL_PATH = f"./{MODEL_NAME}/model"

@dataclass
class Config:
    seq_len = 28 * 28
    image_size = 28
    device = "cuda" if torch.cuda.is_available() else "cpu"
    batch_size = 64
    epochs = 5
    lr = 1e-3

    # rnn
    d_hidden = 128
    n_layers = 2

def to_binary(img):
    """
    transform given data into binary data
    """
    # scales to [0.0, 1.0]
    x = transforms.ToTensor()(img)
    x = (x > 0.5).long()
    x = x.view(-1) # flatten to [784]
    return x


@torch.no_grad()
def evaluate(model, loader, cfg):
    model.eval()
    total_loss = 0.0
    total_pixels = 0

    for x, _ in tqdm(loader, desc="Evaluating"):
        x = x.float().to(cfg.device, non_blocking=True)

        logits = model.forward(x)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, x)

        total_loss += loss.item() * x.numel()
        total_pixels += x.numel()

    avg_bce = total_loss / total_pixels
    bpd = avg_bce / math.log(2)

    return avg_bce, bpd


def get_dataloader(cfg):
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
        batch_size=cfg.batch_size,
        shuffle=True,
        num_workers=1,
        pin_memory=torch.cuda.is_available(),
    )

    test_loader = DataLoader(
        test_set,
        batch_size=cfg.batch_size,
        shuffle=False,
        num_workers=1,
        pin_memory=torch.cuda.is_available()
    )

    return train_loader, test_loader


def train(model, opt, loader, cfg):
    model.train()
    total_loss = 0.0
    total_pixels = 0
    for x, _ in tqdm(loader, desc="Training"):
        x = x.float().to(cfg.device, non_blocking=True)

        logits = model.forward(x)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, x)

        opt.zero_grad()
        loss.backward()
        opt.step()
        total_loss += loss.item() * x.numel()
        total_pixels += x.numel()
    train_loss = total_loss / total_pixels

    return train_loss

if __name__ == "__main__":
    torch.manual_seed(10)
    cfg = Config()

    if MODEL_NAME == "made":
        model = MADE(cfg)
    elif MODEL_NAME == "rnn":
        model = MyRNNBlock(cfg)
    train_loader, test_loader = get_dataloader(cfg)

    model.to(cfg.device)

    opt = torch.optim.Adam(model.parameters(), lr=cfg.lr)

    initial_bce, initial_bpd = evaluate(model, test_loader, cfg)
    print(f"Before training: test BCE: {initial_bce}, test BPD: {initial_bpd}")
    train_losses = []
    test_bces = [initial_bce]
    test_bpds = [initial_bpd]
    for i in range(cfg.epochs):
        train_loss = train(model, opt, train_loader, cfg)
        test_bce, test_bpd = evaluate(model, test_loader, cfg)

        train_losses.append(train_loss)
        test_bces.append(test_bce)
        test_bpds.append(test_bpd)

        print(
            f"Epoch: {i:02d} | "
            f"train loss: {train_loss:.6f} | "
            f"test BCE: {test_bce:.6f} | "
            f"test BPD: {test_bpd:.4f}"
        )

        
        samples = model.sample(25).cpu()
        utils.save_image(samples, SAMPLE_PATH + f"/epoch_{i}.png", nrow=5, padding=2)

    torch.save(model.state_dict(), MODEL_PATH + f"binary_mnist_{MODEL_NAME}.pt")