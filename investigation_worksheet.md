# Complete Mathematical Investigation and Findings

## Purpose and scope

How do demand assumptions, costs and price restrictions affect a hypothetical business's revenue and operating profit? This investigation compares two demand functions matched at the same starting price, quantity, slope and elasticity. It calculates their complete profit-maximising price sets on a shared permitted interval and tests the financial sensitivity of those conclusions. These are conditional model results, not forecasts established from customer data.

## Starting assumptions and financial definitions

The benchmark is p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £6.00/unit, F = £0.00/week and p ∈ [£1.00, £15.00]. Prices are continuous and quantity can be fractional. Costs and demand use a consistent weekly period. Both models have Q(p₀)=Q₀ and Q′(p₀)=−eQ₀/p₀; the linear curve's point elasticity varies with price below its cutoff, whereas constant-elasticity demand keeps elasticity e.

$$R(p)=pQ(p),\quad VC(p)=cQ(p),\quad TC(p)=cQ(p)+F,\quad \pi(p)=(p-c)Q(p)-F.$$

Contribution is revenue less variable cost: (p−c)Q. It is available to cover fixed costs. A positive contribution can coexist with an operating loss; when Q=0, unavoidable fixed costs remain payable and π=−F.

### Benchmark profit maxima

| Demand model | Optimal price set | Units/week | Revenue/week | Total cost/week | Profit/week |
| --- | --- | --- | --- | --- | --- |
| Linear | £10.50 | 90 | £945.00 | £540.00 | £405.00 |
| Constant elasticity | £12.00 | 69.4444 | £833.33 | £416.67 | £416.67 |

## Starting, chosen and profit-optimal price comparison

For this reproducible example the chosen test price is £12.00, the constant-elasticity optimum. The live app allows any test price in the permitted interval. Each change is relative to that same curve's starting-price profit. Percentages are only reported when starting profit is positive; no percentage is assigned to a zero or negative baseline.

| Demand model | Price choice | Price | Units/week | Revenue/week | Variable cost/week | Contribution/week | Profit/week | Δ profit/week | Δ profit (%) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Linear | Starting price | £10.00 | 100 | £1,000.00 | £600.00 | £400.00 | £400.00 | £0.00 | +0.0000% |
| Linear | Chosen test price | £12.00 | 60 | £720.00 | £360.00 | £360.00 | £360.00 | −£40.00 | -10.0000% |
| Linear | Profit optimum | £10.50 | 90 | £945.00 | £540.00 | £405.00 | £405.00 | +£5.00 | +1.2500% |
| Constant elasticity | Starting price | £10.00 | 100 | £1,000.00 | £600.00 | £400.00 | £400.00 | £0.00 | +0.0000% |
| Constant elasticity | Chosen test price | £12.00 | 69.4444 | £833.33 | £416.67 | £416.67 | £416.67 | +£16.67 | +4.1667% |
| Constant elasticity | Profit optimum | £12.00 | 69.4444 | £833.33 | £416.67 | £416.67 | £416.67 | +£16.67 | +4.1667% |

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

## Marginal revenue equals marginal cost: applicable interior checks

For differentiable demand with Q′(p) ≠ 0, marginal revenue is MR = p + Q/Q′ and marginal cost is MC = c. At a differentiable interior positive-demand stationary profit maximum, π′(p) = Q + (p−c)Q′ = Q′(MR−MC) = 0, so MR = MC. The equality is not required at a binding boundary, a cutoff or a flat zero-demand region; those cases need endpoint or complete-set comparisons instead.

At the benchmark linear optimum £10.50, MR = £6.00/unit and MC = £6.00/unit. At this differentiable interior maximum with positive demand, MR = p + Q/Q′ agrees with MC = c within numerical tolerance.

At the benchmark constant elasticity optimum £12.00, MR = £6.00/unit and MC = £6.00/unit. At this differentiable interior maximum with positive demand, MR = p + Q/Q′ agrees with MC = c within numerical tolerance.

## Revenue maximisation versus profit maximisation

Revenue rewards sales receipts. Profit deducts the costs of generating those sales. On the positive-demand linear segment, R=ap−bp², R′=a−2bp and R″=−2b<0, so the stationary revenue price is z/2, subject to the price interval and cutoff. For constant elasticity, R=Kp^(1−e) and R′=K(1−e)p^(−e): revenue falls with price when e>1, is constant when e=1, and rises when e<1. Endpoints and any complete tie set are included.

For linear demand, the revenue optimum is £7.50, giving 150 units/week, revenue £1,125.00 and profit £225.00/week. The profit optimum is £10.50, giving revenue £945.00 and profit £405.00/week. Choosing the revenue objective increases revenue by £180.00 but reduces profit by £180.00/week.

For constant elasticity demand, the revenue optimum is £1.00, giving 10,000 units/week, revenue £10,000.00 and profit −£50,000.00/week. The profit optimum is £12.00, giving revenue £833.33 and profit £416.67/week. Choosing the revenue objective increases revenue by £9,166.67 but reduces profit by £50,416.67/week.

| Model | Objective | Optimal price set | Units/week | Revenue/week | Total cost/week | Profit/week |
| --- | --- | --- | --- | --- | --- | --- |
| Linear | Maximum profit | £10.50 | 90 | £945.00 | £540.00 | £405.00 |
| Linear | Maximum revenue | £7.50 | 150 | £1,125.00 | £900.00 | £225.00 |
| Constant elasticity | Maximum profit | £12.00 | 69.4444 | £833.33 | £416.67 | £416.67 |
| Constant elasticity | Maximum revenue | £1.00 | 10,000 | £10,000.00 | £60,000.00 | −£50,000.00 |

The benchmark therefore shows why sales volume or revenue alone is an incomplete pricing target: additional units can carry costs that outweigh their additional receipts. For tied revenue optima in other input cases, the smallest reported price is only a representative; compare profit within the whole revenue-optimal set before making a decision.

At the constant-elasticity benchmark revenue optimum £1.00, the assumed curve predicts 10,000 units/week. That extreme quantity follows from extrapolating the curve to the lower permitted boundary with no capacity constraint. It is not an established sales forecast; the associated profit −£50,000.00/week also shows why revenue alone is an incomplete objective.

## 1. Elasticity and pricing

### Economic question

How does the assumed responsiveness of demand change the profit-maximising price and the financial disagreement between locally matched models?

### Starting assumptions and variables

Changed: Starting elasticity e = 0.5, 1, 1.5, 2, 3; the baseline is e = 2.

Held constant: p₀ = £10.00, Q₀ = 100 units/week; c = £6.00/unit, F = £0.00/week, permitted prices £1.00–£15.00. Both models match quantity, slope and elasticity at p₀ within each scenario.

### Theoretical prediction

Before clipping or price bounds apply, increasing e reduces the linear cutoff z = p₀(1+1/e), hence lowers the linear stationary price (z+c)/2. For constant elasticity with e>1 and c>0, ec/(e−1) also falls as e increases. For e≤1 profit rises throughout positive prices, so the bounded optimum is U. The models share local starting information but have different curvature away from p₀.

### Mathematical reasoning

$$
Q_L(p)=\max(0,a-bp),\quad a=Q_0(1+e),\quad b=\frac{eQ_0}{p_0}
$$

$$
Q_C(p)=Q_0(p/p_0)^{-e}
$$

$$
R=pQ,\quad TC=cQ+F,\quad \pi=(p-c)Q-F
$$

$$
v_L=\frac{p_0(1+1/e)+c}{2},\quad \frac{dv_L}{de}=-\frac{p_0}{2e^2}<0
$$

$$
v_C=\frac{ec}{e-1},\quad \frac{dv_C}{de}=-\frac{c}{(e-1)^2}<0\quad(e>1,c>0)
$$

### Calculated results and before-and-after comparison

| Scenario | Demand model | Optimal price set | Units/week | Revenue/week | Total cost/week | Profit/week |
| --- | --- | --- | --- | --- | --- | --- |
| e = 0.5 | Linear | £15.00 | 75 | £1,125.00 | £450.00 | £675.00 |
| e = 0.5 | Constant elasticity | £15.00 | 81.6497 | £1,224.74 | £489.90 | £734.85 |
| e = 1 | Linear | £13.00 | 70 | £910.00 | £420.00 | £490.00 |
| e = 1 | Constant elasticity | £15.00 | 66.6667 | £1,000.00 | £400.00 | £600.00 |
| e = 1.5 | Linear | £11.33 | 80 | £906.67 | £480.00 | £426.67 |
| e = 1.5 | Constant elasticity | £15.00 | 54.4331 | £816.50 | £326.60 | £489.90 |
| e = 2 (baseline) | Linear | £10.50 | 90 | £945.00 | £540.00 | £405.00 |
| e = 2 (baseline) | Constant elasticity | £12.00 | 69.4444 | £833.33 | £416.67 | £416.67 |
| e = 3 | Linear | £9.67 | 110 | £1,063.33 | £660.00 | £403.33 |
| e = 3 | Constant elasticity | £9.00 | 137.1742 | £1,234.57 | £823.05 | £411.52 |

