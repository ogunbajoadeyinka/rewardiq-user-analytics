"""Load generated RewardIQ source data into PostgreSQL/Supabase.

Credentials are read exclusively from environment variables. Tables are truncated
and reloaded instead of dropped so repeated CI runs do not spend time rebuilding
large relations on the Supabase free tier.
"""
import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, inspect, text
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
    return create_engine(
        url,
        pool_pre_ping=True,
        connect_args={"sslmode": "require", "options": "-c statement_timeout=0"},
    )


def main():
    engine = engine_from_env()
    with engine.begin() as conn:
        conn.execute(text("create schema if not exists rewardiq"))
        # Disable the per-role statement timeout for this controlled CI session.
        conn.execute(text("set local statement_timeout = 0"))

    inspector = inspect(engine)
    existing = set(inspector.get_table_names(schema="rewardiq"))

    for table in TABLES:
        path = DATA_DIR / f"{table}.csv"
        if not path.exists():
            raise FileNotFoundError(path)
        df = pd.read_csv(path)

        if table in existing:
            with engine.begin() as conn:
                conn.execute(text("set local statement_timeout = 0"))
                conn.execute(text(f'TRUNCATE TABLE rewardiq."{table}"'))
            if len(df):
                df.to_sql(
                    table,
                    engine,
                    schema="rewardiq",
                    if_exists="append",
                    index=False,
                    method="multi",
                    chunksize=500,
                )
        else:
            df.to_sql(
                table,
                engine,
                schema="rewardiq",
                if_exists="fail",
                index=False,
                method="multi",
                chunksize=500,
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
