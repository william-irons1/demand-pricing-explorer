"""Verify completed findings against equations and separate objective searches.

These checks cover the generated investigation records and revenue objective;
the original model verification suite remains unchanged in test_models.py.
"""

from dataclasses import asdict, replace
import math

import pytest
from scipy.optimize import minimize_scalar

from analysis import (
    INVESTIGATION_LABELS, build_investigation, investigation_keys,
    METHODOLOGY, report_markdown, revenue_optimum, summary_markdown,
)
from models import Parameters, analytical_optimum, demand, evaluate, numerical_optimum


MODELS = ("linear", "constant_elasticity")
KEYS = ("elasticity", "unit_cost", "price_cap", "fixed_cost", "high_cost")
FINANCIAL_FIELDS = (
    "price", "quantity", "revenue", "variable_cost", "total_cost", "contribution", "profit",
)


def parameters_of(row):
    return Parameters(**{key: row[key] for key in asdict(Parameters())})


def member(price, intervals):
    return any(lo - 1e-6 <= price <= hi + 1e-6 for lo, hi in intervals)


def row_for(key, model, **conditions):
    return next(row for row in build_investigation(key)["rows"]
                if row["model"] == model
                and all(row[field] == value for field, value in conditions.items()))


def independent_values(model, price, params):
    """Use direct mathematical expressions, without calling model evaluate."""
    if model == "linear":
        quantity = max(0, params.Q0 * (1 + params.e) - params.e * params.Q0 / params.p0 * price)
    else:
        quantity = params.Q0 * (price / params.p0) ** (-params.e)
    return dict(price=price, quantity=quantity, revenue=price * quantity,
                variable_cost=params.c * quantity, total_cost=params.c * quantity + params.F,
                contribution=(price - params.c) * quantity,
                profit=(price - params.c) * quantity - params.F)


def test_all_five_existing_investigations_are_complete():
    assert set(investigation_keys()) == set(KEYS)
    assert set(INVESTIGATION_LABELS) == set(KEYS)
    assert sum(len(build_investigation(key)["rows"]) for key in KEYS) == 26
    for key in KEYS:
        investigation = build_investigation(key)
        assert investigation["key"] == key
        for field in ("title", "question", "changed", "held", "theory", "interpretation",
                      "financial_implications", "conclusion", "limitation"):
            assert investigation[field], (key, field)
        assert investigation["equations"]
        row_keys = {(row["model"], row["scenario"]) for row in investigation["rows"]}
        working_keys = {(work["model"], work["scenario"]) for work in investigation["workings"]}
        assert working_keys == row_keys
        assert all(work["steps"] for work in investigation["workings"])


@pytest.mark.parametrize("key", KEYS)
def test_every_generated_result_agrees_with_direct_equations_and_numerical_search(key):
    for row in build_investigation(key)["rows"]:
        params = parameters_of(row)
        independent = independent_values(row["model"], row["price"], params)
        for field in FINANCIAL_FIELDS:
            assert row[field] == pytest.approx(independent[field], rel=1e-10, abs=1e-8)
            assert math.isfinite(row[field])
        assert params.price_min <= row["price"] <= params.price_max
        assert row["quantity"] >= 0
        numerical = numerical_optimum(row["model"], params)
        assert member(numerical.price, row["optimal_intervals"])
        assert numerical.profit == pytest.approx(row["profit"], rel=1e-8, abs=1e-7)
        for lo, hi in row["optimal_intervals"]:
            assert params.price_min <= lo <= hi <= params.price_max
            for price in (lo, (lo + hi) / 2, hi):
                assert independent_values(row["model"], price, params)["profit"] == pytest.approx(row["profit"])
        for field in ("price", "quantity", "revenue", "profit"):
            assert row[f"{field}_change"] == pytest.approx(row[field] - row[f"baseline_{field}"])


@pytest.mark.parametrize("key,changed,values", [
    ("elasticity", "e", {0.5, 1, 1.5, 2, 3}),
    ("unit_cost", "c", {6, 7}),
    ("price_cap", "price_max", {11, 15}),
    ("fixed_cost", "F", {0, 50}),
    ("high_cost", "c", {6, 20}),
])
def test_investigations_control_every_other_assumption_and_use_correct_baseline(key, changed, values):
    base = Parameters(F=50, price_max=20) if key == "high_cost" else Parameters()
    rows = build_investigation(key)["rows"]
    for model in MODELS:
        model_rows = [row for row in rows if row["model"] == model]
        assert {row[changed] for row in model_rows} == values
        baseline = independent_values(model, analytical_optimum(model, base).price, base)
        for row in model_rows:
            for field, value in asdict(base).items():
                if field != changed:
                    assert row[field] == value
            for field in ("price", "quantity", "revenue", "profit"):
                assert row[f"baseline_{field}"] == pytest.approx(baseline[field])


