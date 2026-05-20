# TideGuard AI

**AI that predicts plastic before it pollutes.**

TideGuard AI is an open-source citizen-science platform that combines:

- A **Physics-Informed Neural Network (PINN)** trained on the 2D advection-diffusion equation to forecast marine debris concentration up to 14 days in advance.
- A **FastAPI** backend serving forecast tiles, citizen reports, cleanups, education and KPI endpoints.
- A **Next.js 14** web dashboard with a MapLibre + raster heatmap, time slider, lessons and leaderboard.
- A **Flutter** mobile companion for photo reporting + lessons offline.
- An **Environmental Education (EE) module** with 10 standalone lessons, quizzes, XP and PDF certificates.

Built for the **Youth Innovation Challenge — Taiwan 2026** (deadline May 31) and **Young Climate Prize NY 2026** (deadline June 30).

## Live structure

```
tideguard/
├── apps/
│   ├── ml/          # PyTorch PINN, training, ingest pipelines
│   ├── api/         # FastAPI + SQLAlchemy + Alembic + PostGIS
│   ├── web/         # Next.js 14 + MapLibre + Tailwind
│   └── mobile/      # Flutter 3 + Riverpod + go_router
├── content/lessons/ # 10 markdown lessons with embedded JSON quizzes
├── infra/           # Docker + docker-compose + fly.toml
├── docs/            # model card, proposal, founder story, architecture
└── .github/workflows/  # CI for each app
```

## Quickstart

### 1. Backend (API)

```bash
cd apps/api
uv venv && uv pip install -e ".[dev]"
uv run pytest -q                       # all tests pass
uv run uvicorn tideguard_api.main:app --reload
# now visit http://localhost:8000/docs
# the dev DB is sqlite and auto-creates the schema
```

Seed the 10 EE lessons:
```bash
curl -X POST http://localhost:8000/education/_seed
```

### 2. ML — train the PINN on synthetic data

```bash
cd apps/ml
uv venv && uv pip install -e ".[dev]"
uv run pytest -q                       # PINN smoke tests
uv run python -m tideguard_ml.train --synthetic --epochs 1000
# saves a checkpoint to checkpoints/pinn_v1.pt
```

### 3. Web (Next.js)

```bash
pnpm install
cd apps/web
pnpm dev
# visit http://localhost:3000
```

### 4. Mobile (Flutter)

```bash
cd apps/mobile
flutter pub get
flutter run
```

### 5. All-in-one via Docker

```bash
cd infra
docker compose -f docker-compose.dev.yml up --build
```

## The science

TideGuard's PINN solves the 2D advection-diffusion equation for surface debris concentration:

```
∂C/∂t + ∇·((u_ocean + α·u_wind) · C) − ∇·(K · ∇C) + λ · C = S(x,y,t)
```

with three **learnable physical parameters**:

- **α** — windage coefficient (≈ 0.03 for bottles; the model fine-tunes per debris type)
- **K** — diffusion coefficient (m²/s)
- **λ** — beaching rate (1/day)

See [docs/model_card.md](docs/model_card.md) for full architecture, metrics and limitations.

## Endpoints

| Method | Path                          | Purpose                              |
|-------:|-------------------------------|--------------------------------------|
| GET    | `/healthz`                    | Health check                         |
| GET    | `/me`                         | Current user profile                 |
| GET    | `/forecast`                   | Predicted concentration grid         |
| GET    | `/tiles/{z}/{x}/{y}.png`      | Raster heatmap tile                  |
| POST   | `/reports`                    | Submit a citizen report (photo+GPS)  |
| GET    | `/reports`                    | List approved reports in bbox        |
| PATCH  | `/reports/{id}`               | Moderator: approve/reject report     |
| POST   | `/cleanups`                   | Log a cleanup event (polygon + kg)   |
| GET    | `/cleanups/stats`             | Aggregate KPIs                       |
| GET    | `/education/lessons`          | List EE lessons                      |
| GET    | `/education/lessons/{slug}`   | Lesson body + quiz                   |
| POST   | `/education/progress`         | Record quiz progress, award XP       |
| GET    | `/education/certificate`      | Generate PDF certificate (≥5 done)   |
| GET    | `/leaderboard`                | Top users by XP                      |
| GET    | `/admin/kpi`                  | Impact dashboard (admin only)        |

## License

- Code: MIT (see [LICENSE](LICENSE))
- Lesson content: CC-BY-4.0

## Acknowledgements

Built independently by a youth-led team for the 2026 climate prize cycle.
PINN methodology inspired by Raissi et al. (2019) and Biermann et al. (2020).
Ocean current data: Copernicus Marine Service (CMEMS). Wind reanalysis: ECMWF ERA5.

— Contact: contact@tideguard.app
