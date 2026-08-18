"""Generate reproducible synthetic product-analytics data for RewardIQ.

RewardIQ is fictional. The generator intentionally creates a retention problem
that can be diagnosed by acquisition channel, platform, activation, and cohort.
"""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
N_USERS = 50_000
OUT = Path("data/generated")


def main():
    rng = np.random.default_rng(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    user_id = np.arange(1, N_USERS + 1)
    signup_date = pd.to_datetime(rng.choice(pd.date_range("2025-01-01", "2025-12-31"), N_USERS))
    channel = rng.choice(["organic", "paid_social", "paid_search", "referral", "partner"], N_USERS,
                         p=[.30, .25, .18, .15, .12])
    platform = rng.choice(["ios", "android", "web"], N_USERS, p=[.43, .47, .10])
    region = rng.choice(["south", "midwest", "west", "northeast"], N_USERS, p=[.32, .25, .24, .19])

    # Intentional business issue: paid-social Android cohorts acquired in H2
    # activate and retain worse despite acquisition volume increasing.
    h2 = signup_date >= pd.Timestamp("2025-07-01")
    problem = (channel == "paid_social") & (platform == "android") & h2
    activation_prob = np.clip(.68 - .20 * problem + .05 * (channel == "referral"), .15, .90)
    activated = rng.random(N_USERS) < activation_prob

    users = pd.DataFrame({
        "user_id": user_id, "signup_date": signup_date, "acquisition_channel": channel,
        "platform": platform, "region": region, "activated_7d": activated
    }).sort_values("user_id")

    event_rows, txn_rows, reward_rows = [], [], []
    txn_id = reward_id = 1
    event_id = 1
    for row in users.itertuples(index=False):
        is_problem = (row.acquisition_channel == "paid_social" and row.platform == "android"
                      and row.signup_date >= pd.Timestamp("2025-07-01"))
        base_return = .72 if row.activated_7d else .38
        if is_problem:
            base_return -= .18
        active_days = [0]
        for d in range(1, 46):
            p = base_return * np.exp(-d / 35)
            if rng.random() < p:
                active_days.append(d)
        for d in active_days:
            ts = row.signup_date + pd.Timedelta(days=d) + pd.Timedelta(hours=int(rng.integers(8, 22)))
            event_rows.append((event_id, row.user_id, ts, "app_open")); event_id += 1
            if d <= 7 and row.activated_7d and rng.random() < .35:
                event_rows.append((event_id, row.user_id, ts + pd.Timedelta(minutes=5), "receipt_scan")); event_id += 1
            if rng.random() < (.16 if row.activated_7d else .06):
                amount = round(float(rng.gamma(2.5, 18)), 2)
                txn_rows.append((txn_id, row.user_id, ts + pd.Timedelta(minutes=12), amount, "completed"))
                if rng.random() < .45:
                    points = int(max(50, amount * 10))
                    reward_rows.append((reward_id, row.user_id, txn_id, ts + pd.Timedelta(minutes=13), points, "earned"))
                    reward_id += 1
                txn_id += 1

    events = pd.DataFrame(event_rows, columns=["event_id", "user_id", "event_ts", "event_name"])
    txns = pd.DataFrame(txn_rows, columns=["transaction_id", "user_id", "transaction_ts", "amount", "status"])
    rewards = pd.DataFrame(reward_rows, columns=["reward_id", "user_id", "transaction_id", "reward_ts", "points", "reward_type"])

    # Marketing campaign dimension
    campaigns = pd.DataFrame([
        [1, "Organic / Direct", "organic", "2025-01-01", "2025-12-31"],
        [2, "Social Growth", "paid_social", "2025-01-01", "2025-12-31"],
        [3, "Search Always-On", "paid_search", "2025-01-01", "2025-12-31"],
        [4, "Member Referral", "referral", "2025-01-01", "2025-12-31"],
        [5, "Partner Rewards", "partner", "2025-01-01", "2025-12-31"],
    ], columns=["campaign_id", "campaign_name", "acquisition_channel", "start_date", "end_date"])

    # Randomized experiment among eligible activated users.
    eligible = users.loc[users.activated_7d, "user_id"].sample(n=min(12000, int(users.activated_7d.sum())), random_state=SEED)
    assignments = pd.DataFrame({"user_id": eligible.values})
    assignments["experiment_id"] = "exp_reward_reminder_001"
    assignments["variant"] = np.where(rng.random(len(assignments)) < .5, "control", "treatment")
    assignments["assigned_at"] = pd.Timestamp("2025-11-01")

    for name, df in {"users": users, "events": events, "transactions": txns, "rewards": rewards,
                     "campaigns": campaigns, "experiment_assignments": assignments}.items():
        df.to_csv(OUT / f"{name}.csv", index=False)

    print(f"Generated {len(users):,} users, {len(events):,} events, {len(txns):,} transactions")


if __name__ == "__main__":
    main()
