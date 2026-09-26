import torch
import math
import torch.nn as nn

class CausalSelfAttention(nn.Module):
    """
    A self-attention layer with lower triangular masks for autoregressive
    """
    def __init__(self, d_model, n_heads):
        super().__init__()
        assert d_model % n_heads == 0, "d_model must be divided by d_head"
        self.d_head = d_model // n_heads
        self.n_heads = n_heads
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, x):
        """
        Compute the attention map and apply mask
        
        First, the Q, K, and V are computed normally
        Considering only one input, we get [T, D = d_model] shape (since we have multiplied square matrices).
        For multi-head, we split D into [H, h_d] for Q, K and V. That is, reshape [T, D] into [T, H, d_h] and transpose to [H, T, d_h].
        Now the part [T, d_h] is the Q, K, V of each heads. Apply matmul [H, T, d_h] (Q) @ [H, d_h, T] (K, transposed) -> [H, T, T] divide by sqrt(d_h)
        Apply mask (fill the values to -1e9, since softmax will compute this value to 0) and then apply softmax about last dimension.
        matmul [H, T, T] (attention map) @ [H, T, d_h] (V) -> [H, T, d_h] (self-attention)
        transpose [T, H, d_h] and reshape [T, D]. Apply W_o [T, D] @ [D, D] -> [T, D]
        """

        H, d_h = self.n_heads, self.d_head
        B, T, D = x.shape

        Q = self.W_q(x).view(B, T, H, d_h).transpose(1, 2) # [B, H, T, d_h]
        K = self.W_k(x).view(B, T, H, d_h).transpose(1, 2) # [B, H, T, d_h]
        V = self.W_v(x).view(B, T, H, d_h).transpose(1, 2) # [B, H, T, d_h]

        scores = (Q @ K.transpose(-1, -2)) / math.sqrt(d_h) # [B, H, T, T]
        mask = torch.tril(torch.ones_like(scores)).to(dtype=torch.bool) # lower triangular must survive
        masked_scores = scores.masked_fill(~mask, -1e9)
        amap = torch.softmax(masked_scores, dim=-1) 
        sa = amap @ V # [B, H, T, T] @ [B, H, T, d_h] = [B, H, T, d_h]
        
        concatanated = sa.transpose(1, 2).reshape(B, T, D) # [B, T, H, d_h] -> [B, T, D]
        # view requires the tensor to be contiguous, reshape does not
        return self.W_o(concatanated) # [B, T, D]

    def step(self, tok_new, cache):
        """
        A KV Cache implementation
        Receives a new token [B, 1, D] cache: None or (K, V) which has shape [B, H, t, d_h]
        """
        H, d_h = self.n_heads, self.d_head
        B, _, D = tok_new.shape

        q = self.W_q(tok_new).view(B, 1, H, d_h).transpose(1, 2) # [B, H, 1, d_h]
        k = self.W_k(tok_new).view(B, 1, H, d_h).transpose(1, 2) # [B, H, 1, d_h]
        v = self.W_v(tok_new).view(B, 1, H, d_h).transpose(1, 2) # [B, H, 1, d_h]

        if cache is None:
            K, V = k, v
        else:
            K, V = cache
            K = torch.cat([K, k], dim=2) # attach to cache [B, H, t + 1, d_h]
            V = torch.cat([V, v], dim=2) # attach to cache [B, H, t + 1, d_h]

        score = q @ K.transpose(-1, -2) / math.sqrt(d_h) # [B, H, 1, t + 1]
        # no mask is required here, since only the current and previous keys are used
        attn_map = torch.softmax(score, dim=-1)
        sa = attn_map @ V # [B, H, 1, d_h]
        concatanated = sa.transpose(1, 2).reshape(B, 1, D) # [B, 1, D]

        return self.W_o(concatanated), (K, V) # [B, 1, D] and cache

