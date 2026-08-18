"""Reusable experiment-analysis utilities for RewardIQ."""
from math import ceil
from typing import Dict
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportions_ztest, proportion_effectsize


def required_sample_size(baseline_rate: float, mde_absolute: float,
                         alpha: float = 0.05, power: float = 0.80) -> int:
    """Return required observations per arm for a two-sided proportions test."""
    treatment_rate = baseline_rate + mde_absolute
    effect = abs(proportion_effectsize(baseline_rate, treatment_rate))
    n = NormalIndPower().solve_power(effect_size=effect, alpha=alpha,
                                     power=power, ratio=1.0, alternative='two-sided')
    return ceil(n)


def analyze_binary_experiment(control_successes: int, control_n: int,
                              treatment_successes: int, treatment_n: int,
                              alpha: float = 0.05) -> Dict[str, float | str]:
    """Analyze a binary A/B test and return business-friendly results."""
    if min(control_n, treatment_n) <= 0:
        raise ValueError('Both experiment arms must contain observations.')
    control_rate = control_successes / control_n
    treatment_rate = treatment_successes / treatment_n
    absolute_lift = treatment_rate - control_rate
    relative_lift = absolute_lift / control_rate if control_rate else float('nan')
    z_stat, p_value = proportions_ztest(
        [treatment_successes, control_successes], [treatment_n, control_n]
    )
    decision = 'Launch' if p_value < alpha and absolute_lift > 0 else ('Stop' if p_value < alpha else 'Iterate')
    return {
        'control_rate': control_rate,
        'treatment_rate': treatment_rate,
        'absolute_lift': absolute_lift,
        'relative_lift': relative_lift,
        'z_stat': float(z_stat),
        'p_value': float(p_value),
        'statistically_significant': bool(p_value < alpha),
        'decision': decision,
    }


if __name__ == '__main__':
    print('Required sample per arm:', required_sample_size(0.24, 0.02))
    print(analyze_binary_experiment(1200, 5000, 1350, 5000))