### Changes from each model's baseline

| Scenario | Demand model | Δ price | Δ units/week | Δ revenue/week | Δ profit/week |
| --- | --- | --- | --- | --- | --- |
| e = 0.5 | Linear | +£4.50 | -15.0000 | +£180.00 | +£270.00 |
| e = 0.5 | Constant elasticity | +£3.00 | +12.2052 | +£391.41 | +£318.18 |
| e = 1 | Linear | +£2.50 | -20.0000 | −£35.00 | +£85.00 |
| e = 1 | Constant elasticity | +£3.00 | -2.7778 | +£166.67 | +£183.33 |
| e = 1.5 | Linear | +£0.83 | -10.0000 | −£38.33 | +£21.67 |
| e = 1.5 | Constant elasticity | +£3.00 | -15.0113 | −£16.84 | +£73.23 |
| e = 2 (baseline) | Linear | £0.00 | +0.0000 | £0.00 | £0.00 |
| e = 2 (baseline) | Constant elasticity | £0.00 | +0.0000 | £0.00 | £0.00 |
| e = 3 | Linear | −£0.83 | +20.0000 | +£118.33 | −£1.67 |
| e = 3 | Constant elasticity | −£3.00 | +67.7298 | +£401.23 | −£5.14 |

Calculations use unrounded values. Currency is displayed to two decimal places and quantity to four where needed. An interval denotes every equally optimal price; the displayed financial quantities use its smallest representative.

### Worked calculations

#### Linear — e = 0.5

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 0.5, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. a = Q₀(1 + e) = 100(1 + 0.5) = 150; b = eQ₀/p₀ = 0.5 × 100/10 = 5. Thus Q(p) = max(0, 150 − 5p).
3. The zero-demand cutoff is z = a/b = 150/5 = 30. For p < 30, π(p) = (p − 6)(150 − 5p) − 0.
4. On this positive-demand part, π′(p) = a + bc − 2bp = 180 − 10p. Setting π′ = 0 gives v = (z + c)/2 = (30 + 6)/2 = 18.
5. The candidate 18 is outside the permitted interval. It cannot be used as an interior positive-demand maximum.
6. Candidate comparison: p = 1: π = −£725.00; p = 15: π = £675.00.
7. Selected quantity: Q(15) = max(0, 150 − 5 × 15) = 75 units/week.
8. Full profit-maximising price set: £15.00. This maximum is classified as upper boundary.
9. R = pQ = 15 × 75 = £1,125.00/week; VC = cQ = 6 × 75 = £450.00/week; TC = VC + F = £450.00 + £0.00 = £450.00/week.
10. Contribution = (p−c)Q = (15 − 6) × 75 = £675.00/week. Operating profit π = R−TC = £1,125.00 − £450.00 = £675.00/week.
11. Change from this model's baseline: price +£4.50; quantity -15.0000 units/week; revenue +£180.00/week; profit +£270.00/week. Differences use unrounded calculations.

#### Constant elasticity — e = 0.5

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 0.5, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. Q(p) = 100(p/10)^(−0.5). π(p) = (p − 6) × 100(p/10)^(−0.5) − 0.
3. Write K = Q₀p₀^e > 0. Differentiation gives π′(p) = Kp^(−e−1)[(1−e)p + ec] = Kp^(−1.5)[(0.5)p + 3]. The first factor is positive, so the bracket decides whether profit rises or falls.
4. Here e = 0.5 < 1. The derivative is strictly positive for every positive price, so the bounded maximum is the upper boundary £15.00. No interior stationary maximum is available.
5. Candidate comparison: p = 1: π = −£1,581.14; p = 15: π = £734.85.
6. Selected quantity: Q(15) = 100 × (15/10)^(−0.5) = 81.6497 units/week.
7. Full profit-maximising price set: £15.00. This maximum is classified as upper boundary.
8. R = pQ = 15 × 81.649658 = £1,224.74/week; VC = cQ = 6 × 81.649658 = £489.90/week; TC = VC + F = £489.90 + £0.00 = £489.90/week.
9. Contribution = (p−c)Q = (15 − 6) × 81.649658 = £734.85/week. Operating profit π = R−TC = £1,224.74 − £489.90 = £734.85/week.
10. Change from this model's baseline: price +£3.00; quantity +12.2052 units/week; revenue +£391.41/week; profit +£318.18/week. Differences use unrounded calculations.

#### Linear — e = 1

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 1, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. a = Q₀(1 + e) = 100(1 + 1) = 200; b = eQ₀/p₀ = 1 × 100/10 = 10. Thus Q(p) = max(0, 200 − 10p).
3. The zero-demand cutoff is z = a/b = 200/10 = 20. For p < 20, π(p) = (p − 6)(200 − 10p) − 0.
4. On this positive-demand part, π′(p) = a + bc − 2bp = 260 − 20p. Setting π′ = 0 gives v = (z + c)/2 = (20 + 6)/2 = 13.
5. v = 13 is permitted and below z = 20. π″ = −2b = −20 < 0, so it is the strict maximum on the positive-demand piece; compare it with the boundaries and plateau.
6. Candidate comparison: p = 1: π = −£950.00; p = 13: π = £490.00; p = 15: π = £450.00.
7. Selected quantity: Q(13) = max(0, 200 − 10 × 13) = 70 units/week.
8. Full profit-maximising price set: £13.00. This maximum is classified as interior.
9. R = pQ = 13 × 70 = £910.00/week; VC = cQ = 6 × 70 = £420.00/week; TC = VC + F = £420.00 + £0.00 = £420.00/week.
10. Contribution = (p−c)Q = (13 − 6) × 70 = £490.00/week. Operating profit π = R−TC = £910.00 − £420.00 = £490.00/week.
11. Change from this model's baseline: price +£2.50; quantity -20.0000 units/week; revenue −£35.00/week; profit +£85.00/week. Differences use unrounded calculations.

#### Constant elasticity — e = 1

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 1, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. Q(p) = 100(p/10)^(−1). π(p) = (p − 6) × 100(p/10)^(−1) − 0.
3. Write K = Q₀p₀^e > 0. Differentiation gives π′(p) = Kp^(−e−1)[(1−e)p + ec] = Kp^(−2)[(0)p + 6]. The first factor is positive, so the bracket decides whether profit rises or falls.
4. Here e = 1 = 1 with c > 0. The derivative is strictly positive for every positive price, so the bounded maximum is the upper boundary £15.00. No interior stationary maximum is available.
5. Candidate comparison: p = 1: π = −£5,000.00; p = 15: π = £600.00.
6. Selected quantity: Q(15) = 100 × (15/10)^(−1) = 66.6667 units/week.
7. Full profit-maximising price set: £15.00. This maximum is classified as upper boundary.
8. R = pQ = 15 × 66.666667 = £1,000.00/week; VC = cQ = 6 × 66.666667 = £400.00/week; TC = VC + F = £400.00 + £0.00 = £400.00/week.
9. Contribution = (p−c)Q = (15 − 6) × 66.666667 = £600.00/week. Operating profit π = R−TC = £1,000.00 − £400.00 = £600.00/week.
10. Change from this model's baseline: price +£3.00; quantity -2.7778 units/week; revenue +£166.67/week; profit +£183.33/week. Differences use unrounded calculations.

#### Linear — e = 1.5

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 1.5, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. a = Q₀(1 + e) = 100(1 + 1.5) = 250; b = eQ₀/p₀ = 1.5 × 100/10 = 15. Thus Q(p) = max(0, 250 − 15p).
3. The zero-demand cutoff is z = a/b = 250/15 = 16.666667. For p < 16.666667, π(p) = (p − 6)(250 − 15p) − 0.
4. On this positive-demand part, π′(p) = a + bc − 2bp = 340 − 30p. Setting π′ = 0 gives v = (z + c)/2 = (16.666667 + 6)/2 = 11.333333.
5. v = 11.333333 is permitted and below z = 16.666667. π″ = −2b = −30 < 0, so it is the strict maximum on the positive-demand piece; compare it with the boundaries and plateau.
6. Candidate comparison: p = 1: π = −£1,175.00; p = 11.333333: π = £426.67; p = 15: π = £225.00.
7. Selected quantity: Q(11.333333) = max(0, 250 − 15 × 11.333333) = 80 units/week.
8. Full profit-maximising price set: £11.33. This maximum is classified as interior.
9. R = pQ = 11.333333 × 80 = £906.67/week; VC = cQ = 6 × 80 = £480.00/week; TC = VC + F = £480.00 + £0.00 = £480.00/week.
10. Contribution = (p−c)Q = (11.333333 − 6) × 80 = £426.67/week. Operating profit π = R−TC = £906.67 − £480.00 = £426.67/week.
11. Change from this model's baseline: price +£0.83; quantity -10.0000 units/week; revenue −£38.33/week; profit +£21.67/week. Differences use unrounded calculations.

