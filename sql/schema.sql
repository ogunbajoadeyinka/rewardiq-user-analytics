CREATE SCHEMA IF NOT EXISTS rewardiq;

CREATE TABLE IF NOT EXISTS rewardiq.users (
    user_id BIGINT PRIMARY KEY,
    signup_date DATE NOT NULL,
    acquisition_channel TEXT NOT NULL,
    platform TEXT NOT NULL,
    region TEXT NOT NULL,
    activated_7d BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS rewardiq.events (
    event_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES rewardiq.users(user_id),
    event_ts TIMESTAMP NOT NULL,
    event_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rewardiq.transactions (
    transaction_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES rewardiq.users(user_id),
    transaction_ts TIMESTAMP NOT NULL,
    amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rewardiq.rewards (
    reward_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES rewardiq.users(user_id),
    transaction_id BIGINT REFERENCES rewardiq.transactions(transaction_id),
    reward_ts TIMESTAMP NOT NULL,
    points INTEGER NOT NULL CHECK (points >= 0),
    reward_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rewardiq.campaigns (
    campaign_id BIGINT PRIMARY KEY,
    campaign_name TEXT NOT NULL,
    acquisition_channel TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS rewardiq.experiment_assignments (
    user_id BIGINT NOT NULL REFERENCES rewardiq.users(user_id),
    experiment_id TEXT NOT NULL,
    variant TEXT NOT NULL CHECK (variant IN ('control','treatment')),
    assigned_at TIMESTAMP NOT NULL,
    PRIMARY KEY (user_id, experiment_id)
);

CREATE INDEX IF NOT EXISTS idx_events_user_ts ON rewardiq.events(user_id, event_ts);
CREATE INDEX IF NOT EXISTS idx_txns_user_ts ON rewardiq.transactions(user_id, transaction_ts);
CREATE INDEX IF NOT EXISTS idx_users_signup_channel ON rewardiq.users(signup_date, acquisition_channel);
