"""Independent checks for matched demand and bounded operating-price choices.

Expected benchmark values and optimal sets below are independently checkable.
Finite differences verify derivatives; SciPy checks optima without a coarse grid.
"""

from dataclasses import replace
import math

import pytest

from models import (
    Parameters,
    analytical_optimum,
    demand,
    elasticity,
    evaluate,
    numerical_optimum,
    sensitivity_rows,
    slope,
    unconstrained_summary,
    zero_demand_price,
)


MODELS = ("linear", "constant_elasticity")


def assert_intervals_equal(actual, expected):
    """Compare finite interval endpoints without rounding model calculations."""
    assert len(actual) == len(expected)
    for interval, expected_interval in zip(actual, expected):
        assert interval == pytest.approx(expected_interval, rel=1e-8, abs=1e-8)


def belongs_to_optimal_set(price, intervals):
    tolerance = 1e-6 * max(1.0, abs(price))
    return any(lo - tolerance <= price <= hi + tolerance for lo, hi in intervals)


@pytest.mark.parametrize("model", MODELS)
@pytest.mark.parametrize(
    "params",
    [
        Parameters(),
        Parameters(p0=4.0, Q0=250.0, e=0.5, c=0.0),
        Parameters(p0=18.0, Q0=40.0, e=1.0, c=7.0),
        Parameters(p0=18.0, Q0=40.0, e=3.0, c=7.0),
    ],
)
def test_reference_quantity_slope_and_elasticity_match(model, params):
    assert demand(model, params.p0, params) == pytest.approx(params.Q0)
    expected_slope = -params.e * params.Q0 / params.p0
    assert slope(model, params.p0, params) == pytest.approx(expected_slope)
    assert elasticity(model, params.p0, params) == pytest.approx(params.e)

    # This calculation uses demand values rather than the derivative function.
    step = params.p0 * 1e-5
    finite_difference = (
        demand(model, params.p0 + step, params)
        - demand(model, params.p0 - step, params)
    ) / (2.0 * step)
    assert finite_difference == pytest.approx(expected_slope, rel=1e-7)
    independently_checked_elasticity = -params.p0 * finite_difference / params.Q0
    assert independently_checked_elasticity == pytest.approx(params.e, rel=1e-7)


def test_linear_elasticity_changes_away_from_reference():
    params = Parameters()
    assert elasticity("linear", 8.0, params) == pytest.approx(8.0 / 7.0)
    assert elasticity("linear", 12.0, params) == pytest.approx(4.0)
    for price in (8.0, 12.0):
        assert elasticity("constant_elasticity", price, params) == pytest.approx(2.0)


@pytest.mark.parametrize("model", MODELS)
def test_reference_financial_results(model):
    assert evaluate(model, 10.0, Parameters(F=50.0)) == pytest.approx(
        {
            "price": 10.0,
            "quantity": 100.0,
            "revenue": 1000.0,
            "variable_cost": 600.0,
            "total_cost": 650.0,
            "contribution": 400.0,
            "profit": 350.0,
        }
    )


def test_benchmark_linear_curve_is_300_minus_20p_until_cutoff():
    params = Parameters()
    for price, quantity in [(5.0, 200.0), (10.0, 100.0), (15.0, 0.0), (20.0, 0.0)]:
        assert demand("linear", price, params) == pytest.approx(quantity)


@pytest.mark.parametrize(
    "model,expected_price,expected_quantity,expected_profit",
    [
        ("linear", 10.5, 90.0, 405.0),
        ("constant_elasticity", 12.0, 625.0 / 9.0, 1250.0 / 3.0),
    ],
)
def test_benchmark_optima(model, expected_price, expected_quantity, expected_profit):
    params = Parameters()
    assert (params.price_min, params.price_max) == (1.0, 15.0)
    result = analytical_optimum(model, params)
    assert result.price == pytest.approx(expected_price)
    assert result.quantity == pytest.approx(expected_quantity)
    assert result.profit == pytest.approx(expected_profit)
    assert result.boundary == "interior"
    assert_intervals_equal(result.optimal_intervals, ((expected_price, expected_price),))
    assert result.revenue - result.total_cost == pytest.approx(result.profit)
    assert result.contribution == pytest.approx(result.profit)

    # The nearby symmetric second difference is negative at this interior maximum.
    step = 0.001
    left = evaluate(model, result.price - step, params)["profit"]
    right = evaluate(model, result.price + step, params)["profit"]
    assert left < result.profit and right < result.profit
    assert (right - left) / (2.0 * step) == pytest.approx(0.0, abs=1e-5)
    assert (right - 2.0 * result.profit + left) / step**2 < 0.0


