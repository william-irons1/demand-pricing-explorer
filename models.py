"""Matched hypothetical demand models on a shared, closed price interval.

Quantities are continuous. Profit includes unavoidable fixed cost even when
quantity is zero; a separate shutdown decision is outside this project.
"""

from dataclasses import asdict, dataclass, replace
import math
from numbers import Real

from scipy.optimize import minimize_scalar


MODEL_LABELS = {"linear": "Linear", "constant_elasticity": "Constant elasticity"}


def _number(name: str, value: float, *, positive: bool = True) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite real number.")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite.")
    if positive and value <= 0:
        raise ValueError(f"{name} must be greater than zero.")
    if not positive and value < 0:
        raise ValueError(f"{name} must be zero or greater.")
    return value


@dataclass(frozen=True)
class Parameters:
    """Shared demand assumptions and an economic interval, not a graph range."""

    p0: float = 10.0
    Q0: float = 100.0
    e: float = 2.0
    c: float = 6.0
    F: float = 0.0
    price_min: float = 1.0
    price_max: float = 15.0

    def __post_init__(self) -> None:
        for name in ("p0", "Q0", "e", "price_min", "price_max"):
            object.__setattr__(self, name, _number(name, getattr(self, name)))
        for name in ("c", "F"):
            object.__setattr__(self, name, _number(name, getattr(self, name), positive=False))
        if self.price_max <= self.price_min:
            raise ValueError("price_max must be greater than price_min.")


@dataclass(frozen=True)
class Optimum:
    model: str
    price: float
    quantity: float
    revenue: float
    variable_cost: float
    total_cost: float
    contribution: float
    profit: float
    boundary: str
    warning: str | None
    optimal_intervals: tuple[tuple[float, float], ...]


def _check_model(model: str) -> None:
    if model not in MODEL_LABELS:
        raise ValueError(f"Unknown demand model {model!r}; choose {tuple(MODEL_LABELS)}.")


def _finite_result(name: str, value: float) -> float:
    if not math.isfinite(value):
        raise ValueError(f"{name} exceeds floating-point range; use smaller inputs.")
    return value


def zero_demand_price(params: Parameters) -> float:
    """Cutoff a/b; linear demand is zero at and above this positive price."""
    return _finite_result("Linear zero-demand cutoff", params.p0 * (1.0 + 1.0 / params.e))


def _price(model: str, p: float) -> float:
    _check_model(model)
    return _number("Price", p)


def _log_ratio(numerator: float, denominator: float) -> float:
    relative_difference = (numerator - denominator) / denominator
    if math.isfinite(relative_difference) and relative_difference > -1:
        return math.log1p(relative_difference)
    return math.log(numerator) - math.log(denominator)


def demand(model: str, p: float, params: Parameters) -> float:
    """Evaluate at any positive price; optimisation alone uses the interval."""
    p = _price(model, p)
    if p == params.p0:
        return params.Q0
    if model == "linear":
        if p >= zero_demand_price(params):
            return 0.0
        quantity = params.Q0 * (1.0 - params.e * (p / params.p0 - 1.0))
        return max(0.0, _finite_result("Quantity", quantity))
    try:
        # Combining logs avoids overflowing an intermediate power unnecessarily.
        quantity = math.exp(math.log(params.Q0) - params.e * _log_ratio(p, params.p0))
    except OverflowError as error:
        raise ValueError("Quantity exceeds floating-point range; use smaller inputs.") from error
    return _finite_result("Quantity", quantity)


def slope(model: str, p: float, params: Parameters) -> float:
    """dQ/dp; the clipped linear curve has a corner at its cutoff."""
    p = _price(model, p)
    if model == "linear":
        cutoff = zero_demand_price(params)
        if p == cutoff:
            raise ValueError("Linear slope is undefined at the zero-demand cutoff (a corner).")
        if p > cutoff:
            return 0.0
        return _finite_result("Demand slope", -params.e * (params.Q0 / params.p0))
    return _finite_result("Demand slope", -params.e * (demand(model, p, params) / p))


def elasticity(model: str, p: float, params: Parameters) -> float:
    """Positive magnitude -pQ'/Q, undefined on the linear zero-demand plateau."""
    p = _price(model, p)
    if model == "constant_elasticity":
        return params.e
    quantity = demand(model, p, params)
    if quantity == 0:
        raise ValueError("Linear elasticity is undefined at zero demand.")
    return _finite_result("Elasticity", -slope(model, p, params) * (p / quantity))


