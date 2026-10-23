"""Direct-equation checks of decisions, model risk and reproducible exports."""

import ast
import csv
from dataclasses import asdict, replace
import math

import pytest

import analysis
from analysis import chosen_price_rows, model_risk_rows
from generate_report import write_reports
from models import Parameters


MODELS = ("linear", "constant_elasticity")
FINANCIAL = ("price", "quantity", "revenue", "variable_cost", "total_cost", "contribution", "profit")


def direct(model, price, params):
    """Independent equations: no model evaluator or optimiser is called."""
    quantity = (max(0.0, params.Q0 * (1 + params.e) - params.e * params.Q0 * price / params.p0)
                if model == "linear" else params.Q0 * (price / params.p0) ** -params.e)
    contribution = (price - params.c) * quantity
    return dict(price=price, quantity=quantity, revenue=price * quantity,
                variable_cost=params.c * quantity, total_cost=params.c * quantity + params.F,
                contribution=contribution, profit=contribution - params.F)


def direct_optimum(model, params):
    """Calculus/monotonicity, including exact tied sets, independently stated."""
    lower, upper = params.price_min, params.price_max
    if model == "linear":
        cutoff = params.p0 * (1 + 1 / params.e)
        if lower >= cutoff or (params.c >= cutoff and upper >= cutoff):
            return ((max(lower, cutoff), upper),)
        price = min(upper, max(lower, (cutoff + params.c) / 2))
    elif params.c == 0 and params.e == 1:
        return ((lower, upper),)
    elif params.e <= 1:
        price = upper
    elif params.c == 0:
        price = lower
    else:
        price = min(upper, max(lower, params.e * params.c / (params.e - 1)))
    return ((price, price),)


def find(rows, model, scenario):
    return next(row for row in rows if row["model"] == model and row["scenario"] == scenario)


def test_benchmark_chosen_price_and_model_risk_acceptance_values():
    params = Parameters()
    rows = chosen_price_rows(params, 12)
    assert len(rows) == 6
    for model in MODELS:
        assert find(rows, model, "Starting price")["profit"] == 400
    linear = find(rows, "linear", "Chosen test price")
    assert linear["quantity"] == pytest.approx(60)
    assert linear["revenue"] == pytest.approx(720)
    assert linear["variable_cost"] == pytest.approx(360)
    assert linear["contribution"] == pytest.approx(360)
    assert linear["profit_change"] == pytest.approx(-40)
    assert linear["profit_change_percent"] == pytest.approx(-10)
    ce = find(rows, "constant_elasticity", "Profit optimum")
    assert ce["price"] == 12
    assert ce["profit"] == pytest.approx(1250 / 3)
    assert ce["profit_change_percent"] == pytest.approx(25 / 6)
    risk = {(r["candidate_source"], r["evaluated_model"]): r for r in model_risk_rows(params)}
    assert risk[("constant_elasticity", "linear")]["profit"] == pytest.approx(360)
    assert risk[("constant_elasticity", "linear")]["regret"] == pytest.approx(45)
    assert risk[("linear", "constant_elasticity")]["profit"] == pytest.approx(20000 / 49)
    assert risk[("linear", "constant_elasticity")]["regret"] == pytest.approx(1250 / 3 - 20000 / 49)
    for model in MODELS:
        assert risk[(model, model)]["regret"] == 0