# Include elasticities on each side of 1, zero cost, and linear zero-sales plateaux.
OPTIMUM_CASES = [
    Parameters(),
    Parameters(p0=4.0, Q0=30.0, e=0.5, c=0.0, F=10.0),
    Parameters(p0=20.0, Q0=300.0, e=1.0, c=7.0, F=100.0),
    Parameters(p0=10.0, Q0=1.0, e=1.1, c=6.0, F=50.0),
    Parameters(p0=10.0, Q0=100.0, e=8.0, c=6.0),
    Parameters(p0=0.5, Q0=20.0, e=2.0, c=0.2, F=2.0),
    Parameters(p0=100.0, Q0=5.0, e=1.5, c=30.0, F=400.0),
    Parameters(p0=10.0, Q0=100.0, e=2.0, c=15.0, F=50.0),
    Parameters(p0=10.0, Q0=100.0, e=2.0, c=20.0),
    Parameters(p0=12.0, Q0=80.0, e=3.0, c=1.0, F=500.0),
    Parameters(p0=10.0, Q0=100.0, e=1.0, c=0.0),
    Parameters(p0=10.0, Q0=100.0, e=2.0, c=0.0),
]


@pytest.mark.parametrize("model", MODELS)
@pytest.mark.parametrize("params", OPTIMUM_CASES)
@pytest.mark.parametrize(
    "range_factors",
    [(0.1, 3.0), (0.05, 0.35), (1.6, 2.0)],
)
def test_analytical_and_numerical_bounded_optima_agree(model, params, range_factors):
    lo, hi = range_factors
    params = replace(params, price_min=lo * params.p0, price_max=hi * params.p0)
    analytical = analytical_optimum(model, params)
    numerical = numerical_optimum(model, params)
    assert numerical.profit == pytest.approx(analytical.profit, rel=1e-8, abs=1e-7)
    if all(lo == hi for lo, hi in analytical.optimal_intervals):
        assert numerical.price == pytest.approx(analytical.price, rel=1e-6, abs=1e-7)
    else:
        assert belongs_to_optimal_set(numerical.price, analytical.optimal_intervals)
    for result in (analytical, numerical):
        assert params.price_min <= result.price <= params.price_max
        assert result.quantity >= 0.0
        assert result.optimal_intervals
        for lo, hi in result.optimal_intervals:
            assert params.price_min <= lo <= hi <= params.price_max
            assert math.isfinite(lo) and math.isfinite(hi)

    # Boundary and stationary-point reasoning is checked separately below.
    # These nearby values additionally catch selecting a stationary minimum.
    for price in (analytical.price * 0.99, analytical.price * 1.01):
        if params.price_min <= price <= params.price_max:
            assert evaluate(model, price, params)["profit"] <= analytical.profit + 1e-8


@pytest.mark.parametrize(
    "model,lower,upper,expected_price,expected_boundary",
    [
        ("linear", 1.0, 11.0, 10.5, "interior"),
        ("constant_elasticity", 1.0, 11.0, 11.0, "upper_boundary"),
        ("linear", 11.0, 15.0, 11.0, "lower_boundary"),
        ("constant_elasticity", 11.0, 15.0, 12.0, "interior"),
        ("linear", 13.0, 14.0, 13.0, "lower_boundary"),
        ("constant_elasticity", 13.0, 14.0, 13.0, "lower_boundary"),
        ("linear", 1.0, 5.0, 5.0, "upper_boundary"),
        ("constant_elasticity", 1.0, 5.0, 5.0, "upper_boundary"),
        ("linear", 10.5, 15.0, 10.5, "lower_boundary"),
        ("linear", 1.0, 10.5, 10.5, "upper_boundary"),
        ("constant_elasticity", 12.0, 15.0, 12.0, "lower_boundary"),
        ("constant_elasticity", 1.0, 12.0, 12.0, "upper_boundary"),
    ],
)
def test_shared_permitted_boundaries(model, lower, upper, expected_price, expected_boundary):
    params = Parameters(price_min=lower, price_max=upper)
    result = analytical_optimum(model, params)
    assert result.price == pytest.approx(expected_price)
    assert result.boundary == expected_boundary
    assert_intervals_equal(result.optimal_intervals, ((expected_price, expected_price),))


