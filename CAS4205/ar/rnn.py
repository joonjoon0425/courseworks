import torch
import math
import torch.nn as nn

class MyRNN(nn.Module):
    def __init__(self, d_input, d_hidden):
        super().__init__()
        k = 1.0 / math.sqrt(d_hidden)
        self.d_input = d_input
        self.d_hidden = d_hidden
        self.W_xh = nn.Parameter(torch.empty(d_hidden, d_input).uniform_(-k, k))
        self.W_hh = nn.Parameter(torch.empty(d_hidden, d_hidden).uniform_(-k, k))
        self.b = nn.Parameter(torch.empty(d_hidden).uniform_(-k, k))

    def step(self, x_t, h_prev):
        """
        compute one step of h = tanh(W_xh x_t + W_hh h_prev + b). h_0 = 0
        and return h
        """
        return torch.tanh(x_t @ self.W_xh.T + h_prev @ self.W_hh.T + self.b)

    def forward(self, x):
        # x : [batch size, time step size, input size = 1]
        """
        returns hidden states of each time steps
        """
        B, T, _ = x.shape
        h = x.new_zeros(B, self.d_hidden) # h_0 = [batch size, hidden size] with all elements 0
        hs = []
        for t in range(T):
            h = self.step(x[:, t], h)
            hs.append(h)
        return torch.stack(hs, dim=1) # stack [batch size, hidden size] along dimension = 1, which creates [batch size, time step size, hidden size]

class MyRNNBlock(nn.Module):
    """
    input : [B, time step size]      -> [x_1, x_2, ..., x_n] -> [_, x_1, x_2, ..., x_{n-1}]
    output: [B, time step size]      -> [x_1, x_2, ..., x_n]
    """
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.layers = nn.ModuleList([
            MyRNN(1 if i == 0 else cfg.d_hidden, cfg.d_hidden)
            for i in range(cfg.n_layers)
        ])
        self.d_hidden = cfg.d_hidden
        # compute one single logit
        # [B, time step size, hidden size] -> [B, time step size, 1]
        self.readout = nn.Linear(cfg.d_hidden, 1)

    def forward(self, x):
        # x: [B, time step size]
        x = torch.cat([torch.zeros_like(x[:, :1]), x[:, :-1]], dim=-1)
        h = x.unsqueeze(-1)
        for layer in self.layers:
            h = layer(h)
        return self.readout(h).squeeze(-1)

    @torch.no_grad()
    def sample(self, num_samples):
        self.eval()

        sampled_pixels = torch.zeros((num_samples, self.cfg.seq_len), device=self.cfg.device)
        x_t = torch.zeros((num_samples, 1), device=self.cfg.device)
        # hidden states for each RNN layers
        # note that the output of previous layer becomes the input of current layer
        h = [torch.zeros((num_samples, self.d_hidden), device=self.cfg.device) for _ in self.layers]

        for t in range(self.cfg.seq_len):
            for i, layer in enumerate(self.layers):
                h[i] = layer.step(x_t if i == 0 else h[i - 1], h[i])
            # the output of lasy layer is used
            probs = torch.sigmoid(self.readout(h[-1]).squeeze(-1))
            next_pixel = torch.bernoulli(probs)
            sampled_pixels[:, t] = next_pixel
            x_t = next_pixel.view(num_samples, 1) # becomes the next input
        s = self.cfg.image_size
        return sampled_pixels.view(num_samples, 1, s, s)