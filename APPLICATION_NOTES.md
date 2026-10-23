# Application and interview notes

These are draft application materials based on the finished software. They do not establish which code, calculations or explanations Will personally produced or checked. The project was developed with AI assistance; deterministic calculations and automated tests are separate from personal understanding. Adapt the wording to your actual contribution and complete the personal checklist below before using it. These notes belong outside the public dashboard and completed findings report.

## Two concise finance-CV bullets

- Mathematical pricing investigation comparing matched demand curves, bounded profit maxima and five controlled investigations of elasticity, costs and price restrictions.
- Evaluated chosen prices and model risk; hypothetical benchmark profit maxima of £405–£416.67 per week, supported by mathematical and independent numerical checks.

These describe the project's completed functionality. If using an action verb such as “developed” or “implemented”, qualify it to reflect your own work and the assistance received. The profit figures are model outputs, not business savings.

## Draft personal-statement project paragraph

**Draft for a Maths or Mathematics & Economics application; verify that you can explain every statement and describe your contribution accurately.**

My pricing project compares linear and constant-elasticity demand curves that match quantity, slope and elasticity at a starting price. Despite this local agreement, they imply different profit-maximising prices: £10.50 and £12 under the illustrative benchmark. The investigation uses derivatives, endpoint comparisons and a separate numerical search, including cases with binding price limits or several optimal prices. Comparing each suggested price under both curves makes the financial consequence of the demand assumption explicit. The central distinction is between proving an optimum within stated assumptions and establishing whether those assumptions describe a real business; neither curve has been validated against customer data.

## A 60-second explanation

The project asks how the assumed relationship between price and demand changes the profit-maximising price. It compares two hypothetical demand curves with the same quantity, slope and elasticity at £10, so their different results come from how their shapes diverge elsewhere. With unit cost £6 and prices restricted to £1–£15, linear demand gives an optimum of £10.50 and weekly profit £405. Constant elasticity gives £12 and about £416.67. Both use illustrative assumptions, rather than fitted customer data. The project checks derivatives, endpoints and zero-demand regions, then compares the result with a separate numerical search. It also evaluates a chosen price and measures how much model-implied profit is lost if the other curve describes demand. For example, charging £12 under linear demand gives £45 less profit than its maximum. The financial lesson is that an exact mathematical optimum can still depend heavily on an unvalidated economic assumption.

Practise this aloud and shorten it to your natural speaking pace. Do not describe the automated checks as handwritten checks you personally completed.

## Six likely follow-up questions

### 1. Why match the models at the starting price?

It gives a common local comparison. Both have quantity $Q_0$, slope $-eQ_0/p_0$ and elasticity magnitude $e$ at $p_0$. This does not make them equivalent elsewhere: linear demand has constant slope and a cutoff, while constant-elasticity demand curves upward and stays positive. Linear elasticity changes with price.

### 2. How do you know that a stationary point is a maximum?

For positive linear demand, profit is a quadratic with second derivative $-2b<0$. The constant-elasticity profit derivative changes from positive to negative at $ec/(e-1)$ when $e>1,c>0$. The permitted endpoints and linear cutoff/plateau must still be checked. A separate numerical search checks the calculated optimum without being given the analytical answer; passing software tests does not validate the demand assumptions.

### 3. Does the higher constant-elasticity profit show that it is the better model?

No. Each maximum assumes its own curve is true. At the benchmark, the constant-elasticity suggestion of £12 earns £360 under linear demand, £45 below the linear maximum. The linear suggestion of £10.50 earns about £408.16 under constant elasticity, about £8.50 below that model's maximum. This comparison exposes consequences of model choice; it supplies no evidence or probabilities about which curve is accurate.

### 4. Why not maximise revenue instead?

Revenue omits costs. Linear benchmark revenue is highest at £7.50, with £1,125 revenue but only £225 profit; its profit optimum earns £405. Constant elasticity predicts 10,000 units at £1, £10,000 revenue and a £50,000 loss. That extreme is a warning about extrapolated demand and missing capacity constraints, not a realistic sales forecast.

