# RewardIQ Execution Runbook

## Quick validation

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python python/generate_data.py
```

Generated CSVs are written to `data/generated/` and are intentionally not committed as source data.

## PostgreSQL

Create a database named `rewardiq`, then run:

```bash
psql -d rewardiq -f sql/schema.sql
```

Load the six generated CSVs into the corresponding tables in the `rewardiq` schema.

## dbt profile

Create `~/.dbt/profiles.yml` locally. Never commit credentials.

```yaml
rewardiq:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: YOUR_POSTGRES_USER
      password: YOUR_POSTGRES_PASSWORD
      port: 5432
      dbname: rewardiq
      schema: dbt
      threads: 4
```

Then run:

```bash
cd dbt
dbt debug
dbt build
```

`dbt build` should create the staging, intermediate, and analytics layers and run the declared tests.

## Experiment smoke test

```bash
python python/experimentation/ab_test.py
```

## Dashboard inputs

Primary dashboard-facing models:

- `mart_kpi_monthly`
- `mart_funnel`
- `mart_user_retention`
- `mart_user_segments`
- `mart_experiment_readout`

Use these modeled assets rather than recreating business logic inside Tableau or Hex.