@pytest.mark.parametrize("params", [
    Parameters(), Parameters(e=0.5), Parameters(e=1), Parameters(e=1, c=0),
    Parameters(e=3, c=0), Parameters(price_max=5), Parameters(price_min=13, price_max=14),
    Parameters(price_min=16, price_max=20), Parameters(c=20, F=50, price_max=20),
    Parameters(p0=10.123456789, Q0=71.23456789, e=1.87654321, c=6.123456789, F=19.87654321),
])
def test_comparison_boundaries_ties_and_finances_follow_independent_equations(params):
    for test_price in (params.price_min, params.price_max):
        rows = chosen_price_rows(params, test_price, period="month")
        assert len(rows) == 6
        for row in rows:
            model = row["model"]
            expected = direct(model, row["price"], params)
            baseline = direct(model, params.p0, params)
            for field in FINANCIAL:
                assert row[field] == pytest.approx(expected[field], rel=1e-11, abs=1e-8)
            assert row["profit_change"] == pytest.approx(expected["profit"] - baseline["profit"], abs=1e-8)
            assert row["period"] == "month"
            assert all(row[key] == value for key, value in asdict(params).items())
            expected_set = direct_optimum(model, params)
            for actual, wanted in zip(row["optimal_intervals"], expected_set, strict=True):
                assert actual == pytest.approx(wanted)
            if row["scenario"] == "Profit optimum":
                assert row["price"] == pytest.approx(expected_set[0][0])

    risk = model_risk_rows(params, period="day")
    assert {(r["candidate_source"], r["evaluated_model"]) for r in risk} == {
        (source, model) for source in MODELS for model in MODELS
    }
    for row in risk:
        model = row["evaluated_model"]
        source_set = direct_optimum(row["candidate_source"], params)
        model_set = direct_optimum(model, params)
        assert row["candidate_price"] == pytest.approx(source_set[0][0])
        expected = direct(model, source_set[0][0], params)
        maximum = direct(model, model_set[0][0], params)
        for field in FINANCIAL:
            assert row[field] == pytest.approx(expected[field], rel=1e-11, abs=1e-8)
        assert row["max_profit"] == pytest.approx(maximum["profit"], abs=1e-8)
        assert row["regret"] == pytest.approx(maximum["profit"] - expected["profit"], abs=1e-8)
        assert row["regret"] >= 0
        assert row["period"] == "day"
        assert all(row[key] == value for key, value in asdict(params).items())
        for field, expected_set in (("candidate_optimal_intervals", source_set),
                                    ("evaluated_optimal_intervals", model_set)):
            for actual, wanted in zip(row[field], expected_set, strict=True):
                assert actual == pytest.approx(wanted)


@pytest.mark.parametrize("fixed_cost", [400, 450])
def test_nonpositive_starting_profit_omits_percentage_with_explanation(fixed_cost):
    rows = chosen_price_rows(Parameters(F=fixed_cost), 12)
    for row in rows:
        assert row["baseline_profit"] <= 0
        assert row["profit_change_percent"] is None
        assert "zero or negative" in row["percentage_explanation"]
    assert find(rows, "linear", "Chosen test price")["profit_change"] == pytest.approx(-40)


def test_starting_price_outside_interval_is_evaluated_and_clearly_flagged():
    rows = chosen_price_rows(Parameters(price_min=11), 12)
    for model in MODELS:
        start = find(rows, model, "Starting price")
        assert start["price"] == 10
        assert start["profit"] == 400
        assert start["permitted"] is False
        assert find(rows, model, "Chosen test price")["permitted"] is True


@pytest.mark.parametrize("price", [0, -1, 0.999999, 15.000001, math.inf, -math.inf, math.nan, True, "12", None])
def test_invalid_test_price_is_rejected(price):
    with pytest.raises(ValueError, match="Test price"):
        chosen_price_rows(Parameters(), price)


@pytest.mark.parametrize("period", [None, "", "  ", 12])
def test_period_requires_a_label(period):
    for function in (lambda: chosen_price_rows(Parameters(), 12, period),
                     lambda: model_risk_rows(Parameters(), period)):
        with pytest.raises(ValueError, match="Period"):
            function()


def test_tied_candidates_report_whole_sets_and_use_the_smallest_representative():
    high_cost = model_risk_rows(Parameters(c=20, F=50, price_max=20))
    linear_source = [r for r in high_cost if r["candidate_source"] == "linear"]
    assert all(r["candidate_optimal_intervals"] == ((15, 20),) for r in linear_source)
    assert all(r["candidate_price"] == 15 and r["representative_price"] for r in linear_source)
    other_curve = next(r for r in linear_source if r["evaluated_model"] == "constant_elasticity")
    assert other_curve["regret"] == pytest.approx(2000 / 9)
    flat = model_risk_rows(Parameters(e=1, c=0))
    ce_source = [r for r in flat if r["candidate_source"] == "constant_elasticity"]
    assert all(r["candidate_price"] == 1 for r in ce_source)
    assert all(r["candidate_optimal_intervals"] == ((1, 15),) for r in ce_source)


