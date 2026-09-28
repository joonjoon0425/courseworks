import torch
import torch.nn as nn
from torchvision import datasets, transforms, utils
from tqdm import tqdm
import os
from config import Config

# A simple variational autoencoder implementation
class VAE(nn.Module):
    def __init__(self, input_dim, latent_dim, hidden_dim):
        super().__init__()
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self.hidden_dim = hidden_dim

        self.dense1 = nn.Linear(input_dim, hidden_dim)
        self.dense2 = nn.Linear(hidden_dim, hidden_dim)
        self.mu = nn.Linear(hidden_dim, latent_dim)
        self.log_var = nn.Linear(hidden_dim, latent_dim)

        self.dense3 = nn.Linear(latent_dim, hidden_dim)
        self.dense4 = nn.Linear(hidden_dim, hidden_dim)
        self.dense5 = nn.Linear(hidden_dim, input_dim)

    def encode(self, x):
        x = nn.functional.relu((self.dense1(x)))
        x = nn.functional.relu(self.dense2(x))
        mu = self.mu(x)
        log_var = self.log_var(x)

        return mu, log_var

    def rsample(self, mu, log_var):
        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(mu)

        return mu + eps * std
    
    def decode(self, z):
        z = nn.functional.relu(self.dense3(z))
        z = nn.functional.relu(self.dense4(z))
        z = self.dense5(z)

        return torch.sigmoid(z)

    def forward(self, x):
        mu, log_var = self.encode(x)
        z = self.rsample(mu, log_var)
        x_hat = self.decode(z)

        return x_hat, mu, log_var

def vae_loss(x, recon_x, mu, log_var):
    mse_loss = torch.nn.functional.mse_loss(x, recon_x, reduction="sum")
    kl_loss = 0.5 * torch.sum(mu.pow(2) + log_var.exp() - 1 - log_var)

    return kl_loss + mse_loss, mse_loss, kl_loss

# 이 이후는 교수님께서 제공해주신 코드들이다
def get_loaders(data_dir, batch_size):
    transform = transforms.ToTensor()
    train_set = datasets.MNIST(data_dir, train=True, download=True, transform=transform)
    test_set = datasets.MNIST(data_dir, train=False, download=True, transform=transform)

    train_loader = torch.utils.data.DataLoader(
        train_set, batch_size=batch_size, shuffle=True
    )
    test_loader = torch.utils.data.DataLoader(
        test_set, batch_size=batch_size, shuffle=False
    )
    return train_loader, test_loader

def train(args):
    device = torch.device("cuda" if torch.cuda.is_available() and not args.cpu else "cpu")
    os.makedirs(args.out_dir, exist_ok=True)

    train_loader, test_loader = get_loaders(args.data_dir, args.batch_size)
    model = VAE(28 * 28, args.latent_dim, args.hidden_dim).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    history = []  # per-epoch averages (per image), used for the loss curve

    for epoch in range(1, args.epochs + 1):
        model.train()
        total_loss = total_mse = total_kld = 0.0
        progress_bar = tqdm(train_loader, desc=f"epoch {epoch:02d}/{args.epochs}")

        for x, _ in progress_bar:
            x = x.to(device).view(-1, 28 * 28)

            optimizer.zero_grad()
            recon, mu, logvar = model(x)
            loss, mse, kld = vae_loss(recon, x, mu, logvar)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            total_mse += mse.item()
            total_kld += kld.item()

            batch_size = x.size(0)
            progress_bar.set_postfix(
                loss=f"{loss.item() / batch_size:.2f}",
                recon=f"{mse.item() / batch_size:.2f}",
                kl=f"{kld.item() / batch_size:.2f}",
            )

        n = len(train_loader.dataset)
        history.append(
            {
                "epoch": epoch,
                "loss": total_loss / n,
                "recon": total_mse / n,
                "kl": total_kld / n,
            }
        )
        print(
            f"epoch {epoch:02d} | "
            f"loss {history[-1]['loss']:.2f} | "
            f"recon {history[-1]['recon']:.2f} | "
            f"kl {history[-1]['kl']:.2f}"
        )

        sample(
            model,
            device,
            os.path.join(args.out_dir, f"samples_epoch_{epoch:02d}.png"),
            args.latent_dim,
        )
        reconstruct(
            model,
            test_loader,
            device,
            os.path.join(args.out_dir, f"recon_epoch_{epoch:02d}.png"),
        )

    torch.save(
        {
            "model_state": model.state_dict(),
            "latent_dim": args.latent_dim,
            "hidden_dim": args.hidden_dim,
        },
        os.path.join(args.out_dir, "vae_mnist.pt"),
    )
    print(f"saved checkpoint to {os.path.join(args.out_dir, 'vae_mnist.pt')}")
    print(f"saved loss curve to {os.path.join(args.out_dir, 'loss_curve.png')}")


