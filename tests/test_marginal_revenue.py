"""Interior MR checks and regressions for the separate stable searches."""

from dataclasses import replace

import pytest

from models import (
    Parameters,
    analytical_optimum,
    demand,
    evaluate,
    mr_mc_check,
    numerical_optimum,
)


@pytest.mark.parametrize("model,price", [("linear", 10.5), ("constant_elasticity", 12.0)])
def test_benchmark_marginal_revenue_equals_six_pounds_per_unit(model, price):
    params = Parameters()
    check = mr_mc_check(model, params)
    assert check["applicable"] is True
    assert check["status"] == "verified"
    assert check["equal"] is True
    assert check["price"] == pytest.approx(price)
    assert check["marginal_revenue"] == pytest.approx(6.0)
    assert check["marginal_cost"] == 6.0
    assert check["difference"] == pytest.approx(0.0, abs=1e-12)

    # Independently vary quantity through nearby prices: MR = change R / change Q.
    delta = 1e-4
    left = evaluate(model, price - delta, params)
    right = evaluate(model, price + delta, params)
    finite_difference = (right["revenue"] - left["revenue"]) / (
        right["quantity"] - left["quantity"])
    assert finite_difference == pytest.approx(6.0, rel=1e-8)


@pytest.mark.parametrize("model", ["linear", "constant_elasticity"])
@pytest.mark.parametrize("params", [
    Parameters(),
    Parameters(p0=20, Q0=350, e=1.5, c=8, F=100, price_max=50),
    Parameters(p0=0.5, Q0=20, e=2, c=0.2, price_min=0.01, price_max=2),
])
def test_separately_searched_interior_price_passes_mr_mc_check(model, params):
    optimum = numerical_optimum(model, params)
    assert optimum.boundary == "interior"
    check = mr_mc_check(model, params, optimum)
    assert check["price"] == optimum.price
    assert check["status"] == "verified"
    assert check["equal"] is True


@pytest.mark.parametrize("model,params,reason", [
    ("linear", Parameters(price_max=8), "boundary"),
    ("linear", Parameters(price_min=11), "boundary"),
    ("constant_elasticity", Parameters(price_max=11), "boundary"),
    ("constant_elasticity", Parameters(price_min=13), "boundary"),
    # A stationary point exactly on a bound is still a constrained boundary.
    ("linear", Parameters(price_max=10.5), "boundary"),
    ("constant_elasticity", Parameters(price_min=12), "boundary"),
    ("constant_elasticity", Parameters(e=0.5), "boundary"),
    ("constant_elasticity", Parameters(e=1), "boundary"),
    ("constant_elasticity", Parameters(c=0), "boundary"),
    ("linear", Parameters(c=20, F=50, price_max=20), "cutoff"),
    ("linear", Parameters(c=15, price_max=15), "cutoff"),
    ("linear", Parameters(price_min=16, price_max=20), "zero-demand"),
    ("constant_elasticity", Parameters(e=1, c=0), "flat"),
])
def test_mr_mc_explains_exceptions_without_a_misleading_pass_fail(model, params, reason):
    check = mr_mc_check(model, params)
    assert check["status"] == "not_applicable"
    assert check["applicable"] is False
    assert check["equal"] is None
    assert check["marginal_revenue"] is None
    assert check["difference"] is None
    assert reason in check["explanation"].lower()


@pytest.mark.parametrize("params", [Parameters(Q0=5e-324), Parameters(Q0=5e-324, c=14)])
def test_mr_mc_check_handles_unresolvable_positive_demand_or_slope_without_crashing(params):
    check = mr_mc_check("linear", params)
    assert check["status"] == "unavailable"
    assert check["equal"] is None
    assert "floating-point precision" in check["explanation"]


def test_mr_mc_check_does_not_silently_replace_an_incorrect_interior_candidate():
    params = Parameters()
    candidate = replace(analytical_optimum("linear", params), price=10.0)
    check = mr_mc_check("linear", params, candidate)
    assert check["price"] == 10.0
    assert check["status"] == "check_failed"
    assert check["applicable"] is True
    assert check["equal"] is False
    assert check["marginal_revenue"] == pytest.approx(5.0)
    assert check["difference"] == pytest.approx(-1.0)


def test_mr_mc_rejects_an_unknown_or_mismatched_model():
    with pytest.raises(ValueError, match="Unknown demand model"):
        mr_mc_check("unknown", Parameters())
    with pytest.raises(ValueError, match="requested demand model"):
        mr_mc_check("linear", Parameters(), analytical_optimum("constant_elasticity", Parameters()))


@pytest.mark.parametrize("model,expected_price,expected_contribution", [
    ("linear", 10.5, 405.0),
    ("constant_elasticity", 12.0, 1250.0 / 3),
])
def test_large_fixed_cost_does_not_hide_the_optimum_from_the_separate_search(
        model, expected_price, expected_contribution):
    params = Parameters(F=1e24)
    optimum = numerical_optimum(model, params)
    # Rounded profit values cannot distinguish these candidates at this scale.
    assert evaluate(model, 10.0, params)["profit"] == optimum.profit
    assert optimum.price == pytest.approx(expected_price, rel=1e-6)
    assert optimum.contribution == pytest.approx(expected_contribution, rel=1e-10)


@pytest.mark.parametrize("Q0,p0,price,expected", [
    (1e-200, 1e100, 1e-100, 1e200),
    (1e200, 1e-100, 1e100, 1e-200),
])
def test_log_domain_demand_avoids_unnecessary_intermediate_power_overflow(Q0, p0, price, expected):
    params = Parameters(Q0=Q0, p0=p0, e=2)
    assert demand("constant_elasticity", price, params) == pytest.approx(expected, rel=2e-12, abs=0)
