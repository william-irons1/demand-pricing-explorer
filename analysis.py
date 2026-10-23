"""Reproducible mathematical investigations built from the implemented models.

Every result and numerical comparison is calculated at generation time.  The
scenario choices are fixed so a reader can reproduce the same investigation.
"""

from dataclasses import asdict, replace
import math
from numbers import Real

from models import (
    MODEL_LABELS, Parameters, analytical_optimum, evaluate, mr_mc_check, sensitivity_rows,
    unconstrained_summary, zero_demand_price,
)


INVESTIGATION_LABELS = {
    "elasticity": "Elasticity and pricing",
    "unit_cost": "Unit cost and margin",
    "price_cap": "Price restrictions",
    "fixed_cost": "Fixed cost and operating profit",
    "high_cost": "High cost and zero-demand plateau",
}
METHODOLOGY = (
    "AI assisted with code development and explanatory drafting. Results are calculated "
    "deterministically from the displayed mathematical models and checked by automated "
    "tests and separate equation-based calculations. These software checks do not establish "
    "which checks the project owner has personally completed."
)


def investigation_keys():
    return tuple(INVESTIGATION_LABELS)


def _n(value):
    """Readable workings retain more precision than the financial tables."""
    return f"{value:,.6f}".rstrip("0").rstrip(".")


def _money(value):
    return ("−" if value < 0 else "") + f"£{abs(value):,.2f}"


def _signed_money(value):
    return ("+" if value > 0 else "−" if value < 0 else "") + f"£{abs(value):,.2f}"


def _quantity(value):
    return f"{value:,.4f}".rstrip("0").rstrip(".")


def _set_text(intervals):
    pieces = []
    for lower, upper in intervals:
        pieces.append(_money(lower) if lower == upper else f"[{_money(lower)}, {_money(upper)}]")
    return " ∪ ".join(pieces)


def _multiple(intervals):
    return len(intervals) > 1 or any(lo < hi for lo, hi in intervals)


def _period_label(period):
    if not isinstance(period, str) or not period.strip():
        raise ValueError("Period must be a non-empty label; it does not convert inputs.")
    return period


def _permitted_test_price(params, test_price):
    if (isinstance(test_price, bool) or not isinstance(test_price, Real)
            or not math.isfinite(test_price)):
        raise ValueError("Test price must be a finite real number.")
    test_price = float(test_price)
    if not params.price_min <= test_price <= params.price_max:
        raise ValueError("Test price must lie within the permitted price interval.")
    return test_price


def chosen_price_rows(params, test_price, period="week", models=None):
    """Compare starting, chosen and profit-optimal prices without rounding.

    The starting price is evaluated even when outside the permitted interval;
    only the chosen price must be feasible. ``models`` can select a model whose
    results remain available if another curve exceeds floating-point range.
    Period is metadata: all quantities and fixed costs retain their input units.
    """
    test_price = _permitted_test_price(params, test_price)
    period = _period_label(period)
    models = tuple(MODEL_LABELS) if models is None else ((models,) if isinstance(models, str) else tuple(models))
    rows = []
    for model in models:
        if model not in MODEL_LABELS:
            raise ValueError(f"Unknown demand model {model!r}.")
        baseline = evaluate(model, params.p0, params)
        optimum = analytical_optimum(model, params)
        for scenario, price in (("Starting price", params.p0), ("Chosen test price", test_price),
                                ("Profit optimum", min(lo for lo, _ in optimum.optimal_intervals))):
            values = evaluate(model, price, params)
            # F cancels algebraically; subtracting rounded large negative profits
            # could otherwise erase a genuine change in operating contribution.
            change = values["contribution"] - baseline["contribution"]
            percent = (100.0 * (change / baseline["profit"])) if baseline["profit"] > 0 else None
            if not math.isfinite(change) or (percent is not None and not math.isfinite(percent)):
                raise ValueError("Profit change exceeds floating-point range; use smaller inputs.")
            explanation = ("Percentage change is 100 × profit change / positive starting profit."
                           if percent is not None else
                           "Percentage change omitted because starting profit is zero or negative; "
                           "the absolute change remains meaningful.")
            rows.append(dict(**asdict(params), period=period, model=model, model_label=MODEL_LABELS[model],
                             scenario=scenario, **values, baseline_price=params.p0,
                             baseline_profit=baseline["profit"], baseline_contribution=baseline["contribution"],
                             profit_change=change, profit_change_percent=percent,
                             percentage_explanation=explanation,
                             permitted=params.price_min <= price <= params.price_max,
                             optimal_intervals=optimum.optimal_intervals,
                             boundary=optimum.boundary, warning=optimum.warning,
                             representative_price=_multiple(optimum.optimal_intervals)))
    return rows


def _checked_regret(max_contribution, contribution):
    """Remove only machine roundoff, and surface substantive solver mismatches."""
    regret = max_contribution - contribution
    if not math.isfinite(regret):
        raise ValueError("Regret exceeds floating-point range; use smaller inputs.")
    tolerance = 8.0 * max(math.ulp(max_contribution), math.ulp(contribution))
    if regret < -tolerance:
        raise ValueError("Negative regret exceeds floating-point tolerance; review the optimisation result.")
    return 0.0 if abs(regret) <= tolerance else regret


def model_risk_rows(params, period="week"):
    """Evaluate each model's smallest optimal representative under both curves.

    All four candidate/evaluated-model combinations share the feasible interval.
    Full optimal sets remain in each row. Regret equals maximum profit minus
    candidate profit; computing the equivalent contribution difference avoids
    cancellation when a large unavoidable fixed cost is present.
    """
    period = _period_label(period)
    optima = {model: analytical_optimum(model, params) for model in MODEL_LABELS}
    rows = []
    for source, candidate in optima.items():
        price = min(lo for lo, _ in candidate.optimal_intervals)
        for model, maximum in optima.items():
            values = evaluate(model, price, params)
            regret = _checked_regret(maximum.contribution, values["contribution"])
            rows.append(dict(**asdict(params), period=period, candidate_source=source,
                             candidate_source_label=MODEL_LABELS[source], candidate_price=price,
                             candidate_optimal_intervals=candidate.optimal_intervals,
                             candidate_boundary=candidate.boundary,
                             representative_price=_multiple(candidate.optimal_intervals),
                             evaluated_model=model, evaluated_model_label=MODEL_LABELS[model],
                             **values, evaluated_optimal_intervals=maximum.optimal_intervals,
                             max_profit=maximum.profit, max_contribution=maximum.contribution,
                             regret=regret))
    return rows


