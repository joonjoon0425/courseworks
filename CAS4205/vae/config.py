from dataclasses import dataclass

@dataclass
class Config:
    # Choose what to run: "train", "sample", "reconstruct", or "sample_smooth_interpolation".
    mode: str = "sample_smooth_interpolation"

    # Paths
    data_dir: str = "data"
    out_dir: str = "outputs"
    checkpoint: str = "outputs/vae_mnist.pt"
    sample_output: str = "outputs/samples.png"
    reconstruct_output: str = "outputs/reconstructions.png"
    smooth_interpolation_output: str = "outputs/smooth_interpolation_output.png"

    # Training
    epochs: int = 20
    batch_size: int = 128
    lr: float = 1e-3

    # Model
    latent_dim: int = 32
    hidden_dim: int = 512

    # Inference
    num_images: int = 64

    # Hardware
    cpu: bool = True