#### Constant elasticity — e = 1.5

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 1.5, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. Q(p) = 100(p/10)^(−1.5). π(p) = (p − 6) × 100(p/10)^(−1.5) − 0.
3. Write K = Q₀p₀^e > 0. Differentiation gives π′(p) = Kp^(−e−1)[(1−e)p + ec] = Kp^(−2.5)[(-0.5)p + 9]. The first factor is positive, so the bracket decides whether profit rises or falls.
4. v = ec/(e−1) = 1.5 × 6/(1.5 − 1) = 18. The derivative is positive below v and negative above v, proving a global maximum over positive prices.
5. Restricting the candidate to the interval gives min(15, max(1, 18)) = 15. The maximum is at a permitted boundary; its derivative need not be zero.
6. Candidate comparison: p = 1: π = −£15,811.39; p = 15: π = £489.90.
7. Selected quantity: Q(15) = 100 × (15/10)^(−1.5) = 54.4331 units/week.
8. Full profit-maximising price set: £15.00. This maximum is classified as upper boundary.
9. R = pQ = 15 × 54.433105 = £816.50/week; VC = cQ = 6 × 54.433105 = £326.60/week; TC = VC + F = £326.60 + £0.00 = £326.60/week.
10. Contribution = (p−c)Q = (15 − 6) × 54.433105 = £489.90/week. Operating profit π = R−TC = £816.50 − £326.60 = £489.90/week.
11. Change from this model's baseline: price +£3.00; quantity -15.0113 units/week; revenue −£16.84/week; profit +£73.23/week. Differences use unrounded calculations.

#### Linear — e = 2 (baseline)

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. a = Q₀(1 + e) = 100(1 + 2) = 300; b = eQ₀/p₀ = 2 × 100/10 = 20. Thus Q(p) = max(0, 300 − 20p).
3. The zero-demand cutoff is z = a/b = 300/20 = 15. For p < 15, π(p) = (p − 6)(300 − 20p) − 0.
4. On this positive-demand part, π′(p) = a + bc − 2bp = 420 − 40p. Setting π′ = 0 gives v = (z + c)/2 = (15 + 6)/2 = 10.5.
5. v = 10.5 is permitted and below z = 15. π″ = −2b = −40 < 0, so it is the strict maximum on the positive-demand piece; compare it with the boundaries and plateau.
6. Candidate comparison: p = 1: π = −£1,400.00; p = 10.5: π = £405.00; p = 15: π = £0.00.
7. Every permitted zero-demand price in [£15.00, £15.00] gives Q = 0, contribution = £0.00 and π = −F = £0.00. Compare this entire plateau with the positive-demand candidates.
8. Selected quantity: Q(10.5) = max(0, 300 − 20 × 10.5) = 90 units/week.
9. Full profit-maximising price set: £10.50. This maximum is classified as interior.
10. R = pQ = 10.5 × 90 = £945.00/week; VC = cQ = 6 × 90 = £540.00/week; TC = VC + F = £540.00 + £0.00 = £540.00/week.
11. Contribution = (p−c)Q = (10.5 − 6) × 90 = £405.00/week. Operating profit π = R−TC = £945.00 − £540.00 = £405.00/week.
12. Change from this model's baseline: price £0.00; quantity +0.0000 units/week; revenue £0.00/week; profit £0.00/week. Differences use unrounded calculations.

#### Constant elasticity — e = 2 (baseline)

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. Q(p) = 100(p/10)^(−2). π(p) = (p − 6) × 100(p/10)^(−2) − 0.
3. Write K = Q₀p₀^e > 0. Differentiation gives π′(p) = Kp^(−e−1)[(1−e)p + ec] = Kp^(−3)[(-1)p + 12]. The first factor is positive, so the bracket decides whether profit rises or falls.
4. v = ec/(e−1) = 2 × 6/(2 − 1) = 12. The derivative is positive below v and negative above v, proving a global maximum over positive prices.
5. The candidate lies strictly inside the permitted interval. π″(v) = K(1−e)v^(−e−1) < 0 because 1−e = -1 < 0.
6. Candidate comparison: p = 1: π = −£50,000.00; p = 12: π = £416.67; p = 15: π = £400.00.
7. Selected quantity: Q(12) = 100 × (12/10)^(−2) = 69.4444 units/week.
8. Full profit-maximising price set: £12.00. This maximum is classified as interior.
9. R = pQ = 12 × 69.444444 = £833.33/week; VC = cQ = 6 × 69.444444 = £416.67/week; TC = VC + F = £416.67 + £0.00 = £416.67/week.
10. Contribution = (p−c)Q = (12 − 6) × 69.444444 = £416.67/week. Operating profit π = R−TC = £833.33 − £416.67 = £416.67/week.
11. Change from this model's baseline: price £0.00; quantity +0.0000 units/week; revenue £0.00/week; profit £0.00/week. Differences use unrounded calculations.

#### Linear — e = 3

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 3, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. a = Q₀(1 + e) = 100(1 + 3) = 400; b = eQ₀/p₀ = 3 × 100/10 = 30. Thus Q(p) = max(0, 400 − 30p).
3. The zero-demand cutoff is z = a/b = 400/30 = 13.333333. For p < 13.333333, π(p) = (p − 6)(400 − 30p) − 0.
4. On this positive-demand part, π′(p) = a + bc − 2bp = 580 − 60p. Setting π′ = 0 gives v = (z + c)/2 = (13.333333 + 6)/2 = 9.666667.
5. v = 9.666667 is permitted and below z = 13.333333. π″ = −2b = −60 < 0, so it is the strict maximum on the positive-demand piece; compare it with the boundaries and plateau.
6. Candidate comparison: p = 1: π = −£1,850.00; p = 9.666667: π = £403.33; p = 13.333333: π = £0.00; p = 15: π = £0.00.
7. Every permitted zero-demand price in [£13.33, £15.00] gives Q = 0, contribution = £0.00 and π = −F = £0.00. Compare this entire plateau with the positive-demand candidates.
8. Selected quantity: Q(9.666667) = max(0, 400 − 30 × 9.666667) = 110 units/week.
9. Full profit-maximising price set: £9.67. This maximum is classified as interior.
10. R = pQ = 9.666667 × 110 = £1,063.33/week; VC = cQ = 6 × 110 = £660.00/week; TC = VC + F = £660.00 + £0.00 = £660.00/week.
11. Contribution = (p−c)Q = (9.666667 − 6) × 110 = £403.33/week. Operating profit π = R−TC = £1,063.33 − £660.00 = £403.33/week.
12. Change from this model's baseline: price −£0.83; quantity +20.0000 units/week; revenue +£118.33/week; profit −£1.67/week. Differences use unrounded calculations.

#### Constant elasticity — e = 3

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 3, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. Q(p) = 100(p/10)^(−3). π(p) = (p − 6) × 100(p/10)^(−3) − 0.
3. Write K = Q₀p₀^e > 0. Differentiation gives π′(p) = Kp^(−e−1)[(1−e)p + ec] = Kp^(−4)[(-2)p + 18]. The first factor is positive, so the bracket decides whether profit rises or falls.
4. v = ec/(e−1) = 3 × 6/(3 − 1) = 9. The derivative is positive below v and negative above v, proving a global maximum over positive prices.
5. The candidate lies strictly inside the permitted interval. π″(v) = K(1−e)v^(−e−1) < 0 because 1−e = -2 < 0.
6. Candidate comparison: p = 1: π = −£500,000.00; p = 9: π = £411.52; p = 15: π = £266.67.
7. Selected quantity: Q(9) = 100 × (9/10)^(−3) = 137.1742 units/week.
8. Full profit-maximising price set: £9.00. This maximum is classified as interior.
9. R = pQ = 9 × 137.174211 = £1,234.57/week; VC = cQ = 6 × 137.174211 = £823.05/week; TC = VC + F = £823.05 + £0.00 = £823.05/week.
10. Contribution = (p−c)Q = (9 − 6) × 137.174211 = £411.52/week. Operating profit π = R−TC = £1,234.57 − £823.05 = £411.52/week.
11. Change from this model's baseline: price −£3.00; quantity +67.7298 units/week; revenue +£401.23/week; profit −£5.14/week. Differences use unrounded calculations.

### Interpretation of findings

e = 0.5: constant-elasticity price minus linear price £0.00, profit difference +£59.85/week; e = 1: constant-elasticity price minus linear price +£2.00, profit difference +£110.00/week; e = 1.5: constant-elasticity price minus linear price +£3.67, profit difference +£63.23/week; e = 2: constant-elasticity price minus linear price +£1.50, profit difference +£11.67/week; e = 3: constant-elasticity price minus linear price −£0.67, profit difference +£8.19/week. Across these 5 scenarios, the upper bound binds in 1 linear and 3 constant-elasticity cases. A matching quantity and slope at one price do not determine the whole curve: linear demand reaches zero, while constant-elasticity demand remains positive at every finite price.

### Financial implications