def test_linear_cutoff_is_clipped_consistently_in_demand_cost_and_profit():
    params = Parameters(F=50.0)
    cutoff = zero_demand_price(params)
    assert cutoff == pytest.approx(15.0)
    for price in (cutoff, cutoff + 0.01, 2.0 * cutoff):
        result = evaluate("linear", price, params)
        assert demand("linear", price, params) == 0.0
        assert result["quantity"] == 0.0
        assert result["revenue"] == 0.0
        assert result["variable_cost"] == 0.0
        assert result["total_cost"] == 50.0
        assert result["profit"] == -50.0
        with pytest.raises(ValueError):
            elasticity("linear", price, params)
    with pytest.raises(ValueError):
        slope("linear", cutoff, params)
    assert slope("linear", cutoff + 1.0, params) == 0.0
    for fraction in (0.01, 0.25, 0.5, 0.75, 0.99, 1.0, 1.5, 3.0):
        assert demand("linear", fraction * cutoff, params) >= 0.0


@pytest.mark.parametrize(
    "cost,lower,upper,optimal_set,expected_boundary",
    [
        (15.0, 1.0, 25.0, ((15.0, 25.0),), "multiple"),
        (20.0, 1.0, 25.0, ((15.0, 25.0),), "multiple"),
        (6.0, 16.0, 25.0, ((16.0, 25.0),), "multiple"),
        (20.0, 16.0, 25.0, ((16.0, 25.0),), "multiple"),
        (15.0, 1.0, 15.0, ((15.0, 15.0),), "upper_boundary"),
    ],
)
def test_linear_zero_demand_optimal_sets(cost, lower, upper, optimal_set, expected_boundary):
    params = Parameters(c=cost, F=50.0, price_min=lower, price_max=upper)
    result = analytical_optimum("linear", params)
    assert result.price == optimal_set[0][0]
    assert result.profit == -50.0
    assert result.contribution == 0.0
    assert result.quantity == 0.0
    assert result.boundary == expected_boundary
    assert result.warning
    assert_intervals_equal(result.optimal_intervals, optimal_set)
    for lo, hi in optimal_set:
        for price in (lo, (lo + hi) / 2.0, hi):
            assert evaluate("linear", price, params)["profit"] == result.profit


def test_positive_linear_contribution_beats_the_zero_demand_plateau():
    result = analytical_optimum("linear", Parameters(F=50.0, price_max=25.0))
    assert result.price == 10.5
    assert result.profit == pytest.approx(355.0)
    assert_intervals_equal(result.optimal_intervals, ((10.5, 10.5),))


@pytest.mark.parametrize("model", MODELS)
def test_upper_boundary_below_unit_cost_can_have_negative_contribution(model):
    params = Parameters(price_max=5.0, F=50.0)
    result = analytical_optimum(model, params)
    assert result.price == 5.0
    assert result.boundary == "upper_boundary"
    assert result.contribution < 0.0
    assert result.profit < -params.F
    assert result.warning


@pytest.mark.parametrize("model", MODELS)
def test_upper_boundary_at_unit_cost_has_zero_contribution(model):
    params = Parameters(price_max=6.0, F=50.0)
    for optimise in (analytical_optimum, numerical_optimum):
        result = optimise(model, params)
        assert result.price == 6.0
        assert result.contribution == 0.0
        assert result.profit == -50.0
        assert result.boundary == "upper_boundary"


def test_upper_boundary_just_below_linear_cutoff():
    params = Parameters(c=20.0, price_max=14.999999)
    for optimise in (analytical_optimum, numerical_optimum):
        result = optimise("linear", params)
        assert result.price == pytest.approx(params.price_max)
        assert result.boundary == "upper_boundary"
        assert result.quantity > 0.0
        assert result.contribution < 0.0