@pytest.mark.parametrize("model,cost,price,quantity,revenue,profit", [
    ("linear", 6, 10.5, 90, 945, 405),
    ("linear", 7, 11, 80, 880, 320),
    ("constant_elasticity", 6, 12, 625 / 9, 2500 / 3, 1250 / 3),
    ("constant_elasticity", 7, 14, 2500 / 49, 5000 / 7, 2500 / 7),
])
def test_cost_investigation_preserves_independently_reproducible_benchmark_values(
    model, cost, price, quantity, revenue, profit,
):
    row = row_for("unit_cost", model, c=cost)
    assert row["price"] == pytest.approx(price)
    assert row["quantity"] == pytest.approx(quantity)
    assert row["revenue"] == pytest.approx(revenue)
    assert row["profit"] == pytest.approx(profit)


@pytest.mark.parametrize("model,price_change,profit_change", [
    ("linear", 0.5, -85),
    ("constant_elasticity", 2, -1250 / 21),
])
def test_one_pound_cost_increase_has_model_specific_pass_through(model, price_change, profit_change):
    row = row_for("unit_cost", model, c=7)
    assert row["price_change"] == pytest.approx(price_change)
    assert row["profit_change"] == pytest.approx(profit_change)
    assert row["quantity_change"] < 0
    assert row["revenue_change"] < 0


@pytest.mark.parametrize("model", MODELS)
def test_fixed_cost_investigation_changes_profit_without_changing_entire_price_set(model):
    before = row_for("fixed_cost", model, F=0)
    after = row_for("fixed_cost", model, F=50)
    assert after["optimal_intervals"] == before["optimal_intervals"]
    for field in ("price", "quantity", "revenue", "variable_cost", "contribution"):
        assert after[field] == before[field]
    assert after["profit_change"] == pytest.approx(-50)
    assert after["total_cost"] - before["total_cost"] == pytest.approx(50)


def test_price_cap_has_a_financial_effect_only_for_the_model_whose_optimum_is_excluded():
    linear = row_for("price_cap", "linear", price_max=11)
    ce = row_for("price_cap", "constant_elasticity", price_max=11)
    assert linear["price"] == 10.5
    assert linear["profit_change"] == 0
    assert ce["price"] == 11
    assert ce["quantity"] == pytest.approx(10000 / 121)
    assert ce["profit"] == pytest.approx(50000 / 121)
    assert ce["profit_change"] == pytest.approx(50000 / 121 - 1250 / 3)
    assert ce["boundary"] == "upper_boundary"


def test_high_cost_comparison_captures_linear_zero_sales_plateau_and_continuing_fixed_cost():
    linear = row_for("high_cost", "linear", c=20)
    ce = row_for("high_cost", "constant_elasticity", c=20)
    assert linear["optimal_intervals"] == ((15, 20),)
    assert linear["quantity"] == 0
    assert linear["revenue"] == 0
    assert linear["total_cost"] == 50
    assert linear["profit"] == -50
    assert ce["optimal_intervals"] == ((20, 20),)
    assert ce["quantity"] == pytest.approx(25)
    assert ce["revenue"] == pytest.approx(500)
    assert ce["total_cost"] == pytest.approx(550)
    assert ce["profit"] == -50


@pytest.mark.parametrize("model,revenue_price,max_revenue,profit_at_revenue_price", [
    ("linear", 7.5, 1125, 225),
    ("constant_elasticity", 1, 10000, -50000),
])
def test_revenue_and_profit_are_distinct_objectives_with_material_financial_consequences(
    model, revenue_price, max_revenue, profit_at_revenue_price,
):
    params = Parameters()
    revenue_result = revenue_optimum(model, params)
    profit_result = analytical_optimum(model, params)
    assert revenue_result["price"] == pytest.approx(revenue_price)
    assert revenue_result["revenue"] == pytest.approx(max_revenue)
    assert revenue_result["profit"] == pytest.approx(profit_at_revenue_price)
    assert revenue_result["price"] != profit_result.price
    assert revenue_result["revenue"] > profit_result.revenue
    assert revenue_result["profit"] < profit_result.profit


@pytest.mark.parametrize("elasticity,expected_price,intervals,boundary", [
    (0.5, 15, ((15, 15),), "upper_boundary"),
    (1, 1, ((1, 15),), "multiple"),
    (2, 1, ((1, 1),), "lower_boundary"),
])
@pytest.mark.parametrize("cost", [0, 6])
def test_constant_elasticity_revenue_regimes_include_the_full_flat_set(
    elasticity, expected_price, intervals, boundary, cost,
):
    params = Parameters(e=elasticity, c=cost, F=50)
    result = revenue_optimum("constant_elasticity", params)
    assert result["price"] == expected_price
    assert result["optimal_intervals"] == intervals
    assert result["boundary"] == boundary
    assert result["profit"] == pytest.approx(result["revenue"] - cost * result["quantity"] - 50)
    if elasticity == 1:
        for price in (1, 6, 10, 15):
            assert evaluate("constant_elasticity", price, params)["revenue"] == pytest.approx(1000)
        if cost == 0:
            assert result["profit"] == pytest.approx(950)
        else:
            assert analytical_optimum("constant_elasticity", params).price == 15