The baseline comparison is Linear (e = 2 (baseline)): optimal price set £10.50, quantity 90 units/week, revenue £945.00/week and operating profit £405.00/week; Constant elasticity (e = 2 (baseline)): optimal price set £12.00, quantity 69.4444 units/week, revenue £833.33/week and operating profit £416.67/week. A hypothetical business should treat the gap as sensitivity to demand assumptions, rather than take either model's higher profit as established revenue potential. A binding maximum price makes the permitted interval a material business assumption.

### Conclusion

Within the tested range from e = 0.5 to e = 3, each model's recommended price is non-increasing as elasticity rises. At e = 2, the model price difference is £1.50; the financial conclusion depends on demand curvature and any active price bound.

### Limitations and further investigation

Elasticity is an assumed local input, not an estimate from sales data. Both Q₀ and p₀ are held fixed when e changes; this compares hypothetical curves, rather than proving a causal effect on real consumers. This own-price sensitivity does not independently identify a substitution effect: no competitor-price or compensated-demand model is established. A follow-up is to estimate elasticity and curvature from observed prices and quantities over a plausible range.

## 2. Unit cost and margin

### Economic question

How much of an increase in unit cost is passed into the profit-maximising selling price, and what happens to sales, revenue and profit?

### Starting assumptions and variables

Changed: Unit cost c increases from £6.00 to £7.00 per unit (change £1.00).

Held constant: p₀ = £10.00, Q₀ = 100 units/week; e = 2, F = £0.00/week, permitted prices £1.00–£15.00.

### Theoretical prediction

On valid interior solutions, the linear price rises by half the unit-cost increase, whereas the constant-elasticity price rises by e/(e−1) times that increase. Re-optimising can protect some margin, but the higher price reduces quantity demanded; a price increase alone does not show that profit improves.

### Mathematical reasoning

$$
Q_L(p)=\max(0,a-bp),\quad a=Q_0(1+e),\quad b=\frac{eQ_0}{p_0}
$$

$$
Q_C(p)=Q_0(p/p_0)^{-e}
$$

$$
R=pQ,\quad TC=cQ+F,\quad \pi=(p-c)Q-F
$$

$$
\frac{dv_L}{dc}=\frac12,\qquad \frac{dv_C}{dc}=\frac{e}{e-1}\quad(e>1,c>0)
$$

### Calculated results and before-and-after comparison

| Scenario | Demand model | Optimal price set | Units/week | Revenue/week | Total cost/week | Profit/week |
| --- | --- | --- | --- | --- | --- | --- |
| c = £6 (baseline) | Linear | £10.50 | 90 | £945.00 | £540.00 | £405.00 |
| c = £6 (baseline) | Constant elasticity | £12.00 | 69.4444 | £833.33 | £416.67 | £416.67 |
| c = £7 | Linear | £11.00 | 80 | £880.00 | £560.00 | £320.00 |
| c = £7 | Constant elasticity | £14.00 | 51.0204 | £714.29 | £357.14 | £357.14 |

### Changes from each model's baseline

| Scenario | Demand model | Δ price | Δ units/week | Δ revenue/week | Δ profit/week |
| --- | --- | --- | --- | --- | --- |
| c = £6 (baseline) | Linear | £0.00 | +0.0000 | £0.00 | £0.00 |
| c = £6 (baseline) | Constant elasticity | £0.00 | +0.0000 | £0.00 | £0.00 |
| c = £7 | Linear | +£0.50 | -10.0000 | −£65.00 | −£85.00 |
| c = £7 | Constant elasticity | +£2.00 | -18.4240 | −£119.05 | −£59.52 |

Calculations use unrounded values. Currency is displayed to two decimal places and quantity to four where needed. An interval denotes every equally optimal price; the displayed financial quantities use its smallest representative.

### Worked calculations

#### Linear — c = £6 (baseline)

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. a = Q₀(1 + e) = 100(1 + 2) = 300; b = eQ₀/p₀ = 2 × 100/10 = 20. Thus Q(p) = max(0, 300 − 20p).
3. The zero-demand cutoff is z = a/b = 300/20 = 15. For p < 15, π(p) = (p − 6)(300 − 20p) − 0.
4. On this positive-demand part, π′(p) = a + bc − 2bp = 420 − 40p. Setting π′ = 0 gives v = (z + c)/2 = (15 + 6)/2 = 10.5.
5. v = 10.5 is permitted and below z = 15. π″ = −2b = −40 < 0, so it is the strict maximum on the positive-demand piece; compare it with the boundaries and plateau.
6. Candidate comparison: p = 1: π = −£1,400.00; p = 10.5: π = £405.00; p = 15: π = £0.00.
7. Every permitted zero-demand price in [£15.00, £15.00] gives Q = 0, contribution = £0.00 and π = −F = £0.00. Compare this entire plateau with the positive-demand candidates.
8. Selected quantity: Q(10.5) = max(0, 300 − 20 × 10.5) = 90 units/week.
9. Full profit-maximising price set: £10.50. This maximum is classified as interior.
10. R = pQ = 10.5 × 90 = £945.00/week; VC = cQ = 6 × 90 = £540.00/week; TC = VC + F = £540.00 + £0.00 = £540.00/week.
11. Contribution = (p−c)Q = (10.5 − 6) × 90 = £405.00/week. Operating profit π = R−TC = £945.00 − £540.00 = £405.00/week.
12. Change from this model's baseline: price £0.00; quantity +0.0000 units/week; revenue £0.00/week; profit £0.00/week. Differences use unrounded calculations.

#### Constant elasticity — c = £6 (baseline)

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. Q(p) = 100(p/10)^(−2). π(p) = (p − 6) × 100(p/10)^(−2) − 0.
3. Write K = Q₀p₀^e > 0. Differentiation gives π′(p) = Kp^(−e−1)[(1−e)p + ec] = Kp^(−3)[(-1)p + 12]. The first factor is positive, so the bracket decides whether profit rises or falls.
4. v = ec/(e−1) = 2 × 6/(2 − 1) = 12. The derivative is positive below v and negative above v, proving a global maximum over positive prices.
5. The candidate lies strictly inside the permitted interval. π″(v) = K(1−e)v^(−e−1) < 0 because 1−e = -1 < 0.
6. Candidate comparison: p = 1: π = −£50,000.00; p = 12: π = £416.67; p = 15: π = £400.00.
7. Selected quantity: Q(12) = 100 × (12/10)^(−2) = 69.4444 units/week.
8. Full profit-maximising price set: £12.00. This maximum is classified as interior.
9. R = pQ = 12 × 69.444444 = £833.33/week; VC = cQ = 6 × 69.444444 = £416.67/week; TC = VC + F = £416.67 + £0.00 = £416.67/week.
10. Contribution = (p−c)Q = (12 − 6) × 69.444444 = £416.67/week. Operating profit π = R−TC = £833.33 − £416.67 = £416.67/week.
11. Change from this model's baseline: price £0.00; quantity +0.0000 units/week; revenue £0.00/week; profit £0.00/week. Differences use unrounded calculations.

#### Linear — c = £7

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £7.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. a = Q₀(1 + e) = 100(1 + 2) = 300; b = eQ₀/p₀ = 2 × 100/10 = 20. Thus Q(p) = max(0, 300 − 20p).
3. The zero-demand cutoff is z = a/b = 300/20 = 15. For p < 15, π(p) = (p − 7)(300 − 20p) − 0.
4. On this positive-demand part, π′(p) = a + bc − 2bp = 440 − 40p. Setting π′ = 0 gives v = (z + c)/2 = (15 + 7)/2 = 11.
5. v = 11 is permitted and below z = 15. π″ = −2b = −40 < 0, so it is the strict maximum on the positive-demand piece; compare it with the boundaries and plateau.
6. Candidate comparison: p = 1: π = −£1,680.00; p = 11: π = £320.00; p = 15: π = £0.00.
7. Every permitted zero-demand price in [£15.00, £15.00] gives Q = 0, contribution = £0.00 and π = −F = £0.00. Compare this entire plateau with the positive-demand candidates.
8. Selected quantity: Q(11) = max(0, 300 − 20 × 11) = 80 units/week.
9. Full profit-maximising price set: £11.00. This maximum is classified as interior.
10. R = pQ = 11 × 80 = £880.00/week; VC = cQ = 7 × 80 = £560.00/week; TC = VC + F = £560.00 + £0.00 = £560.00/week.
11. Contribution = (p−c)Q = (11 − 7) × 80 = £320.00/week. Operating profit π = R−TC = £880.00 − £560.00 = £320.00/week.
12. Change from this model's baseline: price +£0.50; quantity -10.0000 units/week; revenue −£65.00/week; profit −£85.00/week. Differences use unrounded calculations.

