# Project Findings Summary

How does the assumed relationship between price and quantity demanded affect the profit-maximising price? The two hypothetical demand curves match starting quantity, slope and elasticity but differ away from the starting price.

## Benchmark

p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £6.00/unit, F = £0.00/week; permitted prices [£1.00, £15.00]. At the starting price each curve gives profit £400.00/week.

| Model | Optimal price set | Units/week | Revenue/week | Profit/week |
| --- | --- | --- | --- | --- |
| Linear | £10.50 | 90 | £945.00 | £405.00 |
| Constant elasticity | £12.00 | 69.4444 | £833.33 | £416.67 |

## Controlled sensitivities

**Unit cost and margin.** Unit cost c increases from £6.00 to £7.00 per unit (change £1.00). For this £1.00 cost rise, the calculated optimal price rises by £0.50 under linear demand and £2.00 under constant-elasticity demand. The two locally matched demand curves therefore imply materially different pricing responses to the same cost pressure. At the revised inputs: Linear profit £320.00/week (change −£85.00/week); Constant elasticity profit £357.14/week (change −£59.52/week).

**Price restrictions.** Upper permitted price U falls from £15.00 to £11.00. The linear optimum remains £10.50; the constant-elasticity optimum moves from £12.00 to £11.00. The same price restriction has different financial consequences because the demand curves imply different unconstrained optima. At the revised inputs: Linear profit £405.00/week (change £0.00/week); Constant elasticity profit £413.22/week (change −£3.44/week).

**Fixed cost and operating profit.** Weekly fixed cost F rises from £0.00 to £50.00 (increase £50.00). Increasing fixed cost by £50.00/week reduces each model's optimised profit by £50.00/week and preserves its entire optimal price set. Fixed costs affect profitability and cost coverage, even when they do not change the optimal selling price. At the revised inputs: Linear profit £355.00/week (change −£50.00/week); Constant elasticity profit £366.67/week (change −£50.00/week).

## Model-dependent pricing risk

Each curve supplies a candidate price; both curves then evaluate that same decision over the shared permitted interval. Lost model-implied profit (regret) is maxₓ∈[L,U] πₘ(x) − πₘ(p). This compares hypothetical assumptions and does not assign probabilities or establish which curve describes customers.

| Price suggested by | Source model's full optimal set | Price evaluated | Demand assumed | Profit/week | Model maximum/week | Lost profit/week |
| --- | --- | --- | --- | --- | --- | --- |
| Linear | £10.50 | £10.50 | Linear | £405.00 | £405.00 | £0.00 |
| Linear | £10.50 | £10.50 | Constant elasticity | £408.16 | £416.67 | £8.50 |
| Constant elasticity | £12.00 | £12.00 | Linear | £360.00 | £405.00 | £45.00 |
| Constant elasticity | £12.00 | £12.00 | Constant elasticity | £416.67 | £416.67 | £0.00 |

Charging £10.50, the linear recommendation, under constant elasticity demand gives profit £408.16/week, £8.50 below that curve's £416.67/week maximum.

Charging £12.00, the constant elasticity recommendation, under linear demand gives profit £360.00/week, £45.00 below that curve's £405.00/week maximum.

Where an optimal set is tied, the evaluated candidate is its smallest price; the full set is reported and another member can have a different consequence under the other curve. Regret is calculated from unrounded contribution differences, equivalent to profit differences because the same fixed cost cancels. Only floating-point roundoff near zero is removed.

## Conditional conclusion and limitations

The same local demand information supports different optimal prices. The financial result depends on curvature, costs and permitted prices; the larger model-implied profit does not prove that its demand assumption is better. All five complete investigations, derivations and limitations remain in investigation_worksheet.md.

The constant-elasticity revenue objective selects £1.00 and implies 10,000 units/week, with profit −£50,000.00/week. This extreme volume exposes extrapolation and absent capacity constraints; it is not an established sales forecast. Own-price sensitivity does not independently identify a substitution effect. Real customer data, empirical demand checks and operational constraints would be needed for a commercial decision.

## Methodology

AI assisted with code development and explanatory drafting. Results are calculated deterministically from the displayed mathematical models and checked by automated tests and separate equation-based calculations. These software checks do not establish which checks the project owner has personally completed.