@pytest.mark.parametrize("lower,upper,expected_price,intervals,boundary", [
    (1, 5, 5, ((5, 5),), "upper_boundary"),
    (8, 10, 8, ((8, 8),), "lower_boundary"),
    (13, 14, 13, ((13, 13),), "lower_boundary"),
    (16, 20, 16, ((16, 20),), "multiple"),
])
def test_linear_revenue_respects_boundaries_and_entire_zero_demand_plateau(
    lower, upper, expected_price, intervals, boundary,
):
    params = Parameters(price_min=lower, price_max=upper, F=50)
    result = revenue_optimum("linear", params)
    assert result["price"] == expected_price
    assert result["optimal_intervals"] == intervals
    assert result["boundary"] == boundary
    for lo, hi in intervals:
        for price in (lo, (lo + hi) / 2, hi):
            assert independent_values("linear", price, params)["revenue"] == pytest.approx(result["revenue"])
    if lower >= 15:
        assert result["revenue"] == 0
        assert result["profit"] == -50


@pytest.mark.parametrize("params", [
    Parameters(), Parameters(e=0.5), Parameters(e=1), Parameters(e=3, c=0),
    Parameters(price_max=5), Parameters(price_min=13, price_max=14),
    Parameters(price_min=16, price_max=20), Parameters(p0=4, Q0=50, e=3, c=7, F=50),
])
@pytest.mark.parametrize("model", MODELS)
def test_revenue_optimum_agrees_with_separate_scipy_search_and_financial_equations(params, model):
    result = revenue_optimum(model, params)
    # Search the non-flat part separately: bounded golden-section search can
    # otherwise stop entirely within the clipped linear zero-revenue plateau.
    cutoff = params.p0 * (1 + 1 / params.e)
    search_upper = min(params.price_max, cutoff) if model == 'linear' and params.price_min < cutoff else params.price_max
    numerical = minimize_scalar(lambda price: -price * demand(model, price, params),
                                bounds=(params.price_min, search_upper), method="bounded",
                                options={"xatol": 1e-12})
    assert numerical.success
    candidates = [params.price_min, params.price_max, float(numerical.x)]
    best_revenue = max(independent_values(model, price, params)["revenue"] for price in candidates)
    assert result["revenue"] == pytest.approx(best_revenue, rel=1e-8, abs=1e-7)
    assert member(result["price"], result["optimal_intervals"])
    independent = independent_values(model, result["price"], params)
    for field in FINANCIAL_FIELDS:
        assert result[field] == pytest.approx(independent[field], rel=1e-10, abs=1e-8)


def test_unknown_investigation_and_revenue_model_raise_clear_errors():
    with pytest.raises(ValueError):
        build_investigation("unknown")
    with pytest.raises(ValueError):
        revenue_optimum("unknown", Parameters())


def test_complete_export_includes_every_investigation_and_no_unfinished_personal_fields():
    report = report_markdown()
    assert "Complete Mathematical Investigation and Findings" in report
    for key in KEYS:
        assert build_investigation(key)["title"] in report
    for phrase in ("My prediction", "My reflection", "To complete in your own words",
                   "Record your own reasoning", "AI-assisted answers", "Download my notes"):
        assert phrase not in report
    assert "£10.50" in report
    assert "£12.00" in report
    assert "£14.00" in report
    assert "£320.00" in report
    assert "£357.14" in report


def test_reports_explain_risk_capacity_own_price_limits_and_accurate_authorship():
    for text in (report_markdown(), summary_markdown()):
        assert "Model-dependent pricing risk" in text
        assert "£45.00" in text
        assert "£8.50" in text
        assert "smallest" in text
        assert "10,000" in text
        assert "capacity constraint" in text
        assert "substitution effect" in text
        assert "not an established sales forecast" in text or "not an established sales forecast" in text.lower()
        assert METHODOLOGY in text
    assert "code development and explanatory drafting" in METHODOLOGY
    assert "personally completed" in METHODOLOGY
    summary = summary_markdown()
    assert len(summary.split()) < 1000
    assert "Unit cost and margin" in summary
    assert "Price restrictions" in summary
    assert "Fixed cost and operating profit" in summary
    full = report_markdown()
    assert "Marginal revenue equals marginal cost" in full
    assert "MR = £6.00/unit and MC = £6.00/unit" in full
    assert "not required at a binding boundary" in full