#### Constant elasticity — c = £7

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £7.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. Q(p) = 100(p/10)^(−2). π(p) = (p − 7) × 100(p/10)^(−2) − 0.
3. Write K = Q₀p₀^e > 0. Differentiation gives π′(p) = Kp^(−e−1)[(1−e)p + ec] = Kp^(−3)[(-1)p + 14]. The first factor is positive, so the bracket decides whether profit rises or falls.
4. v = ec/(e−1) = 2 × 7/(2 − 1) = 14. The derivative is positive below v and negative above v, proving a global maximum over positive prices.
5. The candidate lies strictly inside the permitted interval. π″(v) = K(1−e)v^(−e−1) < 0 because 1−e = -1 < 0.
6. Candidate comparison: p = 1: π = −£60,000.00; p = 14: π = £357.14; p = 15: π = £355.56.
7. Selected quantity: Q(14) = 100 × (14/10)^(−2) = 51.0204 units/week.
8. Full profit-maximising price set: £14.00. This maximum is classified as interior.
9. R = pQ = 14 × 51.020408 = £714.29/week; VC = cQ = 7 × 51.020408 = £357.14/week; TC = VC + F = £357.14 + £0.00 = £357.14/week.
10. Contribution = (p−c)Q = (14 − 7) × 51.020408 = £357.14/week. Operating profit π = R−TC = £714.29 − £357.14 = £357.14/week.
11. Change from this model's baseline: price +£2.00; quantity -18.4240 units/week; revenue −£119.05/week; profit −£59.52/week. Differences use unrounded calculations.

### Interpretation of findings

Linear: price £10.50 → £11.00 (change +£0.50; pass-through Δp/Δc = 0.5), quantity 90 → 80 units/week (change -10.0000), revenue £945.00 → £880.00 (change −£65.00), and profit £405.00 → £320.00/week (change −£85.00); Constant elasticity: price £12.00 → £14.00 (change +£2.00; pass-through Δp/Δc = 2), quantity 69.4444 → 51.0204 units/week (change -18.4240), revenue £833.33 → £714.29 (change −£119.05), and profit £416.67 → £357.14/week (change −£59.52). Both stationary prices remain feasible, so the derivative pass-through formulas apply without a binding price bound.

### Financial implications

The cost increase reduces optimised profit in both models, even though prices rise. The constant-elasticity response sacrifices more volume because its optimal price adjustment is larger. A hypothetical business would compare supplier savings, attainable margin and the risk of lost demand; passing costs through to customers is constrained by their assumed responsiveness.

### Conclusion

For this £1.00 cost rise, the calculated optimal price rises by £0.50 under linear demand and £2.00 under constant-elasticity demand. The two locally matched demand curves therefore imply materially different pricing responses to the same cost pressure.

### Limitations and further investigation

Unit cost is constant per unit, and demand is unchanged by the supplier cost shock. Capacity, competitor responses and step changes in costs are excluded. The pass-through derivatives apply only while their interior candidates remain valid and within the permitted interval.

## 3. Price restrictions

### Economic question

What is the financial effect of lowering the maximum permitted selling price while leaving demand and costs unchanged?

### Starting assumptions and variables

Changed: Upper permitted price U falls from £15.00 to £11.00.

Held constant: p₀ = £10.00, Q₀ = 100 units/week; e = 2, c = £6.00/unit, F = £0.00/week, lower permitted price £1.00.

### Theoretical prediction

Reducing the feasible set cannot increase its maximum attainable profit. A cap above a model's original optimal price leaves that optimum available; a cap below it can force a lower price, higher quantity and lower margin.

### Mathematical reasoning

$$
Q_L(p)=\max(0,a-bp),\quad a=Q_0(1+e),\quad b=\frac{eQ_0}{p_0}
$$

$$
Q_C(p)=Q_0(p/p_0)^{-e}
$$

$$
R=pQ,\quad TC=cQ+F,\quad \pi=(p-c)Q-F
$$

$$
\widehat p_C=\min(U,\max(L,ec/(e-1)))\quad(e>1,c>0)
$$

$$
[L,U_{new}]\subseteq[L,U_{old}]\;\Longrightarrow\;\max\pi_{new}\leq\max\pi_{old}
$$

### Calculated results and before-and-after comparison

| Scenario | Demand model | Optimal price set | Units/week | Revenue/week | Total cost/week | Profit/week |
| --- | --- | --- | --- | --- | --- | --- |
| Upper price £15 (baseline) | Linear | £10.50 | 90 | £945.00 | £540.00 | £405.00 |
| Upper price £15 (baseline) | Constant elasticity | £12.00 | 69.4444 | £833.33 | £416.67 | £416.67 |
| Upper price £11 | Linear | £10.50 | 90 | £945.00 | £540.00 | £405.00 |
| Upper price £11 | Constant elasticity | £11.00 | 82.6446 | £909.09 | £495.87 | £413.22 |

### Changes from each model's baseline

| Scenario | Demand model | Δ price | Δ units/week | Δ revenue/week | Δ profit/week |
| --- | --- | --- | --- | --- | --- |
| Upper price £15 (baseline) | Linear | £0.00 | +0.0000 | £0.00 | £0.00 |
| Upper price £15 (baseline) | Constant elasticity | £0.00 | +0.0000 | £0.00 | £0.00 |
| Upper price £11 | Linear | £0.00 | +0.0000 | £0.00 | £0.00 |
| Upper price £11 | Constant elasticity | −£1.00 | +13.2002 | +£75.76 | −£3.44 |

Calculations use unrounded values. Currency is displayed to two decimal places and quantity to four where needed. An interval denotes every equally optimal price; the displayed financial quantities use its smallest representative.

### Worked calculations

#### Linear — Upper price £15 (baseline)

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. a = Q₀(1 + e) = 100(1 + 2) = 300; b = eQ₀/p₀ = 2 × 100/10 = 20. Thus Q(p) = max(0, 300 − 20p).
3. The zero-demand cutoff is z = a/b = 300/20 = 15. For p < 15, π(p) = (p − 6)(300 − 20p) − 0.
4. On this positive-demand part, π′(p) = a + bc − 2bp = 420 − 40p. Setting π′ = 0 gives v = (z + c)/2 = (15 + 6)/2 = 10.5.
5. v = 10.5 is permitted and below z = 15. π″ = −2b = −40 < 0, so it is the strict maximum on the positive-demand piece; compare it with the boundaries and plateau.
6. Candidate comparison: p = 1: π = −£1,400.00; p = 10.5: π = £405.00; p = 15: π = £0.00.
7. Every permitted zero-demand price in [£15.00, £15.00] gives Q = 0, contribution = £0.00 and π = −F = £0.00. Compare this entire plateau with the positive-demand candidates.
8. Selected quantity: Q(10.5) = max(0, 300 − 20 × 10.5) = 90 units/week.
9. Full profit-maximising price set: £10.50. This maximum is classified as interior.
10. R = pQ = 10.5 × 90 = £945.00/week; VC = cQ = 6 × 90 = £540.00/week; TC = VC + F = £540.00 + £0.00 = £540.00/week.
11. Contribution = (p−c)Q = (10.5 − 6) × 90 = £405.00/week. Operating profit π = R−TC = £945.00 − £540.00 = £405.00/week.
12. Change from this model's baseline: price £0.00; quantity +0.0000 units/week; revenue £0.00/week; profit £0.00/week. Differences use unrounded calculations.

#### Constant elasticity — Upper price £15 (baseline)

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. Q(p) = 100(p/10)^(−2). π(p) = (p − 6) × 100(p/10)^(−2) − 0.
3. Write K = Q₀p₀^e > 0. Differentiation gives π′(p) = Kp^(−e−1)[(1−e)p + ec] = Kp^(−3)[(-1)p + 12]. The first factor is positive, so the bracket decides whether profit rises or falls.
4. v = ec/(e−1) = 2 × 6/(2 − 1) = 12. The derivative is positive below v and negative above v, proving a global maximum over positive prices.
5. The candidate lies strictly inside the permitted interval. π″(v) = K(1−e)v^(−e−1) < 0 because 1−e = -1 < 0.
6. Candidate comparison: p = 1: π = −£50,000.00; p = 12: π = £416.67; p = 15: π = £400.00.
7. Selected quantity: Q(12) = 100 × (12/10)^(−2) = 69.4444 units/week.
8. Full profit-maximising price set: £12.00. This maximum is classified as interior.
9. R = pQ = 12 × 69.444444 = £833.33/week; VC = cQ = 6 × 69.444444 = £416.67/week; TC = VC + F = £416.67 + £0.00 = £416.67/week.
10. Contribution = (p−c)Q = (12 − 6) × 69.444444 = £416.67/week. Operating profit π = R−TC = £833.33 − £416.67 = £416.67/week.
11. Change from this model's baseline: price £0.00; quantity +0.0000 units/week; revenue £0.00/week; profit £0.00/week. Differences use unrounded calculations.