def revenue_optimum(model, params):
    """Maximise revenue over the same closed interval, reporting every tie.

    Costs affect the returned profit, but cannot affect the revenue optimum.
    For constant elasticity e=1 every permitted price earns the same revenue;
    the smallest is a displayed representative, not a unique recommendation.
    """
    if model not in MODEL_LABELS:
        raise ValueError(f"Unknown demand model {model!r}.")
    lower, upper = params.price_min, params.price_max
    if model == "linear":
        cutoff = zero_demand_price(params)
        if lower >= cutoff:
            intervals = ((lower, upper),)
        else:
            price = max(lower, min(upper, cutoff / 2))
            intervals = ((price, price),)
    elif params.e == 1:
        intervals = ((lower, upper),)
    else:
        price = lower if params.e > 1 else upper
        intervals = ((price, price),)
    price = intervals[0][0]
    boundary = ("multiple" if _multiple(intervals) else
                "lower_boundary" if price == lower else
                "upper_boundary" if price == upper else "interior")
    warning = ("Every price in the reported optimal set maximises revenue; the smallest "
               "is shown as a representative, and its profit need not be the best profit "
               "within that set.") if boundary == "multiple" else None
    return dict(model=model, **evaluate(model, price, params),
                optimal_intervals=intervals, boundary=boundary, warning=warning)


def _rows(key):
    if key == "high_cost":
        defaults = Parameters(F=50, price_max=20)
        baseline = {m: analytical_optimum(m, defaults) for m in MODEL_LABELS}
        rows = []
        for cost in (defaults.c, 20.0):
            params = replace(defaults, c=cost)
            for model, label in MODEL_LABELS.items():
                opt = analytical_optimum(model, params)
                summary = unconstrained_summary(model, params)
                rows.append(dict(investigation=key,
                                 scenario=f"c = £{cost:g}" + (" (baseline)" if cost == defaults.c else ""),
                                 **asdict(params), **asdict(opt), model_label=label,
                                 baseline_price=baseline[model].price,
                                 baseline_profit=baseline[model].profit,
                                 price_change=opt.price - baseline[model].price,
                                 profit_change=opt.profit - baseline[model].profit,
                                 unconstrained_status=summary["status"],
                                 unconstrained_explanation=summary["explanation"]))
    else:
        rows = sensitivity_rows(key)
    bases = {row["model"]: row for row in rows if "(baseline)" in row["scenario"]}
    for row in rows:
        baseline = bases[row["model"]]
        row["baseline_revenue"] = baseline["revenue"]
        row["baseline_quantity"] = baseline["quantity"]
        row["revenue_change"] = row["revenue"] - baseline["revenue"]
        row["quantity_change"] = row["quantity"] - baseline["quantity"]
        params = Parameters(**{name: row[name] for name in Parameters.__dataclass_fields__})
        rev = revenue_optimum(row["model"], params)
        for name in ("price", "quantity", "revenue", "profit"):
            row[f"revenue_max_{name}"] = rev[name]
        row["revenue_optimal_intervals"] = rev["optimal_intervals"]
        row["revenue_boundary"] = rev["boundary"]
        row["revenue_gain_from_profit_price"] = rev["revenue"] - row["revenue"]
        row["profit_cost_of_revenue_objective"] = row["profit"] - rev["profit"]
        row["optimal_price_set"] = _set_text(row["optimal_intervals"])
        row["representative_price"] = _multiple(row["optimal_intervals"])
    return rows