def evaluate(model: str, p: float, params: Parameters) -> dict[str, float]:
    """Financial quantities, even for a hypothetical price outside the interval."""
    p = _price(model, p)
    quantity = demand(model, p, params)
    revenue = _finite_result("Revenue", p * quantity)
    variable_cost = _finite_result("Variable cost", params.c * quantity)
    total_cost = _finite_result("Total cost", variable_cost + params.F)
    contribution = _finite_result("Contribution", (p - params.c) * quantity)
    profit = _finite_result("Profit", contribution - params.F)
    return dict(price=p, quantity=quantity, revenue=revenue, variable_cost=variable_cost,
                total_cost=total_cost, contribution=contribution, profit=profit)


def _result(model: str, intervals: tuple[tuple[float, float], ...], params: Parameters) -> Optimum:
    # Exact structural ties are represented as sets, not guessed from close floats.
    price = min(lo for lo, _ in intervals)
    multiple = any(lo < hi for lo, hi in intervals) or len(intervals) > 1
    boundary = ("multiple" if multiple else "lower_boundary" if price == params.price_min
                else "upper_boundary" if price == params.price_max else "interior")
    values = evaluate(model, price, params)
    warnings = []
    if multiple:
        warnings.append("Multiple permitted prices are equally optimal; the smallest is shown as a representative.")
    elif boundary == "lower_boundary":
        warnings.append("The maximum occurs at the lower permitted boundary; compare with the unrestricted result.")
    elif boundary == "upper_boundary":
        warnings.append("The maximum occurs at the upper permitted boundary; compare with the unrestricted result.")
    if values["contribution"] <= 0:
        warnings.append("No permitted price gives a positive contribution towards fixed costs.")
    if model == "linear" and values["quantity"] == 0:
        warnings.append("Zero demand means profit is −F, because fixed cost remains payable.")
    return Optimum(model=model, **values, boundary=boundary, warning=" ".join(warnings) or None,
                   optimal_intervals=intervals)


def _linear_plateau(params: Parameters) -> tuple[tuple[float, float], ...] | None:
    cutoff = zero_demand_price(params)
    if params.price_min >= cutoff:
        return ((params.price_min, params.price_max),)
    if params.c >= cutoff and params.price_max >= cutoff:
        return ((cutoff, params.price_max),)
    return None


def _smallest_best(candidates, objective) -> float:
    """Always inspect endpoints; exact objective ties prefer the smaller price."""
    return min(sorted(set(candidates)), key=objective)


def analytical_optimum(model: str, params: Parameters) -> Optimum:
    """Compare feasible candidates, interval boundaries, and any optimal plateau."""
    _check_model(model)
    lower, upper = params.price_min, params.price_max
    if model == "linear":
        plateau = _linear_plateau(params)
        if plateau is not None:
            return _result(model, plateau, params)
        cutoff = zero_demand_price(params)
        candidates = [lower, upper]
        stationary = cutoff / 2.0 + params.c / 2.0
        if lower <= stationary <= min(upper, cutoff):
            candidates.append(stationary)
        if lower <= cutoff <= upper:
            candidates.append(cutoff)
        # F is deliberately omitted: it cannot alter the set of maximizing prices.
        price = _smallest_best(candidates, lambda p: -evaluate(model, p, params)["contribution"])
    elif params.c == 0:
        if params.e == 1:
            return _result(model, ((lower, upper),), params)
        price = lower if params.e > 1 else upper
    elif params.e <= 1:
        price = upper
    else:
        stationary = params.c * (1.0 + 1.0 / (params.e - 1.0))
        price = max(lower, min(upper, stationary))
    return _result(model, ((price, price),), params)


def _minimise(objective, lower: float, upper: float):
    result = minimize_scalar(objective, bounds=(lower, upper), method="bounded",
                             options={"xatol": 1e-12, "maxiter": 1000})
    if not result.success:
        raise RuntimeError(f"Numerical optimisation failed: {result.message}")
    return result


def _log_positive_contribution(t: float, e: float) -> float:
    """Log of (exp(t)-1)exp(-et), with a positive price-independent factor removed."""
    if t <= 0:
        return -math.inf
    if t < math.log(2.0):
        return math.log(math.expm1(t)) - e * t
    return (1.0 - e) * t + math.log1p(-math.exp(-t))