#### Linear — Upper price £11

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £11.00].
2. a = Q₀(1 + e) = 100(1 + 2) = 300; b = eQ₀/p₀ = 2 × 100/10 = 20. Thus Q(p) = max(0, 300 − 20p).
3. The zero-demand cutoff is z = a/b = 300/20 = 15. For p < 15, π(p) = (p − 6)(300 − 20p) − 0.
4. On this positive-demand part, π′(p) = a + bc − 2bp = 420 − 40p. Setting π′ = 0 gives v = (z + c)/2 = (15 + 6)/2 = 10.5.
5. v = 10.5 is permitted and below z = 15. π″ = −2b = −40 < 0, so it is the strict maximum on the positive-demand piece; compare it with the boundaries and plateau.
6. Candidate comparison: p = 1: π = −£1,400.00; p = 10.5: π = £405.00; p = 11: π = £400.00.
7. Selected quantity: Q(10.5) = max(0, 300 − 20 × 10.5) = 90 units/week.
8. Full profit-maximising price set: £10.50. This maximum is classified as interior.
9. R = pQ = 10.5 × 90 = £945.00/week; VC = cQ = 6 × 90 = £540.00/week; TC = VC + F = £540.00 + £0.00 = £540.00/week.
10. Contribution = (p−c)Q = (10.5 − 6) × 90 = £405.00/week. Operating profit π = R−TC = £945.00 − £540.00 = £405.00/week.
11. Change from this model's baseline: price £0.00; quantity +0.0000 units/week; revenue £0.00/week; profit £0.00/week. Differences use unrounded calculations.

#### Constant elasticity — Upper price £11

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £11.00].
2. Q(p) = 100(p/10)^(−2). π(p) = (p − 6) × 100(p/10)^(−2) − 0.
3. Write K = Q₀p₀^e > 0. Differentiation gives π′(p) = Kp^(−e−1)[(1−e)p + ec] = Kp^(−3)[(-1)p + 12]. The first factor is positive, so the bracket decides whether profit rises or falls.
4. v = ec/(e−1) = 2 × 6/(2 − 1) = 12. The derivative is positive below v and negative above v, proving a global maximum over positive prices.
5. Restricting the candidate to the interval gives min(11, max(1, 12)) = 11. The maximum is at a permitted boundary; its derivative need not be zero.
6. Candidate comparison: p = 1: π = −£50,000.00; p = 11: π = £413.22.
7. Selected quantity: Q(11) = 100 × (11/10)^(−2) = 82.6446 units/week.
8. Full profit-maximising price set: £11.00. This maximum is classified as upper boundary.
9. R = pQ = 11 × 82.644628 = £909.09/week; VC = cQ = 6 × 82.644628 = £495.87/week; TC = VC + F = £495.87 + £0.00 = £495.87/week.
10. Contribution = (p−c)Q = (11 − 6) × 82.644628 = £413.22/week. Operating profit π = R−TC = £909.09 − £495.87 = £413.22/week.
11. Change from this model's baseline: price −£1.00; quantity +13.2002 units/week; revenue +£75.76/week; profit −£3.44/week. Differences use unrounded calculations.

### Interpretation of findings

Linear: the new cap does not bind; price £10.50 → £10.50, quantity 90 → 90 units/week (change +0.0000), revenue £945.00 → £945.00 (change £0.00), profit £405.00 → £405.00/week (change £0.00); Constant elasticity: the new cap binds; price £12.00 → £11.00, quantity 69.4444 → 82.6446 units/week (change +13.2002), revenue £833.33 → £909.09 (change +£75.76), profit £416.67 → £413.22/week (change −£3.44). The cap is tested against each model's original optimum, rather than assumed to affect both equally.

### Financial implications

Under constant-elasticity demand, lowering the cap costs £3.44 of weekly optimised profit while revenue changes by +£75.76. More revenue can accompany less profit because additional sales incur unit costs and the selling margin falls. This distinction matters when assessing a regulated price, discount ceiling or internal pricing policy.

### Conclusion

The linear optimum remains £10.50; the constant-elasticity optimum moves from £12.00 to £11.00. The same price restriction has different financial consequences because the demand curves imply different unconstrained optima.

### Limitations and further investigation

The restriction changes only the permitted price interval. It does not model shortages, quality changes, competitors or how a real business would respond outside pricing. A follow-up is to compare several caps with capacity and minimum viable profit requirements.

## 4. Fixed cost and operating profit

### Economic question

Does a higher unavoidable fixed cost change the entire set of optimal operating prices, or only the resulting profit?

### Starting assumptions and variables

Changed: Weekly fixed cost F rises from £0.00 to £50.00 (increase £50.00).

Held constant: p₀ = £10.00, Q₀ = 100 units/week; e = 2, c = £6.00/unit, permitted prices £1.00–£15.00.

### Theoretical prediction

Subtracting the same additional fixed cost at every permitted price shifts the profit curve down without changing which prices maximise it. The full optimal price set, demand, revenue and contribution therefore remain the same, while operating profit falls by the fixed-cost increase.

### Mathematical reasoning

$$
Q_L(p)=\max(0,a-bp),\quad a=Q_0(1+e),\quad b=\frac{eQ_0}{p_0}
$$

$$
Q_C(p)=Q_0(p/p_0)^{-e}
$$

$$
R=pQ,\quad TC=cQ+F,\quad \pi=(p-c)Q-F
$$

$$
\pi(p;F+\Delta F)=\pi(p;F)-\Delta F
$$

$$
\operatorname{argmax}_{p\in[L,U]}\pi(p;F+\Delta F)=\operatorname{argmax}_{p\in[L,U]}\pi(p;F)
$$

### Calculated results and before-and-after comparison

| Scenario | Demand model | Optimal price set | Units/week | Revenue/week | Total cost/week | Profit/week |
| --- | --- | --- | --- | --- | --- | --- |
| F = £0 (baseline) | Linear | £10.50 | 90 | £945.00 | £540.00 | £405.00 |
| F = £0 (baseline) | Constant elasticity | £12.00 | 69.4444 | £833.33 | £416.67 | £416.67 |
| F = £50 | Linear | £10.50 | 90 | £945.00 | £590.00 | £355.00 |
| F = £50 | Constant elasticity | £12.00 | 69.4444 | £833.33 | £466.67 | £366.67 |

### Changes from each model's baseline

| Scenario | Demand model | Δ price | Δ units/week | Δ revenue/week | Δ profit/week |
| --- | --- | --- | --- | --- | --- |
| F = £0 (baseline) | Linear | £0.00 | +0.0000 | £0.00 | £0.00 |
| F = £0 (baseline) | Constant elasticity | £0.00 | +0.0000 | £0.00 | £0.00 |
| F = £50 | Linear | £0.00 | +0.0000 | £0.00 | −£50.00 |
| F = £50 | Constant elasticity | £0.00 | +0.0000 | £0.00 | −£50.00 |

Calculations use unrounded values. Currency is displayed to two decimal places and quantity to four where needed. An interval denotes every equally optimal price; the displayed financial quantities use its smallest representative.

### Worked calculations

#### Linear — F = £0 (baseline)

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. a = Q₀(1 + e) = 100(1 + 2) = 300; b = eQ₀/p₀ = 2 × 100/10 = 20. Thus Q(p) = max(0, 300 − 20p).
3. The zero-demand cutoff is z = a/b = 300/20 = 15. For p < 15, π(p) = (p − 6)(300 − 20p) − 0.
4. On this positive-demand part, π′(p) = a + bc − 2bp = 420 − 40p. Setting π′ = 0 gives v = (z + c)/2 = (15 + 6)/2 = 10.5.
5. v = 10.5 is permitted and below z = 15. π″ = −2b = −40 < 0, so it is the strict maximum on the positive-demand piece; compare it with the boundaries and plateau.
6. Candidate comparison: p = 1: π = −£1,400.00; p = 10.5: π = £405.00; p = 15: π = £0.00.
7. Every permitted zero-demand price in [£15.00, £15.00] gives Q = 0, contribution = £0.00 and π = −F = £0.00. Compare this entire plateau with the positive-demand candidates.
8. Selected quantity: Q(10.5) = max(0, 300 − 20 × 10.5) = 90 units/week.
9. Full profit-maximising price set: £10.50. This maximum is classified as interior.
10. R = pQ = 10.5 × 90 = £945.00/week; VC = cQ = 6 × 90 = £540.00/week; TC = VC + F = £540.00 + £0.00 = £540.00/week.
11. Contribution = (p−c)Q = (10.5 − 6) × 90 = £405.00/week. Operating profit π = R−TC = £945.00 − £540.00 = £405.00/week.
12. Change from this model's baseline: price £0.00; quantity +0.0000 units/week; revenue £0.00/week; profit £0.00/week. Differences use unrounded calculations.

