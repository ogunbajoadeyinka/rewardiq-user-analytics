"""Generate recruiter-facing analytical findings from RewardIQ generated data."""
from pathlib import Path
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent / "experimentation"))
from ab_test import analyze_binary_experiment, required_sample_size

DATA = Path("data/generated")
OUT = Path("data/outputs")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    users = pd.read_csv(DATA / "users.csv", parse_dates=["signup_date"])
    events = pd.read_csv(DATA / "events.csv", parse_dates=["event_ts"])
    txns = pd.read_csv(DATA / "transactions.csv", parse_dates=["transaction_ts"])
    assignments = pd.read_csv(DATA / "experiment_assignments.csv", parse_dates=["assigned_at"])

    users["signup_month"] = users.signup_date.dt.to_period("M").astype(str)
    users["problem_segment"] = (
        users.acquisition_channel.eq("paid_social") & users.platform.eq("android") &
        users.signup_date.ge("2025-07-01")
    )

    opens = events.loc[events.event_name.eq("app_open"), ["user_id", "event_ts"]].copy()
    joined = opens.merge(users[["user_id", "signup_date"]], on="user_id")
    joined["days_since_signup"] = (joined.event_ts.dt.normalize() - joined.signup_date).dt.days
    d30_ids = set(joined.loc[joined.days_since_signup.between(28, 32), "user_id"])
    users["retained_d30"] = users.user_id.isin(d30_ids)

    cohort = users.groupby(["signup_month", "acquisition_channel", "platform"], as_index=False).agg(
        users=("user_id", "size"), activation_rate=("activated_7d", "mean"),
        d30_retention=("retained_d30", "mean")
    )
    cohort.to_csv(OUT / "cohort_retention.csv", index=False)

    h2 = users.signup_date.ge("2025-07-01")
    problem = users.problem_segment
    findings = {
        "users": len(users),
        "overall_activation": users.activated_7d.mean(),
        "problem_activation": users.loc[problem, "activated_7d"].mean(),
        "h2_other_activation": users.loc[h2 & ~problem, "activated_7d"].mean(),
        "problem_d30": users.loc[problem, "retained_d30"].mean(),
        "h2_other_d30": users.loc[h2 & ~problem, "retained_d30"].mean(),
        "transactions": len(txns),
        "gtv": txns.loc[txns.status.eq("completed"), "amount"].sum(),
    }

    exp = assignments.merge(events[["user_id", "event_ts", "event_name"]], on="user_id", how="left")
    exp["in_window"] = (
        exp.event_name.eq("app_open") & exp.event_ts.gt(exp.assigned_at) &
        exp.event_ts.le(exp.assigned_at + pd.Timedelta(days=7))
    )
    outcome = exp.groupby(["user_id", "variant"], as_index=False).agg(returned_7d=("in_window", "max"))
    summary = outcome.groupby("variant").returned_7d.agg(["sum", "count"])
    result = analyze_binary_experiment(
        int(summary.loc["control", "sum"]), int(summary.loc["control", "count"]),
        int(summary.loc["treatment", "sum"]), int(summary.loc["treatment", "count"])
    )
    result["required_sample_per_arm_for_2pp_mde"] = required_sample_size(.24, .02)
    pd.DataFrame([result]).to_csv(OUT / "experiment_summary.csv", index=False)

    with open(OUT / "verified_findings.md", "w", encoding="utf-8") as f:
        f.write("# Verified RewardIQ Findings\n\n")
        f.write("These findings are generated reproducibly from the project dataset.\n\n")
        f.write(f"- Users analyzed: **{findings['users']:,}**.\n")
        f.write(f"- Overall 7-day activation: **{findings['overall_activation']:.1%}**.\n")
        f.write(f"- H2 paid-social Android activation: **{findings['problem_activation']:.1%}**, versus **{findings['h2_other_activation']:.1%}** for other H2 users.\n")
        f.write(f"- H2 paid-social Android D30 retention: **{findings['problem_d30']:.1%}**, versus **{findings['h2_other_d30']:.1%}** for other H2 users.\n")
        f.write(f"- Completed transactions: **{findings['transactions']:,}**; generated transaction value: **${findings['gtv']:,.0f}**.\n")
        f.write(f"- Experiment control return rate: **{result['control_rate']:.1%}**; treatment: **{result['treatment_rate']:.1%}**; relative lift: **{result['relative_lift']:.1%}**; p-value: **{result['p_value']:.4f}**.\n")
        f.write(f"- Experiment decision under the predefined rule: **{result['decision']}**.\n\n")
        f.write("## Recommendation\n\n")
        f.write("Investigate paid-social Android acquisition quality and onboarding friction first. Reallocate or gate spend based on downstream activation/retention, and use controlled lifecycle experiments rather than acquisition volume alone as the success criterion.\n")

    print("Portfolio outputs written to", OUT)


if __name__ == "__main__":
    main()
