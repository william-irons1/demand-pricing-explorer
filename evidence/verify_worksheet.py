"""Independent closed-form audit of the investigation report, saved as reproducible evidence.

This script chooses optima from calculus/monotonicity and evaluates demand
using the stated powers, independently of models.py's optimisation functions.
The app's analytical and numerical outputs are compared only afterwards.
"""
from pathlib import Path
import csv
import json
import math
import sys

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from models import Parameters, analytical_optimum, numerical_optimum

DESTINATION = Path(__file__).resolve().parent
DEFAULTS = dict(p0=10.0, Q0=100.0, e=2.0, c=6.0, F=0.0, price_min=1.0, price_max=15.0)
MODELS = ('linear', 'constant_elasticity')


def independent_result(model, assumptions):
    p0, Q0, e, c, F, lo, hi = (assumptions[name] for name in DEFAULTS)
    if model == 'linear':
        cutoff = p0 * (1 + 1 / e)
        if lo >= cutoff or (c >= cutoff and hi >= cutoff):
            intervals = ((max(lo, cutoff), hi),)
            price = intervals[0][0]
        else:
            price = min(hi, max(lo, (cutoff + c) / 2))
            intervals = ((price, price),)
        quantity = max(0.0, Q0 * (1 + e) - e * Q0 / p0 * price)
    else:
        if c == 0 and e == 1:
            price, intervals = lo, ((lo, hi),)
        else:
            if e <= 1:
                price = hi
            elif c == 0:
                price = lo
            else:
                price = min(hi, max(lo, e * c / (e - 1)))
            intervals = ((price, price),)
        quantity = Q0 * (price / p0) ** (-e)
    boundary = ('multiple' if intervals[0][0] < intervals[0][1] else
                'lower_boundary' if price == lo else
                'upper_boundary' if price == hi else 'interior')
    return dict(price=price, quantity=quantity, revenue=price * quantity,
                variable_cost=c * quantity, total_cost=c * quantity + F,
                contribution=(price - c) * quantity,
                profit=(price - c) * quantity - F,
                optimal_from=intervals[0][0], optimal_to=intervals[0][1],
                boundary=boundary)


def check_against_app(model, assumptions, independently_calculated):
    params = Parameters(**assumptions)
    for solver in (analytical_optimum, numerical_optimum):
        actual = solver(model, params)
        tolerance = 2e-6 if solver is numerical_optimum else 1e-10
        for field in ('price', 'quantity', 'revenue', 'variable_cost', 'total_cost', 'contribution', 'profit'):
            assert math.isclose(getattr(actual, field), independently_calculated[field],
                                rel_tol=tolerance, abs_tol=tolerance), (solver.__name__, model, assumptions, field, actual, independently_calculated)
        for actual_interval, expected_interval in zip(actual.optimal_intervals, ((independently_calculated['optimal_from'], independently_calculated['optimal_to']),)):
            for actual_endpoint, expected_endpoint in zip(actual_interval, expected_interval):
                assert math.isclose(actual_endpoint, expected_endpoint, rel_tol=tolerance, abs_tol=tolerance)
        assert actual.boundary == independently_calculated['boundary']


INVESTIGATIONS = {
    'A_elasticity': [dict(scenario=f'e={e:g}', e=e) for e in (0.5, 1.0, 1.5, 2.0, 3.0)],
    'B_unit_cost': [dict(scenario=f'c={c:g}', c=c) for c in (6.0, 7.0)],
    'C_upper_price': [dict(scenario=f'upper={upper:g}', price_max=upper) for upper in (15.0, 11.0)],
    'D_fixed_cost': [dict(scenario=f'F={F:g}', F=F) for F in (0.0, 50.0)],
    'E_high_cost': [dict(scenario=f'c={c:g};F=50;upper=20', c=c, F=50.0, price_max=20.0) for c in (6.0, 20.0)],
}

all_rows = []
for investigation, scenarios in INVESTIGATIONS.items():
    baseline_assumptions = {**DEFAULTS, **({'F': 50.0, 'price_max': 20.0} if investigation.startswith('E_') else {})}
    baseline_results = {model: independent_result(model, baseline_assumptions) for model in MODELS}
    rows = []
    for scenario in scenarios:
        changes = {key: value for key, value in scenario.items() if key != 'scenario'}
        assumptions = {**DEFAULTS, **changes}
        for model in MODELS:
            expected = independent_result(model, assumptions)
            check_against_app(model, assumptions, expected)
            baseline = baseline_results[model]
            rows.append(dict(investigation=investigation, scenario=scenario['scenario'], model=model,
                             **assumptions, **expected,
                             price_change=expected['price'] - baseline['price'],
                             profit_change=expected['profit'] - baseline['profit']))
    with (DESTINATION / f'{investigation}.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    all_rows.extend(rows)

with (DESTINATION / 'independent_results.json').open('w') as handle:
    json.dump(all_rows, handle, indent=2)
for row in all_rows:
    print(f"{row['investigation']:22} {row['scenario']:24} {row['model']:20} "
          f"p={row['price']:.10f} Q={row['quantity']:.10f} profit={row['profit']:.10f} "
          f"delta_p={row['price_change']:+.10f} delta_profit={row['profit_change']:+.10f} "
          f"set=[{row['optimal_from']:.10f},{row['optimal_to']:.10f}] {row['boundary']}")
print(f'All {len(all_rows)} independent results agree with both app optimisers.')
