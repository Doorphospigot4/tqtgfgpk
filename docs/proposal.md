# TideGuard AI — Competition proposal template

> Fill the placeholders (`[…]`) with team-specific values before submission.

## 1. The problem

Every year, an estimated 8–14 million tonnes of plastic enter the ocean. Coastal communities in East and Southeast Asia — particularly around the Taiwan Strait, where currents converge debris from multiple river basins — bear a disproportionate share. Most cleanups today happen *after* a beach is visibly polluted; the same coastline is cleaned repeatedly with no progress on prediction or prevention.

## 2. The solution — TideGuard AI

TideGuard combines (a) a **Physics-Informed Neural Network** that predicts surface debris concentration 1–14 days in advance with (b) a **community action platform** that turns predictions into cleanups, citizen science and student leadership.

Key innovations:

1. **Physics-informed forecasting** — by embedding the 2D advection-diffusion equation into the loss function, our model needs **far less data** than a pure black-box neural network, and remains physically plausible even where citizen reports are sparse. The model **learns the windage (α), diffusion (K) and beaching (λ) coefficients** directly from data — values that can themselves inform future ocean-physics research.
2. **Closed feedback loop** — citizen reports submitted via the mobile app become training data for the next retraining cycle. The more the community uses TideGuard, the smarter it gets.
3. **Education baked in** — 10 standalone lessons + quizzes + PDF certificates turn casual users into ocean stewards and the platform into a curriculum-ready tool for schools.

## 3. Why now & why us

- **Why now**: 2026 is the midpoint of the UN Decade of Ocean Science. Open data (CMEMS, ERA5, Sentinel-2) is more accessible than ever; PyTorch + open foundation tools mean a teenager with a laptop can build what a research lab needed a decade ago.
- **Why us**: a youth-led team building open-source tools — the people most affected by the next 50 years of ocean health are leading.

## 4. Pilot plan (12 weeks)

| Week | Milestone |
|-----:|-----------|
| 1-2 | Bootstrap monorepo, scaffolding, CI |
| 3-4 | First synthetic-trained PINN; FastAPI + web MVP |
| 5-6 | Pilot launch with [partner school] in [city]; first 100 reports |
| 7-8 | Retrain on real CMEMS + reports; deploy to staging |
| 9-10 | First measured cleanups (target: 200 kg) |
| 11-12 | Public demo + write-up + submission |

## 5. Impact KPIs (12-month targets)

| Metric | Target |
|--------|--------|
| Active citizen reporters | 1,000+ |
| Approved reports | 5,000+ |
| Cleanup events run | 50+ |
| Total mass collected | 5,000+ kg |
| Partner schools | 20+ |
| Lessons completed | 3,000+ |
| Countries served | 3+ |

## 6. Team

- **[Founder name]** — student lead. Built the PINN and the dashboard. [Affiliations.]
- **[Co-founder names]** — research, partnerships, community management.
- **Mentors**: [marine biologist, ML researcher, NGO partner].

## 7. Budget (USD, first 12 months)

| Item | Cost |
|------|------|
| Cloud infrastructure (Fly.io + R2 + Supabase) | $200 |
| Domain + certificates | $50 |
| Pilot cleanup materials (gloves, bags, scales) | $400 |
| Travel to partner schools | $500 |
| **Total ask** | **$1,150** |

We are deliberately frugal; the entire technical stack runs on free or near-free tiers because the model is small and the database is modest.

## 8. Risks & mitigations

| Risk | Mitigation |
|------|-----------|
| Model under-performs in new geographies | Active learning loop; transfer-learning from Taiwan baseline |
| Low citizen engagement | School-led EE module + gamification; partnership-first growth |
| Open data outage (CMEMS / ERA5) | Cache 30 days locally; fallback to persistence baseline |
| Mis-reporting / vandalism | Moderator queue; community flagging |

## 9. References

- Raissi, M., Perdikaris, P. & Karniadakis, G. (2019). *Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations.* Journal of Computational Physics.
- Biermann, L., Clewley, D., Martinez-Vicente, V., Topouzelis, K. (2020). *Finding plastic patches in coastal waters using optical satellite data.* Scientific Reports.
- Copernicus Marine Service (CMEMS). Global Ocean Physics Analysis and Forecast.
- ECMWF ERA5 reanalysis dataset.

— Contact: contact@tideguard.app · GitHub: https://github.com/Doorphospigot4/tqtgfgpk