#### Constant elasticity — F = £0 (baseline)

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £6.00/unit, F = £0.00/week; permitted p ∈ [£1.00, £15.00].
2. Q(p) = 100(p/10)^(−2). π(p) = (p − 6) × 100(p/10)^(−2) − 0.
3. Write K = Q₀p₀^e > 0. Differentiation gives π′(p) = Kp^(−e−1)[(1−e)p + ec] = Kp^(−3)[(-1)p + 12]. The first factor is positive, so the bracket decides whether profit rises or falls.
4. v = ec/(e−1) = 2 × 6/(2 − 1) = 12. The derivative is positive below v and negative above v, proving a global maximum over positive prices.
5. The candidate lies strictly inside the permitted interval. π″(v) = K(1−e)v^(−e−1) < 0 because 1−e = -1 < 0.
6. Candidate comparison: p = 1: π = −£50,000.00; p = 12: π = £416.67; p = 15: π = £400.00.
7. Selected quantity: Q(12) = 100 × (12/10)^(−2) = 69.4444 units/week.
8. Full profit-maximising price set: £12.00. This maximum is classified as interior.
9. R = pQ = 12 × 69.444444 = £833.33/week; VC = cQ = 6 × 69.444444 = £416.67/week; TC = VC + F = £416.67 + £0.00 = £416.67/week.
10. Contribution = (p−c)Q = (12 − 6) × 69.444444 = £416.67/week. Operating profit π = R−TC = £833.33 − £416.67 = £416.67/week.
11. Change from this model's baseline: price £0.00; quantity +0.0000 units/week; revenue £0.00/week; profit £0.00/week. Differences use unrounded calculations.

#### Linear — F = £50

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £6.00/unit, F = £50.00/week; permitted p ∈ [£1.00, £15.00].
2. a = Q₀(1 + e) = 100(1 + 2) = 300; b = eQ₀/p₀ = 2 × 100/10 = 20. Thus Q(p) = max(0, 300 − 20p).
3. The zero-demand cutoff is z = a/b = 300/20 = 15. For p < 15, π(p) = (p − 6)(300 − 20p) − 50.
4. On this positive-demand part, π′(p) = a + bc − 2bp = 420 − 40p. Setting π′ = 0 gives v = (z + c)/2 = (15 + 6)/2 = 10.5.
5. v = 10.5 is permitted and below z = 15. π″ = −2b = −40 < 0, so it is the strict maximum on the positive-demand piece; compare it with the boundaries and plateau.
6. Candidate comparison: p = 1: π = −£1,450.00; p = 10.5: π = £355.00; p = 15: π = −£50.00.
7. Every permitted zero-demand price in [£15.00, £15.00] gives Q = 0, contribution = £0.00 and π = −F = −£50.00. Compare this entire plateau with the positive-demand candidates.
8. Selected quantity: Q(10.5) = max(0, 300 − 20 × 10.5) = 90 units/week.
9. Full profit-maximising price set: £10.50. This maximum is classified as interior.
10. R = pQ = 10.5 × 90 = £945.00/week; VC = cQ = 6 × 90 = £540.00/week; TC = VC + F = £540.00 + £50.00 = £590.00/week.
11. Contribution = (p−c)Q = (10.5 − 6) × 90 = £405.00/week. Operating profit π = R−TC = £945.00 − £590.00 = £355.00/week.
12. Change from this model's baseline: price £0.00; quantity +0.0000 units/week; revenue £0.00/week; profit −£50.00/week. Differences use unrounded calculations.

#### Constant elasticity — F = £50

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £6.00/unit, F = £50.00/week; permitted p ∈ [£1.00, £15.00].
2. Q(p) = 100(p/10)^(−2). π(p) = (p − 6) × 100(p/10)^(−2) − 50.
3. Write K = Q₀p₀^e > 0. Differentiation gives π′(p) = Kp^(−e−1)[(1−e)p + ec] = Kp^(−3)[(-1)p + 12]. The first factor is positive, so the bracket decides whether profit rises or falls.
4. v = ec/(e−1) = 2 × 6/(2 − 1) = 12. The derivative is positive below v and negative above v, proving a global maximum over positive prices.
5. The candidate lies strictly inside the permitted interval. π″(v) = K(1−e)v^(−e−1) < 0 because 1−e = -1 < 0.
6. Candidate comparison: p = 1: π = −£50,050.00; p = 12: π = £366.67; p = 15: π = £350.00.
7. Selected quantity: Q(12) = 100 × (12/10)^(−2) = 69.4444 units/week.
8. Full profit-maximising price set: £12.00. This maximum is classified as interior.
9. R = pQ = 12 × 69.444444 = £833.33/week; VC = cQ = 6 × 69.444444 = £416.67/week; TC = VC + F = £416.67 + £50.00 = £466.67/week.
10. Contribution = (p−c)Q = (12 − 6) × 69.444444 = £416.67/week. Operating profit π = R−TC = £833.33 − £466.67 = £366.67/week.
11. Change from this model's baseline: price £0.00; quantity +0.0000 units/week; revenue £0.00/week; profit −£50.00/week. Differences use unrounded calculations.

### Interpretation of findings

Linear: optimal price set £10.50 → £10.50; quantity 90 → 90 units/week; revenue £945.00 → £945.00; contribution £405.00 → £405.00; profit £405.00 → £355.00/week (change −£50.00); Constant elasticity: optimal price set £12.00 → £12.00; quantity 69.4444 → 69.4444 units/week; revenue £833.33 → £833.33; contribution £416.67 → £416.67; profit £416.67 → £366.67/week (change −£50.00). The algebra establishes invariance of every tied maximiser as well as the displayed representative price.

### Financial implications

Maximum contribution is also the fixed-cost level at which optimised operating profit becomes zero: Linear can cover £405.00/week of unavoidable fixed costs under these demand and variable-cost assumptions; Constant elasticity can cover £416.67/week of unavoidable fixed costs under these demand and variable-cost assumptions. A pricing optimum answers how best to operate within the model; it does not by itself establish whether operating or closing is the better business decision.

### Conclusion

Increasing fixed cost by £50.00/week reduces each model's optimised profit by £50.00/week and preserves its entire optimal price set. Fixed costs affect profitability and cost coverage, even when they do not change the optimal selling price.

### Limitations and further investigation

Fixed costs are assumed unavoidable for the period, including when no units are sold. A shutdown or investment decision needs separate information on avoidable costs, sunk costs and future periods; it cannot be inferred from this pricing calculation alone.

## 5. High cost and zero-demand plateau

### Economic question

When unit cost exceeds the linear zero-demand cutoff, what prices minimise the operating loss, and how does the constant-elasticity model differ?

### Starting assumptions and variables

Changed: Unit cost c rises from £6.00 to £20.00/unit.

Held constant: p₀ = £10.00, Q₀ = 100 units/week; e = 2, F = £50.00/week, permitted prices £1.00–£20.00.

### Theoretical prediction

If linear demand is positive only below a cutoff that is already below unit cost, every positive-demand price loses contribution. Any permitted zero-demand price avoids that variable loss and ties at profit −F. Constant-elasticity demand has no finite zero-demand cutoff, so it need not have this plateau.

### Mathematical reasoning

$$
Q_L(p)=\max(0,a-bp),\quad a=Q_0(1+e),\quad b=\frac{eQ_0}{p_0}
$$

$$
Q_C(p)=Q_0(p/p_0)^{-e}
$$

$$
R=pQ,\quad TC=cQ+F,\quad \pi=(p-c)Q-F
$$

$$
c\geq z,\ p<z\;\Longrightarrow\;(p-c)Q_L(p)<0
$$

$$
p\geq z\;\Longrightarrow\;Q_L=0,\ \pi_L=-F
$$

### Calculated results and before-and-after comparison

| Scenario | Demand model | Optimal price set | Units/week | Revenue/week | Total cost/week | Profit/week |
| --- | --- | --- | --- | --- | --- | --- |
| c = £6 (baseline) | Linear | £10.50 | 90 | £945.00 | £590.00 | £355.00 |
| c = £6 (baseline) | Constant elasticity | £12.00 | 69.4444 | £833.33 | £466.67 | £366.67 |
| c = £20 | Linear | [£15.00, £20.00] | 0 | £0.00 | £50.00 | −£50.00 |
| c = £20 | Constant elasticity | £20.00 | 25 | £500.00 | £550.00 | −£50.00 |

### Changes from each model's baseline

| Scenario | Demand model | Δ price | Δ units/week | Δ revenue/week | Δ profit/week |
| --- | --- | --- | --- | --- | --- |
| c = £6 (baseline) | Linear | £0.00 | +0.0000 | £0.00 | £0.00 |
| c = £6 (baseline) | Constant elasticity | £0.00 | +0.0000 | £0.00 | £0.00 |
| c = £20 | Linear | +£4.50 | -90.0000 | −£945.00 | −£405.00 |
| c = £20 | Constant elasticity | +£8.00 | -44.4444 | −£333.33 | −£416.67 |

Calculations use unrounded values. Currency is displayed to two decimal places and quantity to four where needed. An interval denotes every equally optimal price; the displayed financial quantities use its smallest representative.

### Worked calculations