def _workings(row):
    p = Parameters(**{name: row[name] for name in Parameters.__dataclass_fields__})
    model = row["model"]
    lower, upper = p.price_min, p.price_max
    price = row["price"]
    steps = [
        f"Inputs: p₀ = {_money(p.p0)}, Q₀ = {_quantity(p.Q0)} units/week, "
        f"e = {_n(p.e)}, c = {_money(p.c)}/unit, F = {_money(p.F)}/week; "
        f"permitted p ∈ [{_money(lower)}, {_money(upper)}].",
    ]
    if model == "linear":
        a, b, cutoff = p.Q0 * (1 + p.e), p.e * p.Q0 / p.p0, zero_demand_price(p)
        candidate = (cutoff + p.c) / 2
        steps += [
            f"a = Q₀(1 + e) = {_n(p.Q0)}(1 + {_n(p.e)}) = {_n(a)}; "
            f"b = eQ₀/p₀ = {_n(p.e)} × {_n(p.Q0)}/{_n(p.p0)} = {_n(b)}. "
            f"Thus Q(p) = max(0, {_n(a)} − {_n(b)}p).",
            f"The zero-demand cutoff is z = a/b = {_n(a)}/{_n(b)} = {_n(cutoff)}. "
            f"For p < {_n(cutoff)}, π(p) = (p − {_n(p.c)})({_n(a)} − {_n(b)}p) − {_n(p.F)}.",
            f"On this positive-demand part, π′(p) = a + bc − 2bp = "
            f"{_n(a + b * p.c)} − {_n(2 * b)}p. Setting π′ = 0 gives "
            f"v = (z + c)/2 = ({_n(cutoff)} + {_n(p.c)})/2 = {_n(candidate)}.",
        ]
        if lower <= candidate <= upper and candidate < cutoff:
            steps.append(f"v = {_n(candidate)} is permitted and below z = {_n(cutoff)}. "
                         f"π″ = −2b = −{_n(2*b)} < 0, so it is the strict maximum "
                         "on the positive-demand piece; compare it with the boundaries and plateau.")
        else:
            failures = []
            if not lower <= candidate <= upper:
                failures.append("outside the permitted interval")
            if candidate >= cutoff:
                failures.append("at or beyond the cutoff, where the positive-demand quadratic no longer applies")
            steps.append(f"The candidate {_n(candidate)} is " + " and ".join(failures) +
                         ". It cannot be used as an interior positive-demand maximum.")
        candidates = {lower, upper}
        if lower <= candidate <= upper and candidate < cutoff:
            candidates.add(candidate)
        if lower <= cutoff <= upper:
            candidates.add(cutoff)
        comparisons = "; ".join(f"p = {_n(point)}: π = {_money(evaluate(model, point, p)['profit'])}"
                                for point in sorted(candidates))
        steps.append("Candidate comparison: " + comparisons + ".")
        if upper >= cutoff:
            steps.append(f"Every permitted zero-demand price in "
                         f"[{_money(max(lower, cutoff))}, {_money(upper)}] gives "
                         f"Q = 0, contribution = £0.00 and π = −F = {_money(-p.F)}. "
                         "Compare this entire plateau with the positive-demand candidates.")
        steps.append(f"Selected quantity: Q({_n(price)}) = max(0, {_n(a)} − "
                     f"{_n(b)} × {_n(price)}) = {_quantity(row['quantity'])} units/week.")
    else:
        steps += [
            f"Q(p) = {_n(p.Q0)}(p/{_n(p.p0)})^(−{_n(p.e)}). "
            f"π(p) = (p − {_n(p.c)}) × {_n(p.Q0)}(p/{_n(p.p0)})^(−{_n(p.e)}) − {_n(p.F)}.",
            f"Write K = Q₀p₀^e > 0. Differentiation gives "
            f"π′(p) = Kp^(−e−1)[(1−e)p + ec] = "
            f"Kp^(−{_n(p.e+1)})[({_n(1-p.e)})p + {_n(p.e*p.c)}]. "
            "The first factor is positive, so the bracket decides whether profit rises or falls.",
        ]
        if p.e > 1 and p.c > 0:
            candidate = p.c * (1 + 1 / (p.e - 1))
            steps.append(f"v = ec/(e−1) = {_n(p.e)} × {_n(p.c)}/({_n(p.e)} − 1) "
                         f"= {_n(candidate)}. The derivative is positive below v and negative "
                         "above v, proving a global maximum over positive prices.")
            if lower < candidate < upper:
                steps.append(f"The candidate lies strictly inside the permitted interval. "
                             f"π″(v) = K(1−e)v^(−e−1) < 0 because 1−e = {_n(1-p.e)} < 0.")
            else:
                steps.append(f"Restricting the candidate to the interval gives "
                             f"min({_n(upper)}, max({_n(lower)}, {_n(candidate)})) = {_n(price)}. "
                             "The maximum is at a permitted boundary; its derivative need not be zero.")
        elif p.e == 1 and p.c == 0:
            steps.append("Here e = 1 and c = 0, so the derivative is zero everywhere. "
                         "Revenue and profit are constant over the whole permitted interval; "
                         "every permitted price is optimal.")
        elif p.e > 1:
            steps.append(f"Here c = 0 and e = {_n(p.e)} > 1. The derivative is strictly "
                         f"negative, so the bounded maximum is the lower boundary {_money(lower)}. "
                         "Over all positive prices profit grows without bound as p tends to zero; "
                         "there is no finite unrestricted maximiser.")
        else:
            steps.append(f"Here e = {_n(p.e)} " + ("< 1" if p.e < 1 else "= 1 with c > 0") +
                         ". The derivative is strictly positive for every positive price, "
                         f"so the bounded maximum is the upper boundary {_money(upper)}. "
                         "No interior stationary maximum is available.")
        comparisons = "; ".join(f"p = {_n(point)}: π = {_money(evaluate(model, point, p)['profit'])}"
                                for point in sorted({lower, upper, price}))
        steps.append("Candidate comparison: " + comparisons + ".")
        steps.append(f"Selected quantity: Q({_n(price)}) = {_n(p.Q0)} × "
                     f"({_n(price)}/{_n(p.p0)})^(−{_n(p.e)}) = {_quantity(row['quantity'])} units/week.")
    steps += [
        f"Full profit-maximising price set: {_set_text(row['optimal_intervals'])}. " +
        (f"The displayed price {_money(price)} is the smallest representative of a tied set."
         if _multiple(row["optimal_intervals"]) else f"This maximum is classified as {row['boundary'].replace('_', ' ')}."),
        f"R = pQ = {_n(price)} × {_n(row['quantity'])} = {_money(row['revenue'])}/week; "
        f"VC = cQ = {_n(p.c)} × {_n(row['quantity'])} = {_money(row['variable_cost'])}/week; "
        f"TC = VC + F = {_money(row['variable_cost'])} + {_money(p.F)} = {_money(row['total_cost'])}/week.",
        f"Contribution = (p−c)Q = ({_n(price)} − {_n(p.c)}) × {_n(row['quantity'])} "
        f"= {_money(row['contribution'])}/week. Operating profit π = R−TC = "
        f"{_money(row['revenue'])} − {_money(row['total_cost'])} = {_money(row['profit'])}/week.",
        f"Change from this model's baseline: price {_signed_money(row['price_change'])}; "
        f"quantity {row['quantity_change']:+.4f} units/week; revenue {_signed_money(row['revenue_change'])}/week; "
        f"profit {_signed_money(row['profit_change'])}/week. Differences use unrounded calculations.",
    ]
    return dict(model=model, scenario=row["scenario"], steps=steps)


def _scenario_result(row):
    return (f"{row['model_label']} ({row['scenario']}): optimal price set "
            f"{_set_text(row['optimal_intervals'])}, quantity {_quantity(row['quantity'])} units/week, "
            f"revenue {_money(row['revenue'])}/week and operating profit {_money(row['profit'])}/week")