def numerical_optimum(model: str, params: Parameters) -> Optimum:
    """Independent SciPy search, explicit endpoints, and exact flat-region checks.

    No analytical stationary-price candidate seeds the search. Maximising
    contribution (or a monotone log transform) avoids cancellation from large F.
    The linear positive-demand piece is concave; the CE objective is unimodal
    or monotone. These facts justify bounded search rather than a coarse grid.
    """
    _check_model(model)
    lower, upper = params.price_min, params.price_max
    if model == "linear":
        cutoff = zero_demand_price(params)
        if lower >= cutoff:
            return _result(model, ((lower, upper),), params)
        positive_upper = min(upper, cutoff)
        ratio = params.c / cutoff
        scale = max(1.0, ratio)

        def objective(p):
            x = p / cutoff
            # Same quadratic as -contribution, with constants and scale removed.
            return x * (x / scale - (1.0 + ratio) / scale)

        solution = _minimise(lambda u: objective(lower + u * (positive_upper - lower)), 0.0, 1.0)
        candidates = [lower, positive_upper, lower + solution.x * (positive_upper - lower)]
        price = _smallest_best(candidates, objective)
        # The flat piece has zero contribution. Its exact conditions identify
        # ties without using rounded profit comparisons or the analytical solver.
        if params.c >= cutoff and upper >= cutoff:
            return _result(model, ((cutoff, upper),), params)
        return _result(model, ((price, price),), params)

    if params.c == 0:
        if params.e == 1:
            return _result(model, ((lower, upper),), params)
        log_lower, log_upper = math.log(lower), math.log(upper)
        objective = lambda p: (params.e - 1.0) * math.log(p)
        solution = _minimise(lambda t: (params.e - 1.0) * t, log_lower, log_upper)
        price = _smallest_best([lower, upper, math.exp(solution.x)], objective)
        return _result(model, ((price, price),), params)

    if upper <= params.c:
        # Contributions are non-positive and increase over this whole region.
        # Minimise their log loss, checking the exact permitted endpoints.
        def objective(p):
            t = _log_ratio(p, params.c)
            return -math.inf if t >= 0 else math.log(-math.expm1(t)) - params.e * t

        solution = _minimise(lambda u: objective(lower + u * (upper - lower)), 0.0, 1.0)
        price = _smallest_best([lower, upper, lower + solution.x * (upper - lower)], objective)
        return _result(model, ((price, price),), params)

    # Any feasible p>c gives positive contribution and beats every p<=c.
    positive_lower = max(lower, params.c)
    t_lower, t_upper = _log_ratio(positive_lower, params.c), _log_ratio(upper, params.c)
    objective = lambda p: -_log_positive_contribution(_log_ratio(p, params.c), params.e)
    solution = _minimise(lambda t: -_log_positive_contribution(t, params.e), t_lower, t_upper)
    try:
        price = math.exp(math.log(params.c) + solution.x)
    except OverflowError as error:
        raise ValueError("Numerical price exceeds floating-point range; use smaller inputs.") from error
    price = min(upper, max(positive_lower, price))
    price = _smallest_best([positive_lower, upper, price], objective)
    return _result(model, ((price, price),), params)


def mr_mc_check(model: str, params: Parameters, optimum: Optimum | None = None) -> dict:
    """Check MR = p + Q/Q' = c only for a unique interior operating optimum.

    Dividing the profit first-order condition by nonzero Q' gives MR = MC.
    Boundaries, the linear corner and flat optimal sets need separate reasoning.
    An optional independently searched optimum may be checked without replacing
    its price with the analytical answer.
    """
    _check_model(model)
    optimum = analytical_optimum(model, params) if optimum is None else optimum
    if optimum.model != model:
        raise ValueError("The optimum must belong to the requested demand model.")
    price = optimum.price
    quantity = demand(model, price, params)
    result = dict(applicable=False, status="not_applicable", price=price,
                  marginal_revenue=None, marginal_cost=params.c, difference=None,
                  equal=None, explanation="")
    if model == "linear" and price >= zero_demand_price(params):
        if price == zero_demand_price(params):
            result["explanation"] = (
                "The representative price is the linear zero-demand cutoff, where the "
                "demand curve has a corner and Q′ is undefined. Check the cutoff and "
                "the complete optimal set; MR = MC is not required.")
        else:
            result["explanation"] = (
                "The optimum is on the flat zero-demand region: Q = Q′ = 0, so "
                "Q/Q′ and marginal revenue are undefined. Profit is −F throughout "
                "the permitted plateau; MR = MC is not required.")
        return result
    if optimum.boundary == "multiple" or len(optimum.optimal_intervals) > 1 or any(
            lo < hi for lo, hi in optimum.optimal_intervals):
        result["explanation"] = (
            "Profit is flat over a set of equally optimal prices. In the "
            "constant-elasticity case e = 1, c = 0, MR = MC = 0 holds throughout, "
            "but it does not identify a unique interior maximum.")
        return result
    if not params.price_min < price < params.price_max:
        result["explanation"] = (
            "The permitted price boundary binds. A constrained maximum need not "
            "have a zero profit derivative or MR = MC; compare feasible endpoints "
            "and the unrestricted result.")
        return result
    try:
        derivative = slope(model, price, params)
        if quantity <= 0 or derivative == 0:
            raise ValueError("Positive demand and a nonzero demand slope cannot be resolved at floating-point precision.")
        quantity_term = quantity / derivative
        marginal_revenue = _finite_result("Marginal revenue", price + quantity_term)
        difference = _finite_result("MR − MC", marginal_revenue - params.c)
    except ValueError as error:
        result.update(status="unavailable", explanation=f"MR = MC check unavailable: {error}")
        return result
    # A separate bounded search can differ from the stationary price by a few
    # floating-point units. Scale the residual by its terms, not rounded profit.
    tolerance = 1e-7 * max(abs(price), abs(quantity_term), abs(params.c)) + 1e-10
    equal = abs(difference) <= tolerance
    result.update(applicable=True, status="verified" if equal else "check_failed",
                  marginal_revenue=marginal_revenue, difference=difference, equal=equal,
                  explanation=("At this differentiable interior maximum with positive demand, "
                               "MR = p + Q/Q′ agrees with MC = c within numerical tolerance."
                               if equal else
                               "At this differentiable interior candidate with positive demand, "
                               "MR = p + Q/Q′ does not agree with MC = c within numerical tolerance."))
    return result


