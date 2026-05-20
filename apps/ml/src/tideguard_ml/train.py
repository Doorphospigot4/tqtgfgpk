"""Training script for TideGuard PINN.

Usage:
    python -m tideguard_ml.train --synthetic --epochs 1000
    python -m tideguard_ml.train --config configs/pinn_v1.yaml
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import torch

from tideguard_ml.data import SyntheticDataset
from tideguard_ml.pinn import PINN, pde_residual


@dataclass
class TrainConfig:
    epochs: int = 5000
    lr: float = 1e-3
    n_collocation: int = 4096
    n_obs_batch: int = 1024
    w_data: float = 1.0
    w_pde: float = 0.1
    w_bc: float = 1.0
    w_ic: float = 1.0
    device: str = "cpu"


def train(
    model: PINN,
    dataset: SyntheticDataset,
    cfg: TrainConfig,
) -> PINN:
    """Train PINN with combined data + physics loss."""
    device = cfg.device
    model.to(device)
    opt = torch.optim.Adam(model.parameters(), lr=cfg.lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=cfg.epochs)

    for step in range(cfg.epochs):
        opt.zero_grad()

        obs = dataset.sample_obs(cfg.n_obs_batch, device)
        C_pred = model(obs.x, obs.y, obs.t)
        loss_data = ((C_pred - obs.C) ** 2).mean()

        col = dataset.sample_collocation(cfg.n_collocation, device)
        r = pde_residual(model, col.x, col.y, col.t, col.u_o, col.v_o, col.u_w, col.v_w)
        loss_pde = (r**2).mean()

        loss_ic = dataset.ic_loss(model)
        loss_bc = dataset.bc_loss(model)

        loss = cfg.w_data * loss_data + cfg.w_pde * loss_pde + cfg.w_bc * loss_bc + cfg.w_ic * loss_ic
        loss.backward()
        opt.step()
        sched.step()

        if step % 200 == 0:
            print(
                f"step={step:5d}  loss={loss.item():.4f}  "
                f"data={loss_data.item():.4f}  pde={loss_pde.item():.4f}  "
                f"alpha={model.alpha.item():.4f}  K={model.K.item():.1f}  "
                f"lam={model.lam.item():.2e}"
            )

    return model


def main() -> None:
    parser = argparse.ArgumentParser(description="Train TideGuard PINN")
    parser.add_argument("--synthetic", action="store_true", help="Use synthetic Gaussian bump data")
    parser.add_argument("--epochs", type=int, default=2000)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--save", type=str, default="checkpoints/pinn_v1.pt")
    args = parser.parse_args()

    if args.synthetic:
        dataset = SyntheticDataset(n_obs=5000, seed=42)
    else:
        raise NotImplementedError("Real data training requires CMEMS/ERA5 data. Use --synthetic.")

    model = PINN(hidden=128, depth=6, num_freq=8)
    cfg = TrainConfig(epochs=args.epochs, lr=args.lr, device=args.device)

    print(f"Training PINN on {'synthetic' if args.synthetic else 'real'} data...")
    print(f"Config: {cfg}")
    print(f"Model params: {sum(p.numel() for p in model.parameters()):,}")

    model = train(model, dataset, cfg)

    import os

    os.makedirs(os.path.dirname(args.save), exist_ok=True)
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "alpha": model.alpha.item(),
            "K": model.K.item(),
            "lam": model.lam.item(),
        },
        args.save,
    )
    print(f"Model saved to {args.save}")


if __name__ == "__main__":
    main()