def build_investigation(key):
    if key not in INVESTIGATION_LABELS:
        raise ValueError(f"Unknown investigation {key!r}; choose {investigation_keys()}.")
    rows = _rows(key)
    bases = {r["model"]: r for r in rows if "(baseline)" in r["scenario"]}
    others = {r["model"]: r for r in rows if "(baseline)" not in r["scenario"]}
    reference = bases["linear"]
    common = f"p₀ = {_money(reference['p0'])}, Q₀ = {_quantity(reference['Q0'])} units/week"
    demand_held = f"e = {_n(reference['e'])}"
    cost_held = f"c = {_money(reference['c'])}/unit"
    fixed_held = f"F = {_money(reference['F'])}/week"
    interval_held = f"permitted prices {_money(reference['price_min'])}–{_money(reference['price_max'])}"
    equations = [r"Q_L(p)=\max(0,a-bp),\quad a=Q_0(1+e),\quad b=\frac{eQ_0}{p_0}",
                 r"Q_C(p)=Q_0(p/p_0)^{-e}",
                 r"R=pQ,\quad TC=cQ+F,\quad \pi=(p-c)Q-F"]
    if key == "elasticity":
        question = "How does the assumed responsiveness of demand change the profit-maximising price and the financial disagreement between locally matched models?"
        values = sorted({r["e"] for r in rows})
        changed = "Starting elasticity e = " + ", ".join(_n(e) for e in values) + "; the baseline is e = " + _n(bases["linear"]["e"]) + "."
        held = common + "; " + ", ".join((cost_held, fixed_held, interval_held)) + ". Both models match quantity, slope and elasticity at p₀ within each scenario."
        theory = ("Before clipping or price bounds apply, increasing e reduces the linear cutoff "
                  "z = p₀(1+1/e), hence lowers the linear stationary price (z+c)/2. "
                  "For constant elasticity with e>1 and c>0, ec/(e−1) also falls as e increases. "
                  "For e≤1 profit rises throughout positive prices, so the bounded optimum is U. "
                  "The models share local starting information but have different curvature away from p₀.")
        equations += [r"v_L=\frac{p_0(1+1/e)+c}{2},\quad \frac{dv_L}{de}=-\frac{p_0}{2e^2}<0",
                      r"v_C=\frac{ec}{e-1},\quad \frac{dv_C}{de}=-\frac{c}{(e-1)^2}<0\quad(e>1,c>0)"]
        pairs = [(next(r for r in rows if r["e"] == e and r["model"] == "linear"),
                  next(r for r in rows if r["e"] == e and r["model"] == "constant_elasticity")) for e in values]
        gaps = "; ".join(f"e = {_n(left['e'])}: constant-elasticity price minus linear price "
                         f"{_signed_money(right['price']-left['price'])}, profit difference "
                         f"{_signed_money(right['profit']-left['profit'])}/week" for left, right in pairs)
        counts = {m: sum(r["boundary"] == "upper_boundary" for r in rows if r["model"] == m) for m in MODEL_LABELS}
        interpretation = (gaps + ". Across these " + str(len(values)) + " scenarios, the upper bound binds in "
                          f"{counts['linear']} linear and {counts['constant_elasticity']} constant-elasticity cases. "
                          "A matching quantity and slope at one price do not determine the whole curve: "
                          "linear demand reaches zero, while constant-elasticity demand remains positive at every finite price.")
        financial = ("The baseline comparison is " + _scenario_result(bases["linear"]) + "; " +
                     _scenario_result(bases["constant_elasticity"]) + ". A hypothetical business should treat "
                     "the gap as sensitivity to demand assumptions, rather than take either model's higher profit as established revenue potential. "
                     "A binding maximum price makes the permitted interval a material business assumption.")
        conclusion = (f"Within the tested range from e = {_n(values[0])} to e = {_n(values[-1])}, "
                      "each model's recommended price is non-increasing as elasticity rises. "
                      f"At e = {_n(bases['linear']['e'])}, the model price difference is "
                      f"{_money(bases['constant_elasticity']['price']-bases['linear']['price'])}; "
                      "the financial conclusion depends on demand curvature and any active price bound.")
        limitation = ("Elasticity is an assumed local input, not an estimate from sales data. "
                      "Both Q₀ and p₀ are held fixed when e changes; this compares hypothetical curves, "
                      "rather than proving a causal effect on real consumers. This own-price sensitivity "
                      "does not independently identify a substitution effect: no competitor-price or "
                      "compensated-demand model is established. A follow-up is to estimate "
                      "elasticity and curvature from observed prices and quantities over a plausible range.")
    elif key == "unit_cost":
        before, after = bases, others
        dc = after["linear"]["c"] - before["linear"]["c"]
        question = "How much of an increase in unit cost is passed into the profit-maximising selling price, and what happens to sales, revenue and profit?"
        changed = f"Unit cost c increases from {_money(before['linear']['c'])} to {_money(after['linear']['c'])} per unit (change {_money(dc)})."
        held = common + "; " + ", ".join((demand_held, fixed_held, interval_held)) + "."
        theory = ("On valid interior solutions, the linear price rises by half the unit-cost increase, "
                  "whereas the constant-elasticity price rises by e/(e−1) times that increase. "
                  "Re-optimising can protect some margin, but the higher price reduces quantity demanded; "
                  "a price increase alone does not show that profit improves.")
        equations += [r"\frac{dv_L}{dc}=\frac12,\qquad \frac{dv_C}{dc}=\frac{e}{e-1}\quad(e>1,c>0)"]
        parts = []
        for model in MODEL_LABELS:
            r, b = after[model], before[model]
            parts.append(f"{r['model_label']}: price {_money(b['price'])} → {_money(r['price'])} "
                         f"(change {_signed_money(r['price_change'])}; pass-through Δp/Δc = {_n(r['price_change']/dc)}), "
                         f"quantity {_quantity(b['quantity'])} → {_quantity(r['quantity'])} units/week "
                         f"(change {r['quantity_change']:+.4f}), revenue {_money(b['revenue'])} → {_money(r['revenue'])} "
                         f"(change {_signed_money(r['revenue_change'])}), and profit {_money(b['profit'])} → "
                         f"{_money(r['profit'])}/week (change {_signed_money(r['profit_change'])})")
        interpretation = "; ".join(parts) + ". Both stationary prices remain feasible, so the derivative pass-through formulas apply without a binding price bound."
        financial = ("The cost increase reduces optimised profit in both models, even though prices rise. "
                     "The constant-elasticity response sacrifices more volume because its optimal price adjustment is larger. "
                     "A hypothetical business would compare supplier savings, attainable margin and the risk of lost demand; "
                     "passing costs through to customers is constrained by their assumed responsiveness.")
        conclusion = (f"For this {_money(dc)} cost rise, the calculated optimal price rises by "
                      f"{_money(after['linear']['price_change'])} under linear demand and "
                      f"{_money(after['constant_elasticity']['price_change'])} under constant-elasticity demand. "
                      "The two locally matched demand curves therefore imply materially different pricing responses to the same cost pressure.")
        limitation = ("Unit cost is constant per unit, and demand is unchanged by the supplier cost shock. "
                      "Capacity, competitor responses and step changes in costs are excluded. The pass-through "
                      "derivatives apply only while their interior candidates remain valid and within the permitted interval.")
    elif key == "price_cap":
        before, after = bases, others
        question = "What is the financial effect of lowering the maximum permitted selling price while leaving demand and costs unchanged?"
        changed = f"Upper permitted price U falls from {_money(before['linear']['price_max'])} to {_money(after['linear']['price_max'])}."
        held = common + "; " + ", ".join((demand_held, cost_held, fixed_held)) + f", lower permitted price {_money(reference['price_min'])}."
        theory = ("Reducing the feasible set cannot increase its maximum attainable profit. "
                  "A cap above a model's original optimal price leaves that optimum available; "
                  "a cap below it can force a lower price, higher quantity and lower margin.")
        equations += [r"\widehat p_C=\min(U,\max(L,ec/(e-1)))\quad(e>1,c>0)",
                      r"[L,U_{new}]\subseteq[L,U_{old}]\;\Longrightarrow\;\max\pi_{new}\leq\max\pi_{old}"]
        parts = []
        for model in MODEL_LABELS:
            r, b = after[model], before[model]
            binding = "binds" if r["boundary"] == "upper_boundary" else "does not bind"
            parts.append(f"{r['model_label']}: the new cap {binding}; price {_money(b['price'])} → {_money(r['price'])}, "
                         f"quantity {_quantity(b['quantity'])} → {_quantity(r['quantity'])} units/week "
                         f"(change {r['quantity_change']:+.4f}), revenue {_money(b['revenue'])} → {_money(r['revenue'])} "
                         f"(change {_signed_money(r['revenue_change'])}), profit {_money(b['profit'])} → "
                         f"{_money(r['profit'])}/week (change {_signed_money(r['profit_change'])})")
        interpretation = "; ".join(parts) + ". The cap is tested against each model's original optimum, rather than assumed to affect both equally."
        ce = after["constant_elasticity"]
        financial = (f"Under constant-elasticity demand, lowering the cap costs {_money(-ce['profit_change'])} "
                     f"of weekly optimised profit while revenue changes by {_signed_money(ce['revenue_change'])}. "
                     "More revenue can accompany less profit because additional sales incur unit costs and the selling margin falls. "
                     "This distinction matters when assessing a regulated price, discount ceiling or internal pricing policy.")
        conclusion = (f"The linear optimum remains {_money(after['linear']['price'])}; the constant-elasticity optimum "
                      f"moves from {_money(before['constant_elasticity']['price'])} to {_money(ce['price'])}. "
                      "The same price restriction has different financial consequences because the demand curves imply different unconstrained optima.")
        limitation = ("The restriction changes only the permitted price interval. It does not model shortages, "
                      "quality changes, competitors or how a real business would respond outside pricing. "
                      "A follow-up is to compare several caps with capacity and minimum viable profit requirements.")
    elif key == "fixed_cost":
        before, after = bases, others
        df = after["linear"]["F"] - before["linear"]["F"]
        question = "Does a higher unavoidable fixed cost change the entire set of optimal operating prices, or only the resulting profit?"
        changed = f"Weekly fixed cost F rises from {_money(before['linear']['F'])} to {_money(after['linear']['F'])} (increase {_money(df)})."
        held = common + "; " + ", ".join((demand_held, cost_held, interval_held)) + "."
        theory = ("Subtracting the same additional fixed cost at every permitted price shifts the profit curve "
                  "down without changing which prices maximise it. The full optimal price set, demand, "
                  "revenue and contribution therefore remain the same, while operating profit falls by the fixed-cost increase.")
        equations += [r"\pi(p;F+\Delta F)=\pi(p;F)-\Delta F",r"\operatorname{argmax}_{p\in[L,U]}\pi(p;F+\Delta F)=\operatorname{argmax}_{p\in[L,U]}\pi(p;F)"]
        parts = []
        for model in MODEL_LABELS:
            r, b = after[model], before[model]
            parts.append(f"{r['model_label']}: optimal price set {_set_text(b['optimal_intervals'])} → "
                         f"{_set_text(r['optimal_intervals'])}; quantity {_quantity(b['quantity'])} → {_quantity(r['quantity'])} "
                         f"units/week; revenue {_money(b['revenue'])} → {_money(r['revenue'])}; contribution "
                         f"{_money(b['contribution'])} → {_money(r['contribution'])}; profit {_money(b['profit'])} → "
                         f"{_money(r['profit'])}/week (change {_signed_money(r['profit_change'])})")
        interpretation = "; ".join(parts) + ". The algebra establishes invariance of every tied maximiser as well as the displayed representative price."
        financial = ("Maximum contribution is also the fixed-cost level at which optimised operating profit becomes zero: "
                     + "; ".join(f"{r['model_label']} can cover {_money(r['contribution'])}/week of unavoidable fixed costs "
                                 "under these demand and variable-cost assumptions" for r in after.values()) +
                     ". A pricing optimum answers how best to operate within the model; it does not by itself establish whether operating or closing is the better business decision.")
        conclusion = (f"Increasing fixed cost by {_money(df)}/week reduces each model's optimised profit by "
                      f"{_money(df)}/week and preserves its entire optimal price set. "
                      "Fixed costs affect profitability and cost coverage, even when they do not change the optimal selling price.")
        limitation = ("Fixed costs are assumed unavoidable for the period, including when no units are sold. "
                      "A shutdown or investment decision needs separate information on avoidable costs, sunk costs and future periods; "
                      "it cannot be inferred from this pricing calculation alone.")
    else:
        before, after = bases, others
        question = "When unit cost exceeds the linear zero-demand cutoff, what prices minimise the operating loss, and how does the constant-elasticity model differ?"
        changed = f"Unit cost c rises from {_money(before['linear']['c'])} to {_money(after['linear']['c'])}/unit."
        held = common + f"; e = {_n(after['linear']['e'])}, F = {_money(after['linear']['F'])}/week, permitted prices {_money(after['linear']['price_min'])}–{_money(after['linear']['price_max'])}."
        p = Parameters(**{name: after["linear"][name] for name in Parameters.__dataclass_fields__})
        cutoff = zero_demand_price(p)
        theory = ("If linear demand is positive only below a cutoff that is already below unit cost, "
                  "every positive-demand price loses contribution. Any permitted zero-demand price avoids "
                  "that variable loss and ties at profit −F. Constant-elasticity demand has no finite zero-demand cutoff, "
                  "so it need not have this plateau.")
        equations += [r"c\geq z,\ p<z\;\Longrightarrow\;(p-c)Q_L(p)<0",r"p\geq z\;\Longrightarrow\;Q_L=0,\ \pi_L=-F"]
        linear, ce = after["linear"], after["constant_elasticity"]
        interpretation = (f"The calculated cutoff is {_money(cutoff)}, below unit cost {_money(p.c)}. "
                          f"Linear optimal prices form the complete interval {_set_text(linear['optimal_intervals'])}; "
                          f"the displayed {_money(linear['price'])} is only its smallest representative. "
                          f"Each of those prices gives zero demand, zero revenue, zero contribution and "
                          f"profit {_money(linear['profit'])}/week. Constant elasticity instead selects "
                          f"{_money(ce['price'])}, with {_quantity(ce['quantity'])} units/week, revenue "
                          f"{_money(ce['revenue'])}, contribution {_money(ce['contribution'])} and "
                          f"profit {_money(ce['profit'])}/week. " +
                          "Before-and-after comparison: " + "; ".join(
                              f"{after[m]['model_label']}: price {_money(before[m]['price'])} → {_money(after[m]['price'])}, "
                              f"quantity {_quantity(before[m]['quantity'])} → {_quantity(after[m]['quantity'])}, "
                              f"revenue {_money(before[m]['revenue'])} → {_money(after[m]['revenue'])}, "
                              f"profit {_money(before[m]['profit'])} → {_money(after[m]['profit'])}/week "
                              f"(change {_signed_money(after[m]['profit_change'])})" for m in MODEL_LABELS) + ".")
        financial = (f"The cost rise removes positive contribution at every permitted price in this example. "
                     f"Under linear demand, charging any price in {_set_text(linear['optimal_intervals'])} "
                     f"minimises the loss at the unavoidable fixed cost of {_money(p.F)}/week. "
                     f"Under constant-elasticity demand, the selected price equals unit cost {_money(p.c)}, "
                     "so sales exactly cover their variable cost and contribute nothing towards fixed costs. "
                     "The financial outcome is a loss even though a mathematically optimal price exists.")
        conclusion = (f"Both models' best operating profit is {_money(linear['profit'])}/week here, "
                      "but the mechanisms differ: a complete zero-demand price plateau for linear demand "
                      "versus positive sales at zero unit margin for constant-elasticity demand. "
                      "A single displayed price would conceal the linear model's set of equally good solutions.")
        limitation = ("Zero sales do not remove unavoidable fixed costs in this model. "
                      "Whether to stop trading, change suppliers or redesign the product requires costs and alternatives "
                      "outside the permitted-price calculation. Demand far from the reference price also needs empirical validation.")
    return dict(key=key, title=INVESTIGATION_LABELS[key], question=question, changed=changed,
                held=held, theory=theory, equations=equations, rows=rows,
                workings=[_workings(row) for row in rows], interpretation=interpretation,
                financial_implications=financial, conclusion=conclusion, limitation=limitation)