def unconstrained_summary(model: str, params: Parameters) -> dict:
    """Classify the separate problem over every strictly positive price."""
    _check_model(model)
    if model == "linear":
        cutoff = zero_demand_price(params)
        if params.c >= cutoff:
            return dict(status="multiple", price=cutoff, optimal_from=cutoff, optimal_to=math.inf,
                        explanation="Every price at or above the zero-demand cutoff is equally optimal: "
                                    "quantity is zero and profit is −F. Positive-demand prices do worse.")
        price = cutoff / 2.0 + params.c / 2.0
        return dict(status="unique", price=price, optimal_from=price, optimal_to=price,
                    explanation="The positive-demand profit quadratic is strictly concave, and its "
                                "stationary maximum beats the zero-demand plateau.")
    if params.e == 1 and params.c == 0:
        return dict(status="multiple", price=None, optimal_from=0.0, optimal_to=math.inf,
                    explanation="Every strictly positive price is equally optimal: revenue and profit "
                                "are constant. The lower endpoint 0 is open; there is no smallest price.")
    if params.e > 1 and params.c > 0:
        price = _finite_result("Unconstrained optimal price", params.c * (1.0 + 1.0 / (params.e - 1.0)))
        return dict(status="unique", price=price, optimal_from=price, optimal_to=price,
                    explanation="The profit derivative changes from positive to negative at ec/(e−1), "
                                "giving a unique maximum over all positive prices.")
    if params.e == 1:
        explanation = ("Profit increases towards the finite supremum Q₀p₀−F as price tends to infinity; "
                       "no finite price attains it when unit cost is positive.")
    elif params.e < 1:
        explanation = "Profit grows without bound as price tends to infinity; no finite price maximises it."
    else:
        explanation = ("With zero unit cost and e>1, profit grows without bound as price tends to 0 "
                       "from above; 0 is excluded and no finite positive price maximises it.")
    return dict(status="no_finite_maximum", price=None, optimal_from=None, optimal_to=None,
                explanation=explanation)


def sensitivity_rows(investigation: str) -> list[dict]:
    """Reset to the benchmark, changing just one assumption at each step."""
    scenarios = {
        "elasticity": [(f"e = {e:g}" + (" (baseline)" if e == 2 else ""), {"e": e})
                       for e in (0.5, 1.0, 1.5, 2.0, 3.0)],
        "unit_cost": [("c = £6 (baseline)", {"c": 6.0}), ("c = £7", {"c": 7.0})],
        "fixed_cost": [("F = £0 (baseline)", {"F": 0.0}), ("F = £50", {"F": 50.0})],
        "price_cap": [("Upper price £15 (baseline)", {"price_max": 15.0}),
                      ("Upper price £11", {"price_max": 11.0})],
    }
    if investigation not in scenarios:
        raise ValueError(f"Unknown investigation {investigation!r}; choose {tuple(scenarios)}.")
    defaults = Parameters()
    baseline = {model: analytical_optimum(model, defaults) for model in MODEL_LABELS}
    rows = []
    for scenario, changes in scenarios[investigation]:
        params = replace(defaults, **changes)
        for model, label in MODEL_LABELS.items():
            optimum = analytical_optimum(model, params)
            summary = unconstrained_summary(model, params)
            rows.append(dict(investigation=investigation, scenario=scenario,
                             **asdict(params), **asdict(optimum), model_label=label,
                             baseline_price=baseline[model].price,
                             baseline_profit=baseline[model].profit,
                             price_change=optimum.price - baseline[model].price,
                             profit_change=optimum.profit - baseline[model].profit,
                             unconstrained_status=summary["status"],
                             unconstrained_explanation=summary["explanation"]))
    return rows