#### Linear — c = £6 (baseline)

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £6.00/unit, F = £50.00/week; permitted p ∈ [£1.00, £20.00].
2. a = Q₀(1 + e) = 100(1 + 2) = 300; b = eQ₀/p₀ = 2 × 100/10 = 20. Thus Q(p) = max(0, 300 − 20p).
3. The zero-demand cutoff is z = a/b = 300/20 = 15. For p < 15, π(p) = (p − 6)(300 − 20p) − 50.
4. On this positive-demand part, π′(p) = a + bc − 2bp = 420 − 40p. Setting π′ = 0 gives v = (z + c)/2 = (15 + 6)/2 = 10.5.
5. v = 10.5 is permitted and below z = 15. π″ = −2b = −40 < 0, so it is the strict maximum on the positive-demand piece; compare it with the boundaries and plateau.
6. Candidate comparison: p = 1: π = −£1,450.00; p = 10.5: π = £355.00; p = 15: π = −£50.00; p = 20: π = −£50.00.
7. Every permitted zero-demand price in [£15.00, £20.00] gives Q = 0, contribution = £0.00 and π = −F = −£50.00. Compare this entire plateau with the positive-demand candidates.
8. Selected quantity: Q(10.5) = max(0, 300 − 20 × 10.5) = 90 units/week.
9. Full profit-maximising price set: £10.50. This maximum is classified as interior.
10. R = pQ = 10.5 × 90 = £945.00/week; VC = cQ = 6 × 90 = £540.00/week; TC = VC + F = £540.00 + £50.00 = £590.00/week.
11. Contribution = (p−c)Q = (10.5 − 6) × 90 = £405.00/week. Operating profit π = R−TC = £945.00 − £590.00 = £355.00/week.
12. Change from this model's baseline: price £0.00; quantity +0.0000 units/week; revenue £0.00/week; profit £0.00/week. Differences use unrounded calculations.

#### Constant elasticity — c = £6 (baseline)

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £6.00/unit, F = £50.00/week; permitted p ∈ [£1.00, £20.00].
2. Q(p) = 100(p/10)^(−2). π(p) = (p − 6) × 100(p/10)^(−2) − 50.
3. Write K = Q₀p₀^e > 0. Differentiation gives π′(p) = Kp^(−e−1)[(1−e)p + ec] = Kp^(−3)[(-1)p + 12]. The first factor is positive, so the bracket decides whether profit rises or falls.
4. v = ec/(e−1) = 2 × 6/(2 − 1) = 12. The derivative is positive below v and negative above v, proving a global maximum over positive prices.
5. The candidate lies strictly inside the permitted interval. π″(v) = K(1−e)v^(−e−1) < 0 because 1−e = -1 < 0.
6. Candidate comparison: p = 1: π = −£50,050.00; p = 12: π = £366.67; p = 20: π = £300.00.
7. Selected quantity: Q(12) = 100 × (12/10)^(−2) = 69.4444 units/week.
8. Full profit-maximising price set: £12.00. This maximum is classified as interior.
9. R = pQ = 12 × 69.444444 = £833.33/week; VC = cQ = 6 × 69.444444 = £416.67/week; TC = VC + F = £416.67 + £50.00 = £466.67/week.
10. Contribution = (p−c)Q = (12 − 6) × 69.444444 = £416.67/week. Operating profit π = R−TC = £833.33 − £466.67 = £366.67/week.
11. Change from this model's baseline: price £0.00; quantity +0.0000 units/week; revenue £0.00/week; profit £0.00/week. Differences use unrounded calculations.

#### Linear — c = £20

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £20.00/unit, F = £50.00/week; permitted p ∈ [£1.00, £20.00].
2. a = Q₀(1 + e) = 100(1 + 2) = 300; b = eQ₀/p₀ = 2 × 100/10 = 20. Thus Q(p) = max(0, 300 − 20p).
3. The zero-demand cutoff is z = a/b = 300/20 = 15. For p < 15, π(p) = (p − 20)(300 − 20p) − 50.
4. On this positive-demand part, π′(p) = a + bc − 2bp = 700 − 40p. Setting π′ = 0 gives v = (z + c)/2 = (15 + 20)/2 = 17.5.
5. The candidate 17.5 is at or beyond the cutoff, where the positive-demand quadratic no longer applies. It cannot be used as an interior positive-demand maximum.
6. Candidate comparison: p = 1: π = −£5,370.00; p = 15: π = −£50.00; p = 20: π = −£50.00.
7. Every permitted zero-demand price in [£15.00, £20.00] gives Q = 0, contribution = £0.00 and π = −F = −£50.00. Compare this entire plateau with the positive-demand candidates.
8. Selected quantity: Q(15) = max(0, 300 − 20 × 15) = 0 units/week.
9. Full profit-maximising price set: [£15.00, £20.00]. The displayed price £15.00 is the smallest representative of a tied set.
10. R = pQ = 15 × 0 = £0.00/week; VC = cQ = 20 × 0 = £0.00/week; TC = VC + F = £0.00 + £50.00 = £50.00/week.
11. Contribution = (p−c)Q = (15 − 20) × 0 = £0.00/week. Operating profit π = R−TC = £0.00 − £50.00 = −£50.00/week.
12. Change from this model's baseline: price +£4.50; quantity -90.0000 units/week; revenue −£945.00/week; profit −£405.00/week. Differences use unrounded calculations.

#### Constant elasticity — c = £20

1. Inputs: p₀ = £10.00, Q₀ = 100 units/week, e = 2, c = £20.00/unit, F = £50.00/week; permitted p ∈ [£1.00, £20.00].
2. Q(p) = 100(p/10)^(−2). π(p) = (p − 20) × 100(p/10)^(−2) − 50.
3. Write K = Q₀p₀^e > 0. Differentiation gives π′(p) = Kp^(−e−1)[(1−e)p + ec] = Kp^(−3)[(-1)p + 40]. The first factor is positive, so the bracket decides whether profit rises or falls.
4. v = ec/(e−1) = 2 × 20/(2 − 1) = 40. The derivative is positive below v and negative above v, proving a global maximum over positive prices.
5. Restricting the candidate to the interval gives min(20, max(1, 40)) = 20. The maximum is at a permitted boundary; its derivative need not be zero.
6. Candidate comparison: p = 1: π = −£190,050.00; p = 20: π = −£50.00.
7. Selected quantity: Q(20) = 100 × (20/10)^(−2) = 25 units/week.
8. Full profit-maximising price set: £20.00. This maximum is classified as upper boundary.
9. R = pQ = 20 × 25 = £500.00/week; VC = cQ = 20 × 25 = £500.00/week; TC = VC + F = £500.00 + £50.00 = £550.00/week.
10. Contribution = (p−c)Q = (20 − 20) × 25 = £0.00/week. Operating profit π = R−TC = £500.00 − £550.00 = −£50.00/week.
11. Change from this model's baseline: price +£8.00; quantity -44.4444 units/week; revenue −£333.33/week; profit −£416.67/week. Differences use unrounded calculations.

### Interpretation of findings

The calculated cutoff is £15.00, below unit cost £20.00. Linear optimal prices form the complete interval [£15.00, £20.00]; the displayed £15.00 is only its smallest representative. Each of those prices gives zero demand, zero revenue, zero contribution and profit −£50.00/week. Constant elasticity instead selects £20.00, with 25 units/week, revenue £500.00, contribution £0.00 and profit −£50.00/week. Before-and-after comparison: Linear: price £10.50 → £15.00, quantity 90 → 0, revenue £945.00 → £0.00, profit £355.00 → −£50.00/week (change −£405.00); Constant elasticity: price £12.00 → £20.00, quantity 69.4444 → 25, revenue £833.33 → £500.00, profit £366.67 → −£50.00/week (change −£416.67).

### Financial implications

The cost rise removes positive contribution at every permitted price in this example. Under linear demand, charging any price in [£15.00, £20.00] minimises the loss at the unavoidable fixed cost of £50.00/week. Under constant-elasticity demand, the selected price equals unit cost £20.00, so sales exactly cover their variable cost and contribute nothing towards fixed costs. The financial outcome is a loss even though a mathematically optimal price exists.

### Conclusion

Both models' best operating profit is −£50.00/week here, but the mechanisms differ: a complete zero-demand price plateau for linear demand versus positive sales at zero unit margin for constant-elasticity demand. A single displayed price would conceal the linear model's set of equally good solutions.

### Limitations and further investigation

Zero sales do not remove unavoidable fixed costs in this model. Whether to stop trading, change suppliers or redesign the product requires costs and alternatives outside the permitted-price calculation. Demand far from the reference price also needs empirical validation.

## Overall financial assessment

The appropriate selling price depends on the chosen objective, the full assumed demand curve, unit costs and permitted prices. Local agreement at the starting price is not enough to guarantee the same financial recommendation. Unit-cost changes affect the marginal trade-off between margin and quantity; unavoidable fixed costs affect cost coverage but do not alter any maximising operating price. A binding price restriction can lower profit even when it increases sales revenue. Reporting full tied sets avoids suggesting a unique answer when the mathematics produces a plateau.

The next commercially useful step is to collect price and sales evidence, estimate demand over a credible range, include uncertainty and realistic capacity or cost constraints, and compare model recommendations under those alternatives. Simulated maxima do not establish how real customers or competitors will behave.

## Methodology

AI assisted with code development and explanatory drafting. Results are calculated deterministically from the displayed mathematical models and checked by automated tests and separate equation-based calculations. These software checks do not establish which checks the project owner has personally completed.