@torch.no_grad()
def sample(model, device, path, latent_dim, n=64):
    model.eval()
    z = torch.randn(n, latent_dim, device=device)
    images = model.decode(z).view(n, 1, 28, 28).cpu()
    utils.save_image(images, path, nrow=8)


@torch.no_grad()
def reconstruct(model, loader, device, path, n=8):
    model.eval()
    x, _ = next(iter(loader))
    x = x[:n].to(device)
    flat_x = x.view(-1, 28 * 28)
    recon, _, _ = model(flat_x)
    recon = recon.view(n, 1, 28, 28).cpu()

    comparison = torch.cat([x.cpu(), recon])
    utils.save_image(comparison, path, nrow=n)

def load_model(checkpoint_path, device):
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model = VAE(
        28 * 28,
        latent_dim=checkpoint["latent_dim"],
        hidden_dim=checkpoint["hidden_dim"],
    ).to(device)
    model.load_state_dict(checkpoint["model_state"])
    return model, checkpoint["latent_dim"]


def make_parent_dir(filename):
    parent_dir = os.path.dirname(filename)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

def run_sample(args):
    device = torch.device("cuda" if torch.cuda.is_available() and not args.cpu else "cpu")
    model, latent_dim = load_model(args.checkpoint, device)
    sample(model, device, args.sample_output, latent_dim, args.num_images)
    print(f"saved samples to {args.sample_output}")

def run_smooth_interpolation(args):
    device = torch.device("cuda" if torch.cuda.is_available() and not args.cpu else "cpu")
    model, latent_dim = load_model(args.checkpoint, device)

    z1 = torch.randn(1, latent_dim, device=device)
    z2 = torch.randn(1, latent_dim, device=device)

    n = args.num_images
    # Build all n interpolated latents at once: alphas has shape (n, 1) so it
    # broadcasts against the (1, latent_dim) endpoints to give (n, latent_dim).
    alphas = torch.linspace(0, 1, n, device=device).unsqueeze(1)
    z = (1 - alphas) * z1 + alphas * z2

    model.eval()
    with torch.no_grad():
        images = model.decode(z).view(n, 1, 28, 28).cpu()

    utils.save_image(images, args.smooth_interpolation_output, nrow=8)
    print(f"saved smooth interpolation to {args.smooth_interpolation_output}")
    
def run_reconstruct(args):
    device = torch.device("cuda" if torch.cuda.is_available() and not args.cpu else "cpu")
    _, test_loader = get_loaders(args.data_dir, args.batch_size)
    model, _ = load_model(args.checkpoint, device)
    reconstruct(model, test_loader, device, args.reconstruct_output, args.num_images)
    print(f"saved reconstructions to {args.reconstruct_output}")


def main():
    config = Config()
    make_parent_dir(config.sample_output)
    make_parent_dir(config.reconstruct_output)

    if config.mode == "train":
        train(config)
    elif config.mode == "sample":
        run_sample(config)
    elif config.mode == "reconstruct":
        run_reconstruct(config)
    elif config.mode == "sample_smooth_interpolation":
        run_smooth_interpolation(config)
    else:
        raise ValueError("Config.mode must be 'train', 'sample', or 'reconstruct'")


if __name__ == "__main__":
    main()
