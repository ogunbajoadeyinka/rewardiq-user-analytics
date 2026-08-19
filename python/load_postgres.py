"""Load generated RewardIQ source data into PostgreSQL/Supabase.

Credentials are read exclusively from environment variables.
"""
import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

DATA_DIR = Path("data/generated")
TABLES = [
    "users", "events", "transactions", "rewards", "campaigns",
    "experiment_assignments",
]


def engine_from_env():
    required = ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD"]
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise RuntimeError(f"Missing database environment variables: {', '.join(missing)}")
    url = URL.create(
        "postgresql+psycopg2",
        username=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
        host=os.environ["PGHOST"],
        port=int(os.environ["PGPORT"]),
        database=os.environ["PGDATABASE"],
    )
    return create_engine(url, pool_pre_ping=True, connect_args={"sslmode": "require"})


def main():
    engine = engine_from_env()
    with engine.begin() as conn:
        conn.execute(text("create schema if not exists rewardiq"))

    # Load parents before children. Replace is safe for this reproducible portfolio
    # pipeline because each run rebuilds the complete synthetic source snapshot.
    for table in TABLES:
        path = DATA_DIR / f"{table}.csv"
        if not path.exists():
            raise FileNotFoundError(path)
        df = pd.read_csv(path)
        df.to_sql(
            table,
            engine,
            schema="rewardiq",
            if_exists="replace",
            index=False,
            method="multi",
            chunksize=1000,
        )
        print(f"Loaded rewardiq.{table}: {len(df):,} rows")

    with engine.connect() as conn:
        user_count = conn.execute(text("select count(*) from rewardiq.users")).scalar_one()
        event_count = conn.execute(text("select count(*) from rewardiq.events")).scalar_one()
    if user_count != 50_000 or event_count <= 0:
        raise RuntimeError("Cloud load validation failed")
    print(f"Cloud validation passed: {user_count:,} users, {event_count:,} events")


if __name__ == "__main__":
    main()