@pytest.mark.parametrize(
    "elasticity_value,cost,expected_price,expected_boundary,optimal_set",
    [
        (0.5, 0.0, 15.0, "upper_boundary", ((15.0, 15.0),)),
        (0.5, 6.0, 15.0, "upper_boundary", ((15.0, 15.0),)),
        (1.0, 6.0, 15.0, "upper_boundary", ((15.0, 15.0),)),
        (1.0, 0.0, 1.0, "multiple", ((1.0, 15.0),)),
        (2.0, 0.0, 1.0, "lower_boundary", ((1.0, 1.0),)),
        (2.0, 6.0, 12.0, "interior", ((12.0, 12.0),)),
    ],
)
def test_constant_elasticity_regimes_are_not_blindly_using_stationary_formula(
    elasticity_value, cost, expected_price, expected_boundary, optimal_set
):
    params = Parameters(e=elasticity_value, c=cost)
    result = analytical_optimum("constant_elasticity", params)
    assert result.price == expected_price
    assert result.boundary == expected_boundary
    assert_intervals_equal(result.optimal_intervals, optimal_set)
    if elasticity_value == 1.0 and cost == 0.0:
        assert result.profit == pytest.approx(1000.0)
        for price in (1.0, 6.0, 10.0, 15.0):
            assert evaluate("constant_elasticity", price, params)["profit"] == pytest.approx(1000.0)


@pytest.mark.parametrize(
    "elasticity_value,cost,expected_status,expected_price",
    [
        (0.5, 0.0, "no_finite_maximum", None),
        (0.5, 6.0, "no_finite_maximum", None),
        (1.0, 6.0, "no_finite_maximum", None),
        (1.0, 0.0, "multiple", None),
        (2.0, 0.0, "no_finite_maximum", None),
        (2.0, 6.0, "unique", 12.0),
    ],
)
def test_unconstrained_constant_elasticity_has_distinct_regimes(
    elasticity_value, cost, expected_status, expected_price
):
    params = Parameters(e=elasticity_value, c=cost)
    result = unconstrained_summary("constant_elasticity", params)
    assert result["status"] == expected_status
    assert result["explanation"]
    if expected_status == "unique":
        assert result["price"] == pytest.approx(expected_price)
        assert result["optimal_from"] == pytest.approx(expected_price)
        assert result["optimal_to"] == pytest.approx(expected_price)
    elif expected_status == "no_finite_maximum":
        assert result["price"] is None
        assert result["optimal_from"] is None
        assert result["optimal_to"] is None
    else:
        assert result["price"] is None
        assert result["optimal_from"] == 0.0
        assert result["optimal_to"] == math.inf


@pytest.mark.parametrize("cost", [0.0, 6.0, 15.0, 20.0])
def test_unconstrained_linear_includes_the_zero_sales_plateau(cost):
    params = Parameters(c=cost)
    result = unconstrained_summary("linear", params)
    assert result["explanation"]
    if cost < 15.0:
        expected = (15.0 + cost) / 2.0
        assert result["status"] == "unique"
        assert result["price"] == expected
        assert result["optimal_from"] == expected
        assert result["optimal_to"] == expected
    else:
        assert result["status"] == "multiple"
        assert result["price"] == 15.0
        assert result["optimal_from"] == 15.0
        assert result["optimal_to"] == math.inf


@pytest.mark.parametrize("model", MODELS)
def test_reference_can_be_evaluated_outside_the_permitted_interval(model):
    params = Parameters(price_max=8.0)
    # The starting assumptions remain defined, even if p0 is infeasible for sale.
    assert evaluate(model, params.p0, params)["quantity"] == pytest.approx(params.Q0)
    assert analytical_optimum(model, params).price <= params.price_max


FIXED_COST_CASES = [
    Parameters(),
    Parameters(price_max=8.0),
    Parameters(price_min=13.0, price_max=14.0),
    Parameters(c=20.0, price_max=25.0),
    Parameters(e=1.0, c=0.0),
    Parameters(e=0.5, c=0.0),
    Parameters(e=2.0, c=0.0),
]


@pytest.mark.parametrize("model", MODELS)
@pytest.mark.parametrize("params", FIXED_COST_CASES)
@pytest.mark.parametrize("fixed_cost", [50.0, 1000000.0])
def test_fixed_cost_leaves_the_entire_optimal_operating_price_set_unchanged(model, params, fixed_cost):
    baseline = analytical_optimum(model, params)
    increased = analytical_optimum(model, replace(params, F=fixed_cost))
    assert increased.price == baseline.price
    assert increased.optimal_intervals == baseline.optimal_intervals
    assert increased.boundary == baseline.boundary
    assert increased.quantity == baseline.quantity
    assert increased.contribution == baseline.contribution
    assert increased.profit == pytest.approx(baseline.profit - fixed_cost)
    assert increased.total_cost == pytest.approx(baseline.total_cost + fixed_cost)