### 5. Why does adding £50 fixed cost leave the price unchanged?

When fixed cost is unavoidable and the feasible interval stays the same, it subtracts £50 from profit at every price. Every ordering and tie is preserved, so the entire optimal-price set is unchanged. This is an operating-price result; deciding whether to close requires avoidable-cost and alternative-use information that the project does not supply.

### 6. When does the usual constant-elasticity optimum formula fail?

The positive interior formula $p^*=ec/(e-1)$ requires $e>1,c>0$, and the candidate must lie inside the permitted interval. For $e=1,c>0$, profit increases towards a finite limiting value without attaining an unrestricted maximum; the bounded answer is the upper endpoint. For $e=1,c=0$, all permitted prices tie. The model does not force a stationary formula onto these cases.

## Short benchmark derivation

All figures use pounds per unit and units/profit per week, with $p_0=10$, $Q_0=100$, $e=2$, $c=6$, $F=0$ and $[L,U]=[1,15]$.

1. Linear calibration gives $b=eQ_0/p_0=20$ and $a=Q_0(1+e)=300$. Therefore $Q_L=\max(0,300-20p)$, with cutoff £15.
2. Below the cutoff, $\pi_L=(p-6)(300-20p)$, so $\pi_L'=420-40p$ vanishes at £10.50. The second derivative is −40. Quantity is 90, revenue £945, variable cost £540 and profit £405. Endpoint profits −£1,400 and £0 are smaller.
3. Constant elasticity gives $Q_C=10000/p^2$ and $\pi_C=10000(p-6)/p^2$. Its derivative is $10000(12-p)/p^3$, positive below £12 and negative above. At £12, quantity is $625/9$, revenue $2500/3$, variable cost $1250/3$ and profit $1250/3\approx£416.67$. Endpoint profits −£50,000 and £400 are smaller.
4. Both give starting profit $(10-6)100=£400$. The hypothetical improvements are £5 and about £16.67 per week, conditional on the respective demand curve. At the interior optima, $MR=p+Q/Q'=£6=MC$; that equality is not required at a binding boundary or the linear cutoff.

**A formula that cannot simply be used:** set $e=1,c=6$, keeping $p_0=10$, $Q_0=100$ and $[1,15]$. Then $Q_C=1000/p$ and $\pi_C=1000(1-6/p)-F$, with derivative $6000/p^2>0$. The expression $ec/(e-1)$ would divide by zero. The permitted optimum is £15; unrestricted profit approaches $1000-F$ as price tends to infinity, with no finite maximiser. If unit cost were also zero, every positive price would give the same profit instead.

## Personal understanding and contribution checklist

These tasks are intentionally **unchecked**. Automated verification does not complete them for you.

- [ ] Write down which parts you personally specified, edited, reviewed and explained, and which used AI assistance; amend application wording accordingly.
- [ ] Derive both matched curves and verify their starting quantity, slope and elasticity by hand.
- [ ] Reproduce the £10.50 and £12 benchmark optima, endpoint comparisons and financial quantities without copying the report.
- [ ] Explain why $MR=p+Q/Q'$ differs from $dR/dp$, and why the boundary/cutoff exceptions matter.
- [ ] Recalculate the £45 and approximately £8.50 cross-model profit losses and explain their conditional meaning.
- [ ] Work through one binding-cap case, the $e=1$ counterexample and the high-cost linear plateau $[15,20]$.
- [ ] Change a chosen price in the app, trace its calculation into an export, and explain the handling of zero/negative starting profit and period labels.
- [ ] Explain why own-price sensitivity does not identify a substitution effect, why fixed-cost invariance does not settle shutdown, and why the £1 revenue prediction is implausible.
- [ ] Run the documented checks yourself if you plan to claim that you ran them; record any personal handwritten checks separately.
- [ ] Practise the explanation and six follow-ups in your own words, and describe what evidence or constraints a real pricing decision would additionally need.