def test_large_fixed_cost_does_not_erase_profit_changes_or_model_regret():
    params = Parameters(F=1e20)
    chosen = find(chosen_price_rows(params, 10.5), "linear", "Chosen test price")
    assert chosen["profit_change"] == pytest.approx(5)
    assert chosen["profit_change_percent"] is None
    risk = next(r for r in model_risk_rows(params)
                if r["candidate_source"] == "constant_elasticity" and r["evaluated_model"] == "linear")
    assert risk["regret"] == pytest.approx(45)


def test_only_machine_roundoff_negative_regret_is_removed(monkeypatch):
    original = analysis.evaluate

    def slightly_high(model, price, params):
        result = original(model, price, params)
        result["contribution"] = math.nextafter(result["contribution"], math.inf)
        return result

    monkeypatch.setattr(analysis, "evaluate", slightly_high)
    rows = model_risk_rows(Parameters())
    assert all(r["regret"] >= 0 for r in rows)
    assert all(r["regret"] == 0 for r in rows if r["candidate_source"] == r["evaluated_model"])


def test_substantive_negative_regret_surfaces_an_engine_mismatch(monkeypatch):
    original = analysis.analytical_optimum

    def incorrect_maximum(model, params):
        result = original(model, params)
        return replace(result, contribution=result.contribution - 1, profit=result.profit - 1)

    monkeypatch.setattr(analysis, "analytical_optimum", incorrect_maximum)
    with pytest.raises(ValueError, match="Negative regret"):
        model_risk_rows(Parameters())


def test_model_filter_can_preserve_a_valid_curve_when_another_overflows():
    params = Parameters(e=400)
    with pytest.raises(ValueError, match="floating-point"):
        chosen_price_rows(params, 1)
    rows = chosen_price_rows(params, 1, models="linear")
    assert len(rows) == 3
    assert {r["model"] for r in rows} == {"linear"}
    with pytest.raises(ValueError, match="Unknown demand model"):
        chosen_price_rows(Parameters(), 12, models="unknown")


def test_generated_documents_and_csv_keep_inputs_sets_and_full_float_precision(tmp_path):
    paths = write_reports(tmp_path)
    assert {p.name for p in paths} == {
        "investigation_worksheet.md", "FINDINGS_SUMMARY.md", "chosen_price_comparison.csv", "model_risk.csv"
    }
    comparisons = (("chosen_price_comparison.csv", chosen_price_rows(Parameters(), 12)),
                   ("model_risk.csv", model_risk_rows(Parameters())))
    for filename, expected_rows in comparisons:
        with (tmp_path / "evidence" / filename).open(encoding="utf-8", newline="") as handle:
            saved = list(csv.DictReader(handle))
        assert len(saved) == len(expected_rows)
        for row, expected in zip(saved, expected_rows, strict=True):
            assert row["period"] == "week"
            for key, value in expected.items():
                if isinstance(value, float):
                    assert float(row[key]) == value
                elif key.endswith("intervals"):
                    assert ast.literal_eval(row[key]) == value
            assert all(float(row[key]) == value for key, value in asdict(Parameters()).items())
    ce_chosen = next(row for row in expected_rows if row.get("evaluated_model") == "constant_elasticity")
    assert ce_chosen["quantity"] != round(ce_chosen["quantity"], 4)
    full = (tmp_path / "investigation_worksheet.md").read_text(encoding="utf-8")
    summary = (tmp_path / "FINDINGS_SUMMARY.md").read_text(encoding="utf-8")
    assert full == analysis.report_markdown()
    assert summary == analysis.summary_markdown()