def _table(rows, columns):
    return "\n".join(["| " + " | ".join(label for _, label, _ in columns) + " |",
                       "| " + " | ".join("---" for _ in columns) + " |"] +
                      ["| " + " | ".join(fmt(row[key]).replace("|", "\\|") for key, _, fmt in columns) + " |" for row in rows])


def _risk_sections(params, period="week"):
    rows = model_risk_rows(params, period)
    sections = [
        "## Model-dependent pricing risk",
        "Each curve supplies a candidate price; both curves then evaluate that same decision over "
        "the shared permitted interval. Lost model-implied profit (regret) is "
        "maxₓ∈[L,U] πₘ(x) − πₘ(p). This compares hypothetical assumptions and does not assign "
        "probabilities or establish which curve describes customers.",
        _table(rows, [("candidate_source_label", "Price suggested by", str),
                      ("candidate_optimal_intervals", "Source model's full optimal set", _set_text),
                      ("candidate_price", "Price evaluated", _money),
                      ("evaluated_model_label", "Demand assumed", str),
                      ("profit", f"Profit/{period}", _money),
                      ("max_profit", f"Model maximum/{period}", _money),
                      ("regret", f"Lost profit/{period}", _money)]),
    ]
    for row in rows:
        if row["candidate_source"] != row["evaluated_model"]:
            sections.append(
                f"Charging {_money(row['candidate_price'])}, the {row['candidate_source_label'].lower()} "
                f"recommendation, under {row['evaluated_model_label'].lower()} demand gives profit "
                f"{_money(row['profit'])}/{period}, {_money(row['regret'])} below that curve's "
                f"{_money(row['max_profit'])}/{period} maximum."
            )
    sections.append(
        "Where an optimal set is tied, the evaluated candidate is its smallest price; the full set "
        "is reported and another member can have a different consequence under the other curve. "
        "Regret is calculated from unrounded contribution differences, equivalent to profit differences "
        "because the same fixed cost cancels. Only floating-point roundoff near zero is removed."
    )
    return sections


