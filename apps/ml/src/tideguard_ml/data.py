"""Synthetic and real dataset classes for PINN training."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch


@dataclass
class ObsBatch:
    x: torch.Tensor
    y: torch.Tensor
    t: torch.Tensor
    C: torch.Tensor


@dataclass
class CollocationBatch:
    x: torch.Tensor
    y: torch.Tensor
    t: torch.Tensor
    u_o: torch.Tensor
    v_o: torch.Tensor
    u_w: torch.Tensor
    v_w: torch.Tensor


class SyntheticDataset:
    """Synthetic Gaussian-bump advected by constant current for PINN testing.

    Domain: x in [0, 1], y in [0, 1], t in [0, 1] (normalized).
    Initial condition: Gaussian bump at (0.3, 0.5).
    Ocean current: constant (u=0.2, v=0.1).
    Wind: constant (u_w=1.0, v_w=0.5).
    """

    def __init__(
        self,
        n_obs: int = 2000,
        u_ocean: float = 0.2,
        v_ocean: float = 0.1,
        u_wind: float = 1.0,
        v_wind: float = 0.5,
        alpha_true: float = 0.03,
        K_true: float = 0.005,
        seed: int = 42,
    ):
        rng = np.random.RandomState(seed)
        self.u_ocean = u_ocean
        self.v_ocean = v_ocean
        self.u_wind = u_wind
        self.v_wind = v_wind

        u_eff = u_ocean + alpha_true * u_wind
        v_eff = v_ocean + alpha_true * v_wind

        xs = rng.uniform(0, 1, n_obs).astype(np.float32)
        ys = rng.uniform(0, 1, n_obs).astype(np.float32)
        ts = rng.uniform(0, 1, n_obs).astype(np.float32)

        cx = 0.3 + u_eff * ts
        cy = 0.5 + v_eff * ts
        sigma = 0.05 + 2 * K_true * ts
        C = np.exp(-((xs - cx) ** 2 + (ys - cy) ** 2) / (2 * sigma**2))
        C += rng.normal(0, 0.02, n_obs).astype(np.float32)
        C = np.clip(C, 0, None)

        self._obs_x = torch.tensor(xs)
        self._obs_y = torch.tensor(ys)
        self._obs_t = torch.tensor(ts)
        self._obs_C = torch.tensor(C.astype(np.float32))

    def sample_obs(self, n: int, device: str = "cpu") -> ObsBatch:
        idx = torch.randint(0, len(self._obs_x), (n,))
        return ObsBatch(
            x=self._obs_x[idx].to(device),
            y=self._obs_y[idx].to(device),
            t=self._obs_t[idx].to(device),
            C=self._obs_C[idx].to(device),
        )

    def sample_collocation(self, n: int, device: str = "cpu") -> CollocationBatch:
        x = torch.rand(n, device=device)
        y = torch.rand(n, device=device)
        t = torch.rand(n, device=device)
        return CollocationBatch(
            x=x,
            y=y,
            t=t,
            u_o=torch.full((n,), self.u_ocean, device=device),
            v_o=torch.full((n,), self.v_ocean, device=device),
            u_w=torch.full((n,), self.u_wind, device=device),
            v_w=torch.full((n,), self.v_wind, device=device),
        )

    def ic_loss(self, model: torch.nn.Module) -> torch.Tensor:
        """Initial condition loss: Gaussian bump at t=0."""
        n = 512
        x = torch.rand(n)
        y = torch.rand(n)
        t = torch.zeros(n)
        C_pred = model(x, y, t)
        C_true = torch.exp(-((x - 0.3) ** 2 + (y - 0.5) ** 2) / (2 * 0.05**2))
        return ((C_pred - C_true) ** 2).mean()

    def bc_loss(self, model: torch.nn.Module) -> torch.Tensor:
        """Boundary condition loss: zero flux at domain edges."""
        n = 256
        t = torch.rand(n)

        edges = []
        for _ in range(4):
            edges.append(torch.rand(n // 4))

        x_left = torch.zeros(n // 4)
        x_right = torch.ones(n // 4)
        y_bot = torch.zeros(n // 4)
        y_top = torch.ones(n // 4)

        C_left = model(x_left, edges[0], t[: n // 4])
        C_right = model(x_right, edges[1], t[n // 4 : n // 2])
        C_bot = model(edges[2], y_bot, t[n // 2 : 3 * n // 4])
        C_top = model(edges[3], y_top, t[3 * n // 4 :])

        return (C_left**2 + C_right**2 + C_bot**2 + C_top**2).mean()