class TransformerBlock(nn.Module):
    """
    One decoder block: causal self-attention, then a position-wise MLP, each
    added back to its input (residual connection) with LayerNorm applied to
    the input of the sub-layer (the "pre-LN" arrangement, as in GPT-2):

        x = x + Attn(LN(x))
        x = x + MLP(LN(x)),        MLP(h) = W_2 relu(W_1 h)

    Attention is the only place positions exchange information; the MLP acts
    on every position independently. No dropout.
    """

    def __init__(self, d_model, n_heads):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = CausalSelfAttention(d_model, n_heads)
        self.ln2 = nn.LayerNorm(d_model)
        self.mlp = nn.Sequential(
            nn.Linear(d_model, 4 * d_model), nn.ReLU(), nn.Linear(4 * d_model, d_model),
        )

    def forward(self, x):
        # x: [B, T, D] -> [B, T, D]
        x = x + self.attn(self.ln1(x))
        x = x + self.mlp(self.ln2(x))
        return x

    def step(self, tok_new, cache):
        a, cache = self.attn.step(self.ln1(tok_new), cache)
        tok_new = tok_new + a
        tok_new = tok_new + self.mlp(self.ln2(tok_new))
        return tok_new, cache

class BinaryTransformer(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.D = cfg.transformer_d_model

        self.tok_emb_layer = nn.Linear(1, self.D) # 1차원을 받으므로... D (emb_dim)으로 증폭
        self.pos_emb_layer = nn.Embedding(cfg.seq_len, self.D)

        self.blocks = nn.ModuleList(
            TransformerBlock(self.D, cfg.n_heads)
            for _ in range(cfg.n_blocks)
        )

        self.ln_f = nn.LayerNorm(self.D)
        self.readout = nn.Linear(self.D, 1) # D dim input to 1 dim probability logit

    def forward(self, x):
        # push input one step right
        B, T = x.shape
        x = torch.cat([torch.zeros_like(x[:, :1]), x[:, :-1]], dim=-1) # [B, T]

        pos = torch.arange(T, device=x.device)
        x = self.tok_emb_layer(x.unsqueeze(-1)) + self.pos_emb_layer(pos) # [B, T, D]
        for block in self.blocks:
            x = block.forward(x)
        x = self.ln_f(x) # [B, T, D]
        return self.readout(x).squeeze(-1) # [B, T]

    @torch.no_grad()
    def sample_no_cache(self, n_samples):
        # without KV Cache
        self.eval()

        sampled_pixels = torch.zeros((n_samples, self.cfg.seq_len), device=self.cfg.device) # [n, T]

        for t in range(self.cfg.seq_len):
            logits = self.forward(sampled_pixels[:, : t + 1])
            pixels = torch.bernoulli(torch.sigmoid(logits[:, -1]))
            sampled_pixels[:, t] = pixels
            
        s = self.cfg.image_size
        return sampled_pixels.view(n_samples, 1, s, s)

    @torch.no_grad()
    def sample(self, n_samples):
        # with KV Cache
        self.eval()
        device = self.cfg.device
        sampled_pixels = torch.zeros((n_samples, self.cfg.seq_len), device=device) # [n, T]
        
        caches = [None] * self.cfg.n_blocks
        for t in range(self.cfg.seq_len):
            tok = torch.zeros(n_samples, 1, device=device) if t == 0 else sampled_pixels[:, t-1:t] # [sampled pixels]
            pos = torch.tensor([t], device=device)
            h = self.tok_emb_layer(tok.unsqueeze(-1)) + self.pos_emb_layer(pos) 
            for i, blk in enumerate(self.blocks):
                h, caches[i] = blk.step(h, caches[i])
            h = self.ln_f(h)
            h = self.readout(h).squeeze(-1).squeeze(-1) # [B]
            pixels = torch.bernoulli(torch.sigmoid(h)) # [B]
            sampled_pixels[:, t] = pixels
            
        s = self.cfg.image_size
        return sampled_pixels.view(n_samples, 1, s, s)