def summary_markdown():
    """Concise generated findings, retaining the benchmark assumptions and caveats."""
    params = Parameters()
    benchmark = [asdict(analytical_optimum(model, params)) | {"model_label": label}
                 for model, label in MODEL_LABELS.items()]
    sections = [
        "# Project Findings Summary",
        "How does the assumed relationship between price and quantity demanded affect the "
        "profit-maximising price? The two hypothetical demand curves match starting quantity, "
        "slope and elasticity but differ away from the starting price.",
        "## Benchmark",
        f"p₀ = {_money(params.p0)}, Q₀ = {_quantity(params.Q0)} units/week, e = {_n(params.e)}, "
        f"c = {_money(params.c)}/unit, F = {_money(params.F)}/week; "
        f"permitted prices [{_money(params.price_min)}, {_money(params.price_max)}]. "
        f"At the starting price each curve gives profit {_money(evaluate('linear', params.p0, params)['profit'])}/week.",
        _table(benchmark, [("model_label", "Model", str), ("optimal_intervals", "Optimal price set", _set_text),
                           ("quantity", "Units/week", _quantity), ("revenue", "Revenue/week", _money),
                           ("profit", "Profit/week", _money)]),
        "## Controlled sensitivities",
    ]
    for key in ("unit_cost", "price_cap", "fixed_cost"):
        item = build_investigation(key)
        changed_rows = [row for row in item["rows"] if "(baseline)" not in row["scenario"]]
        financial = "; ".join(
            f"{row['model_label']} profit {_money(row['profit'])}/week "
            f"(change {_signed_money(row['profit_change'])}/week)" for row in changed_rows)
        sections.append(f"**{item['title']}.** {item['changed']} {item['conclusion']} "
                        f"At the revised inputs: {financial}.")
    sections += _risk_sections(params)
    ce_revenue = revenue_optimum("constant_elasticity", params)
    sections += [
        "## Conditional conclusion and limitations",
        "The same local demand information supports different optimal prices. The financial result "
        "depends on curvature, costs and permitted prices; the larger model-implied profit does not "
        "prove that its demand assumption is better. All five complete investigations, derivations "
        "and limitations remain in investigation_worksheet.md.",
        f"The constant-elasticity revenue objective selects {_money(ce_revenue['price'])} and implies "
        f"{_quantity(ce_revenue['quantity'])} units/week, with profit {_money(ce_revenue['profit'])}/week. "
        "This extreme volume exposes extrapolation and absent capacity constraints; it is not an "
        "established sales forecast. Own-price sensitivity does not independently identify a "
        "substitution effect. Real customer data, empirical demand checks and operational constraints "
        "would be needed for a commercial decision.",
        "## Methodology", METHODOLOGY,
    ]
    return "\n\n".join(sections) + "\n"