@pytest.mark.parametrize("model", MODELS)
@pytest.mark.parametrize("params", FIXED_COST_CASES)
def test_quantity_scale_changes_quantities_and_contribution_not_optimal_price_sets(model, params):
    params = replace(params, F=50.0)
    baseline = analytical_optimum(model, params)
    scaled = analytical_optimum(model, replace(params, Q0=3.0 * params.Q0))
    assert scaled.price == baseline.price
    assert scaled.optimal_intervals == baseline.optimal_intervals
    for field in ("quantity", "revenue", "variable_cost", "contribution"):
        assert getattr(scaled, field) == pytest.approx(3.0 * getattr(baseline, field))
    assert scaled.profit == pytest.approx(3.0 * (baseline.profit + params.F) - params.F)


@pytest.mark.parametrize(
    "investigation,changed_field,expected_values",
    [
        ("elasticity", "e", {0.5, 1.0, 1.5, 2.0, 3.0}),
        ("unit_cost", "c", {6.0, 7.0}),
        ("fixed_cost", "F", {0.0, 50.0}),
    ],
)
def test_sensitivity_changes_one_assumption_and_recalibrates_from_benchmark(
    investigation, changed_field, expected_values
):
    rows = sensitivity_rows(investigation)
    assert len(rows) == 2 * len(expected_values)
    assert {row["model"] for row in rows} == set(MODELS)
    defaults = {
        "p0": 10.0, "Q0": 100.0, "e": 2.0, "c": 6.0, "F": 0.0,
        "price_min": 1.0, "price_max": 15.0,
    }
    for model in MODELS:
        model_rows = [row for row in rows if row["model"] == model]
        assert {row[changed_field] for row in model_rows} == expected_values
    for row in rows:
        for field, value in defaults.items():
            if field != changed_field:
                assert row[field] == value
        params = Parameters(**{field: row[field] for field in defaults})
        assert demand(row["model"], params.p0, params) == pytest.approx(100.0)
        assert elasticity(row["model"], params.p0, params) == pytest.approx(params.e)
        assert slope(row["model"], params.p0, params) == pytest.approx(-10.0 * params.e)
        baseline_price = 10.5 if row["model"] == "linear" else 12.0
        baseline_profit = 405.0 if row["model"] == "linear" else 1250.0 / 3.0
        assert row["baseline_price"] == pytest.approx(baseline_price)
        assert row["baseline_profit"] == pytest.approx(baseline_profit)
        assert row["price_change"] == pytest.approx(row["price"] - baseline_price)
        assert row["profit_change"] == pytest.approx(row["profit"] - baseline_profit)


@pytest.mark.parametrize(
    "field,invalid",
    [
        ("p0", 0.0), ("p0", -1.0), ("Q0", 0.0), ("Q0", -1.0),
        ("e", 0.0), ("e", -1.0), ("c", -1.0), ("F", -1.0),
        ("price_min", 0.0), ("price_min", -1.0),
        ("price_max", 0.0), ("price_max", -1.0),
    ],
)
def test_invalid_parameter_ranges_raise_clear_error(field, invalid):
    with pytest.raises(ValueError):
        Parameters(**{field: invalid})


@pytest.mark.parametrize("lower,upper", [(1.0, 1.0), (15.0, 1.0), (2.0, 1.0)])
def test_permitted_interval_must_have_positive_width(lower, upper):
    with pytest.raises(ValueError):
        Parameters(price_min=lower, price_max=upper)


@pytest.mark.parametrize("field", ["p0", "Q0", "e", "c", "F", "price_min", "price_max"])
@pytest.mark.parametrize("invalid", [math.nan, math.inf, -math.inf])
def test_nonfinite_parameters_are_rejected(field, invalid):
    with pytest.raises(ValueError):
        Parameters(**{field: invalid})


@pytest.mark.parametrize("model", MODELS)
@pytest.mark.parametrize("invalid", [0.0, -1.0, math.nan, math.inf, -math.inf])
@pytest.mark.parametrize("function", [demand, slope, elasticity, evaluate])
def test_nonpositive_or_nonfinite_prices_are_rejected(model, invalid, function):
    with pytest.raises(ValueError):
        function(model, invalid, Parameters())


@pytest.mark.parametrize(
    "function",
    [demand, slope, elasticity, evaluate, analytical_optimum, numerical_optimum, unconstrained_summary],
)
def test_unknown_model_is_rejected(function):
    with pytest.raises(ValueError):
        if function in (analytical_optimum, numerical_optimum, unconstrained_summary):
            function("unknown", Parameters())
        else:
            function("unknown", 10.0, Parameters())
