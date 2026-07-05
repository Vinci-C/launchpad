# Tech Stack & Setup Guide

## Core Technologies
- **Backend:** Python 3.12, FastAPI
- **Frontend:** React, TypeScript, Next.js
- **Database:** PostgreSQL
- **Infrastructure:** Google Cloud Platform (GCP)

## Local Development Setup
1. **Prerequisites:** Ensure you have `uv` and Docker installed.
2. **Clone the repo:** `git clone https://github.com/acme-corp/core-api`
3. **Environment:** Run `uv venv` and `source .venv/bin/activate`.
4. **Dependencies:** Run `uv pip install -r requirements.txt`.
5. **Database:** Run `docker-compose up -d db` to start the local Postgres instance.

## Deployment
All code is deployed automatically to staging via GitHub Actions when a PR is merged to `main`. Production deployments happen every Tuesday and Thursday at 10 AM.