def report_markdown(keys=None):
    """Complete deterministic report, or a complete report for selected sections."""
    keys = investigation_keys() if keys is None else ((keys,) if isinstance(keys, str) else tuple(keys))
    if not keys:
        raise ValueError("Choose at least one investigation.")
    investigations = [build_investigation(key) for key in keys]
    params = Parameters()
    benchmark = [asdict(analytical_optimum(model, params)) | {"model_label": label}
                 for model, label in MODEL_LABELS.items()]
    sections = [
        "# Complete Mathematical Investigation and Findings",
        "## Purpose and scope",
        "How do demand assumptions, costs and price restrictions affect a hypothetical business's "
        "revenue and operating profit? This investigation compares two demand functions matched at "
        "the same starting price, quantity, slope and elasticity. It calculates their complete "
        "profit-maximising price sets on a shared permitted interval and tests the financial sensitivity "
        "of those conclusions. These are conditional model results, not forecasts established from customer data.",
        "## Starting assumptions and financial definitions",
        f"The benchmark is p₀ = {_money(params.p0)}, Q₀ = {_quantity(params.Q0)} units/week, "
        f"e = {_n(params.e)}, c = {_money(params.c)}/unit, F = {_money(params.F)}/week and "
        f"p ∈ [{_money(params.price_min)}, {_money(params.price_max)}]. "
        "Prices are continuous and quantity can be fractional. Costs and demand use a consistent weekly period. "
        "Both models have Q(p₀)=Q₀ and Q′(p₀)=−eQ₀/p₀; the linear curve's point elasticity "
        "varies with price below its cutoff, whereas constant-elasticity demand keeps elasticity e.",
        r"$$R(p)=pQ(p),\quad VC(p)=cQ(p),\quad TC(p)=cQ(p)+F,\quad \pi(p)=(p-c)Q(p)-F.$ $".replace("$ $", "$$"),
        "Contribution is revenue less variable cost: (p−c)Q. It is available to cover fixed costs. "
        "A positive contribution can coexist with an operating loss; when Q=0, unavoidable fixed costs remain payable and π=−F.",
        "### Benchmark profit maxima",
        _table(benchmark, [("model_label", "Demand model", str), ("optimal_intervals", "Optimal price set", _set_text),
                           ("quantity", "Units/week", _quantity), ("revenue", "Revenue/week", _money),
                           ("total_cost", "Total cost/week", _money), ("profit", "Profit/week", _money)]),
    ]
    test_price = analytical_optimum("constant_elasticity", params).price
    sections += [
        "## Starting, chosen and profit-optimal price comparison",
        f"For this reproducible example the chosen test price is {_money(test_price)}, "
        "the constant-elasticity optimum. The live app allows any test price in the permitted interval. "
        "Each change is relative to that same curve's starting-price profit. Percentages are only "
        "reported when starting profit is positive; no percentage is assigned to a zero or negative baseline.",
        _table(chosen_price_rows(params, test_price),
               [("model_label", "Demand model", str), ("scenario", "Price choice", str),
                ("price", "Price", _money), ("quantity", "Units/week", _quantity),
                ("revenue", "Revenue/week", _money), ("variable_cost", "Variable cost/week", _money),
                ("contribution", "Contribution/week", _money), ("profit", "Profit/week", _money),
                ("profit_change", "Δ profit/week", _signed_money),
                ("profit_change_percent", "Δ profit (%)", lambda n: "Not meaningful" if n is None else f"{n:+.4f}%")]),
    ]
    sections += _risk_sections(params)
    sections += [
        "## Marginal revenue equals marginal cost: applicable interior checks",
        "For differentiable demand with Q′(p) ≠ 0, marginal revenue is MR = p + Q/Q′ "
        "and marginal cost is MC = c. At a differentiable interior positive-demand stationary "
        "profit maximum, π′(p) = Q + (p−c)Q′ = Q′(MR−MC) = 0, so MR = MC. "
        "The equality is not required at a binding boundary, a cutoff or a flat zero-demand "
        "region; those cases need endpoint or complete-set comparisons instead.",
    ]
    for model, label in MODEL_LABELS.items():
        check = mr_mc_check(model, params)
        if check["applicable"] and check["marginal_revenue"] is not None:
            sections.append(f"At the benchmark {label.lower()} optimum {_money(check['price'])}, "
                            f"MR = {_money(check['marginal_revenue'])}/unit and "
                            f"MC = {_money(check['marginal_cost'])}/unit. {check['explanation']}")
        else:
            sections.append(f"{label}: {check['explanation']}")
    sections += [
        "## Revenue maximisation versus profit maximisation",
        "Revenue rewards sales receipts. Profit deducts the costs of generating those sales. "
        "On the positive-demand linear segment, R=ap−bp², R′=a−2bp and R″=−2b<0, "
        "so the stationary revenue price is z/2, subject to the price interval and cutoff. "
        "For constant elasticity, R=Kp^(1−e) and R′=K(1−e)p^(−e): revenue falls with price "
        "when e>1, is constant when e=1, and rises when e<1. Endpoints and any complete tie set are included.",
    ]
    objective_rows = []
    for model, label in MODEL_LABELS.items():
        profit = analytical_optimum(model, params)
        revenue = revenue_optimum(model, params)
        for objective, result in (("Maximum profit", asdict(profit)), ("Maximum revenue", revenue)):
            objective_rows.append(result | {"model_label": label, "objective": objective})
        sections.append(
            f"For {label.lower()} demand, the revenue optimum is {_set_text(revenue['optimal_intervals'])}, "
            f"giving {_quantity(revenue['quantity'])} units/week, revenue {_money(revenue['revenue'])} "
            f"and profit {_money(revenue['profit'])}/week. The profit optimum is "
            f"{_set_text(profit.optimal_intervals)}, giving revenue {_money(profit.revenue)} and "
            f"profit {_money(profit.profit)}/week. Choosing the revenue objective increases revenue by "
            f"{_money(revenue['revenue']-profit.revenue)} but reduces profit by "
            f"{_money(profit.profit-revenue['profit'])}/week."
        )
    sections.append(_table(objective_rows, [("model_label", "Model", str), ("objective", "Objective", str),
                                            ("optimal_intervals", "Optimal price set", _set_text),
                                            ("quantity", "Units/week", _quantity), ("revenue", "Revenue/week", _money),
                                            ("total_cost", "Total cost/week", _money), ("profit", "Profit/week", _money)]))
    sections.append("The benchmark therefore shows why sales volume or revenue alone is an incomplete "
                    "pricing target: additional units can carry costs that outweigh their additional receipts. "
                    "For tied revenue optima in other input cases, the smallest reported price is only a "
                    "representative; compare profit within the whole revenue-optimal set before making a decision.")
    ce_revenue = revenue_optimum("constant_elasticity", params)
    sections.append(f"At the constant-elasticity benchmark revenue optimum {_money(ce_revenue['price'])}, "
                    f"the assumed curve predicts {_quantity(ce_revenue['quantity'])} units/week. "
                    "That extreme quantity follows from extrapolating the curve to the lower permitted boundary "
                    "with no capacity constraint. It is not an established sales forecast; the associated "
                    f"profit {_money(ce_revenue['profit'])}/week also shows why revenue alone is an incomplete objective.")
    for index, item in enumerate(investigations, 1):
        sections += [f"## {index}. {item['title']}", "### Economic question", item["question"],
                     "### Starting assumptions and variables", "Changed: " + item["changed"],
                     "Held constant: " + item["held"], "### Theoretical prediction", item["theory"],
                     "### Mathematical reasoning"]
        sections += ["$$\n" + equation + "\n$$" for equation in item["equations"]]
        sections += ["### Calculated results and before-and-after comparison",
                     _table(item["rows"], [("scenario", "Scenario", str), ("model_label", "Demand model", str),
                                           ("optimal_intervals", "Optimal price set", _set_text),
                                           ("quantity", "Units/week", _quantity), ("revenue", "Revenue/week", _money),
                                           ("total_cost", "Total cost/week", _money), ("profit", "Profit/week", _money)]),
                     "### Changes from each model's baseline",
                     _table(item["rows"], [("scenario", "Scenario", str), ("model_label", "Demand model", str),
                                           ("price_change", "Δ price", _signed_money),
                                           ("quantity_change", "Δ units/week", lambda n: f"{n:+.4f}"),
                                           ("revenue_change", "Δ revenue/week", _signed_money),
                                           ("profit_change", "Δ profit/week", _signed_money)]),
                     "Calculations use unrounded values. Currency is displayed to two decimal places and "
                     "quantity to four where needed. An interval denotes every equally optimal price; "
                     "the displayed financial quantities use its smallest representative.",
                     "### Worked calculations"]
        for working in item["workings"]:
            sections.append(f"#### {MODEL_LABELS[working['model']]} — {working['scenario']}")
            sections.append("\n".join(f"{i}. {step}" for i, step in enumerate(working["steps"], 1)))
        sections += ["### Interpretation of findings", item["interpretation"],
                     "### Financial implications", item["financial_implications"],
                     "### Conclusion", item["conclusion"],
                     "### Limitations and further investigation", item["limitation"]]
    sections += [
        "## Overall financial assessment",
        "The appropriate selling price depends on the chosen objective, the full assumed demand "
        "curve, unit costs and permitted prices. Local agreement at the starting price is not enough "
        "to guarantee the same financial recommendation. Unit-cost changes affect the marginal "
        "trade-off between margin and quantity; unavoidable fixed costs affect cost coverage but "
        "do not alter any maximising operating price. A binding price restriction can lower profit "
        "even when it increases sales revenue. Reporting full tied sets avoids suggesting a unique "
        "answer when the mathematics produces a plateau.",
        "The next commercially useful step is to collect price and sales evidence, estimate demand "
        "over a credible range, include uncertainty and realistic capacity or cost constraints, and "
        "compare model recommendations under those alternatives. Simulated maxima do not establish "
        "how real customers or competitors will behave.",
        "## Methodology", METHODOLOGY,
    ]
    return "\n\n".join(sections) + "\n"
