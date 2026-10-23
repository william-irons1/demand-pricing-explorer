# Mathematics behind Demand and Pricing Explorer

> How does the assumed relationship between price and quantity demanded affect the profit-maximising price?

This explanation derives the demand functions, proves the bounded profit maxima, compares revenue and profit objectives, and interprets the five complete financial investigations. The dashboard and downloadable findings calculate results from these equations. The reference examples below use the same model functions and assumptions.

## 1. Definitions, units and the bounded question

| Symbol | Meaning |
|---|---|
| $p$ | Selling price, in pounds per unit. |
| $p_0>0$ | Starting/reference price. |
| $Q_0>0$ | Starting quantity, in continuous units per selected period. |
| $e>0$ | Positive magnitude of elasticity at the starting point. |
| $c\geq0$ | Constant variable cost, in pounds per unit. |
| $F\geq0$ | Unavoidable fixed cost, in pounds per the same period. |
| $0<L<U$ | Shared permitted price interval $[L,U]$. |

The default period is a week. Quantity and fixed cost must refer to that same period, so revenue, total cost and profit are also per week. If you choose another period, provide consistent figures; changing a label alone does not convert them.

The website answers a **bounded** question: maximise operating profit over $[L,U]$. This differs from an unrestricted question over every positive price. Both demand models, and hence both profit functions, are continuous on the finite closed interval, so they attain a maximum there. The set of prices attaining it may contain more than one price.

For either demand function,

$$
R(p)=pQ(p),\quad VC(p)=cQ(p),\quad TC(p)=cQ(p)+F,
$$

$$
\pi(p)=R(p)-TC(p)=(p-c)Q(p)-F.
$$

The expression $(p-c)Q$ is **contribution toward fixed costs**. Positive contribution does not ensure positive profit when $F>0$. No sales means $Q=0$ and profit $-F$, not automatically zero. Deciding whether to shut down requires assumptions about avoidable costs and is outside the project.

## 2. Constructing demand and matching starting conditions

### Linear demand with an explicit cutoff

Set

$$
b=\frac{eQ_0}{p_0}>0,\qquad a=Q_0(1+e),\qquad
Q_L(p)=\max(0,a-bp).
$$

Before the cutoff, this is the earlier matched linear expression

$$
a-bp=Q_0[1-e(p/p_0-1)].
$$

The zero-demand cutoff is

$$
z=\frac{a}{b}=p_0(1+1/e).
$$

For $0<p<z$, demand is positive; for $p\geq z$, demand is zero. The function is continuous at $z$, but its derivative changes from $-b$ on the left to zero on the right. Negative quantities are never used in graphs, profit calculations or optimisation.

### Constant-elasticity demand

$$
Q_C(p)=Q_0(p/p_0)^{-e},\qquad p>0.
$$

Demand is positive at every finite positive price. It has no finite zero-demand cutoff.

### Quantity, slope and elasticity at the starting price

Since $z>p_0$, the starting point is always in the positive-demand part of the linear curve, even if $p_0$ is outside the permitted interval. At $p_0$,

$$
Q_L(p_0)=a-bp_0=Q_0(1+e)-eQ_0=Q_0,
\qquad Q_C(p_0)=Q_0.
$$

Differentiate:

$$
Q_L'(p)=-\frac{eQ_0}{p_0}\quad(p<z),\qquad
Q_C'(p)=-\frac{eQ_0}{p_0}(p/p_0)^{-e-1}.
$$

Both slopes at $p_0$ are $-eQ_0/p_0$.

Price elasticity measures percentage responsiveness of quantity to price; it is usually reported as a magnitude for downward-sloping demand. See [OpenStax, Principles of Economics 3e, §5.1](https://openstax.org/books/principles-economics-3e/pages/5-1-price-elasticity-of-demand-and-price-elasticity-of-supply) for the definition and distinction from slope. The following point-elasticity expression is derived here by taking the small-change limit:

$$
\frac{\Delta Q/Q}{\Delta p/p}\longrightarrow\frac{p}{Q}Q'(p),
\qquad E(p)=-\frac{p}{Q(p)}Q'(p).
$$

It follows that both give $E(p_0)=e$. Away from the starting point,

$$
E_L(p)=\frac{bp}{a-bp}=\frac{ep}{p_0(1+e)-ep}
\quad(0<p<z),\qquad E_C(p)=e.
$$

Linear elasticity is **not constant**. It tends to infinity as $p$ approaches $z$ from below and is undefined when quantity is zero. The zero-demand plateau has zero slope but not a meaningful finite elasticity.

### Why matched models can disagree

They agree in value and first derivative at $p_0$, but not in curvature:

$$
Q_L''(p)=0\quad(p<z),\qquad
Q_C''(p)=\frac{e(e+1)Q_0}{p_0^2}(p/p_0)^{-e-2}>0.
$$

The linear curve is the tangent line to the constant-elasticity curve at $p_0$ until the cutoff applies. The convex constant-elasticity curve lies above that tangent away from the point of contact. Local matching is a fair basis for comparison, but it does not establish global agreement or real-world accuracy.

## 3. Linear profit: stationary point, boundaries and plateau

In the positive-demand region $p<z$,

$$
\pi_L(p)=(p-c)(a-bp)-F
=-bp^2+(a+bc)p-ac-F.
$$

Hence

$$
\pi_L'(p)=a+bc-2bp,
\qquad
v_L=\frac{a+bc}{2b}=\frac{z+c}{2}
=\frac{p_0(1+1/e)+c}{2}.
$$

The second derivative is

$$
\pi_L''(p)=-2b<0.
$$

So a stationary point **inside the positive-demand region** is a strict maximum of that quadratic. It is not automatically the answer to the bounded, clipped problem. Check whether $v_L$ lies in $[L,U]$ and below $z$ before including it.

For $p\geq z$,

$$
Q_L(p)=0,\qquad \pi_L(p)=-F.
$$

This whole segment is a plateau, not a continuation of the quadratic into negative demand.

### A complete candidate comparison

To find the bounded maximum:

1. Evaluate the permitted endpoints $L$ and $U$.
2. Evaluate $v_L$ if it lies in the permitted positive-demand region.
3. Evaluate $z$ if $z\in[L,U]$.
4. If $U\geq z$, include every price in the feasible plateau $[\max(L,z),U]$, all with profit $-F$.
5. Compare values and report the full set of equally best prices, including any optimal plateau.

This finite candidate reasoning is exhaustive: the positive-demand piece is a concave quadratic, and the remaining piece is constant. A stationary point is the only possible interior strict maximum on the quadratic; otherwise the best point on that segment is an endpoint. At the cutoff, ordinary differentiability may fail, so it must be checked separately.

Useful cases:

- If $c<z$ and $v_L$ is permitted, $v_L<z$ gives positive contribution and beats a zero-demand plateau.
- If the interval truncates the increasing or decreasing part of the quadratic, a permitted endpoint can maximise profit.
- If $c\geq z$, every positive-demand price has non-positive margin. Whenever the permitted interval contains zero-demand prices, all of those plateau prices maximise profit at $-F$.
- If $L\geq z$, the entire permitted interval is optimal: every price produces no sales and profit $-F$.
- If the whole permitted interval lies below both unit cost and the cutoff, its best contribution can be negative. A zero-demand option cannot be assumed available outside the stated interval.

For a valid interior stationary price with $c<z$,

$$
Q_L(v_L)=\frac{b}{2}(z-c),\qquad
\pi_L(v_L)=\frac{b}{4}(z-c)^2-F.
$$

These formulas must not be used for a quadratic vertex beyond the cutoff. Over the unrestricted domain $p>0$, the linear model has the unique maximum $v_L$ when $c<z$, and the full optimal plateau $[z,\infty)$ when $c\geq z$.

## 4. Constant-elasticity profit: all supported cases

For algebra, write $K=Q_0p_0^e>0$:

$$
Q_C(p)=Kp^{-e},\qquad
\pi_C(p)=K(p-c)p^{-e}-F.
$$

The product rule gives

$$
\pi_C'(p)=K[p^{-e}-e(p-c)p^{-e-1}]
=Kp^{-e-1}[(1-e)p+ec].
$$

The factor $Kp^{-e-1}$ is positive, so the bracket determines the derivative’s sign.

### Case $e>1$ and $c>0$

The stationary candidate is

$$
v_C=\frac{ec}{e-1}>c.
$$

The bracket is positive below $v_C$ and negative above it. Profit therefore increases then decreases. This proves a unique unrestricted global maximum. As an additional local check,

$$
\pi_C''(v_C)=K(1-e)v_C^{-e-1}<0.
$$

On the shared interval, the unique optimal price is the candidate restricted to its bounds:

$$
\widehat p_C=\min\big(U,\max(L,v_C)\big).
$$

A candidate strictly between $L$ and $U$ is interior; one at or outside a bound gives a boundary maximum. Boundary maxima do not need a zero derivative.

### Cases $0<e<1$ or $e=1,c>0$

For $0<e<1$ and any $c\geq0$, $(1-e)p+ec>0$. Profit is strictly increasing, so $U$ is the unique bounded maximiser.

For $e=1,c>0$,

$$
\pi_C(p)=K(1-c/p)-F,\qquad \pi_C'(p)=Kc/p^2>0.
$$

Again the bounded maximum is at $U$.

### Zero unit cost

If $c=0$,

$$
\pi_C(p)=Kp^{1-e}-F.
$$

It increases for $0<e<1$ (optimum $U$), is constant for $e=1$ (every price in $[L,U]$ is optimal), and decreases for $e>1$ (optimum $L$). The formula $ec/(e-1)$ is inapplicable to the flat case and would give the excluded price zero for $e>1,c=0$.

### Bounded maxima versus unrestricted behaviour

| Assumptions | On the bounded interval $[L,U]$ | On every positive price, with no bounds |
|---|---|---|
| $0<e<1$, $c\geq0$ | Unique optimum $U$. | Contribution tends to infinity as $p\to\infty$; no finite maximiser. |
| $e=1$, $c>0$ | Unique optimum $U$. | Profit approaches $K-F$ from below but never attains it; no finite maximiser. |
| $e=1$, $c=0$ | Entire interval is optimal. | Profit is $K-F$ at every $p>0$; all positive prices are optimal. |
| $e>1$, $c>0$ | Unique candidate restricted to $[L,U]$. | Unique maximum at $ec/(e-1)$. |
| $e>1$, $c=0$ | Unique optimum $L$. | Profit tends to infinity as $p\to0^+$; no finite maximiser. |

For $0<e<1$,

$$
K(p-c)p^{-e}=Kp^{1-e}-Kcp^{-e}\to\infty
\quad(p\to\infty).
$$

For $e=1,c>0$, the finite limiting value $K-F$ is a **supremum**: an upper bound approached but never achieved. For $e>1,c=0$, $Kp^{1-e}-F$ diverges upwards as price approaches zero. These limiting behaviours are limitations of the assumed curve, not practical advice about extreme prices. The app’s finite interval makes each supported calculation well-defined, while retaining a separate explanation of the unrestricted problem.

## 5. Optimal-price sets, fixed cost and scale

Write

$$
S=\operatorname*{arg\,max}_{p\in[L,U]}\pi(p).
$$

This notation means the **set** of all permitted prices earning the maximum profit. It is a single point for a unique optimum, an interval for a plateau, or the whole permitted interval for a flat profit curve. The application displays the set explicitly and can use its smallest price as a representative. Calculated quantity and revenue at that representative are not necessarily shared by all tied prices: in the constant-elasticity flat case $e=1,c=0$, quantities vary even though revenue and profit do not.

Adding fixed cost $\Delta F$ gives

$$
\pi_{\mathrm{new}}(p)=\pi_{\mathrm{old}}(p)-\Delta F.
$$

Subtracting the same constant from every feasible price preserves every ordering and tie, so the **entire argmax set** is unchanged when $[L,U]$ is unchanged. This conclusion includes plateaus and boundary solutions, not just an interior derivative calculation. It does not decide whether operating is worthwhile.

Multiplying $Q_0$ by a positive factor multiplies demand, revenue, variable cost and contribution by that factor. It preserves the optimal-price set. With $F$ held constant, profit becomes scaled contribution minus unchanged $F$; profit itself is not simply multiplied by that factor.

At an interior stationary price with positive demand,

$$
Q+(p-c)Q'=0
\quad\Longrightarrow\quad
\frac{p-c}{p}=\frac{1}{E(p)}.
$$

For constant elasticity this produces $p=ec/(e-1)$ only when the conditions for a positive stationary price hold. For linear demand, use elasticity at the candidate price, not the input $e$, which describes the starting point. This first-order condition does not apply to zero-demand plateaus or, in general, boundary maxima.

### Marginal revenue equals marginal cost: scope and check

Marginal revenue means the change in revenue **per additional unit of quantity**, not the change per pound of price. Where demand is differentiable and $Q'(p)\ne0$,

$$
MR=\frac{dR/dp}{dQ/dp}=\frac{Q+pQ'}{Q'}=p+\frac{Q}{Q'},
\qquad MC=\frac{d(cQ+F)}{dQ}=c.
$$

At a differentiable interior profit optimum with positive demand,

$$
0=\pi'(p)=Q+(p-c)Q'
\quad\Longrightarrow\quad p+\frac{Q}{Q'}=c.
$$

The implementation checks this equality using the evaluated quantity and slope. At the benchmark linear optimum, $MR=10.50+90/(-20)=6$. For constant elasticity, $Q'=-eQ/p$, so $MR=p(1-1/e)=12(1-1/2)=6$. Both agree with unit marginal cost £6, even though their optimal prices differ.

The equality is a necessary first-order condition in this interior setting; the curvature/derivative-sign and full feasible-set arguments above establish maxima. At a binding permitted boundary, equality is not required. At the linear cutoff the derivative has a corner, and on the zero-demand plateau $Q=Q'=0$, so the ratio is undefined. For the flat positive-demand case $e=1,c=0$, $MR=MC=0$ everywhere and does not select a unique price. The dashboard explains these cases instead of labelling them failed equality checks. If finite-precision arithmetic cannot resolve a nonzero slope, it reports that the check is unavailable.

## 6. Generated benchmark calculation

Use $p_0=10$, $Q_0=100$ units per week, $e=2$, $c=6$, $F=0$ per week and common interval $[L,U]=[1,15]$.

### Linear model

$$
a=100(1+2)=300,\qquad b=2(100)/10=20,
\qquad Q_L(p)=\max(0,300-20p).
$$

The cutoff is $z=15$, and the stationary price is

$$
v_L=(300+20\times6)/(2\times20)=10.50.
$$

It lies in $[1,15]$ and below the cutoff. Directly,

$$
\pi_L=(p-6)(300-20p),\quad \pi_L'=420-40p,
\quad \pi_L''=-40.
$$

At £10.50,

$$
Q_L=90,\quad R_L=945,\quad TC_L=540,\quad \pi_L=405.
$$

Endpoint profits are $\pi_L(1)=-1400$ and $\pi_L(15)=0$, so the stationary point is the unique bounded maximum.

### Constant-elasticity model

$$
Q_C(p)=100(p/10)^{-2}=10000/p^2,\qquad
v_C=\frac{2\times6}{2-1}=12.
$$

The stationary price is within $[1,15]$ and has the increase-then-decrease derivative pattern. At £12,

$$
Q_C=\frac{10000}{144}=\frac{625}{9}\approx69.4444,
$$

$$
R_C=\frac{2500}{3}\approx833.3333,\qquad
TC_C=\frac{1250}{3}\approx416.6667,
$$

$$
\pi_C=(12-6)\frac{625}{9}=\frac{1250}{3}\approx416.6667.
$$

Endpoint profits are $\pi_C(1)=-50000$ and $\pi_C(15)=400$, below the interior result. At the starting £10, both models give quantity 100, revenue £1,000, total cost £600 and profit £400. Different optimum predictions demonstrate sensitivity to assumed demand shape; they do not establish which model is more accurate for a real business.

### Comparing a chosen permitted price

For a chosen $p_t\in[L,U]$, the dashboard evaluates the starting price $p_0$, chosen price $p_t$ and each model's profit-optimal price through the same financial equations. It shows quantity, revenue, variable cost, contribution and profit, together with

$$
\Delta\pi_m(p_t)=\pi_m(p_t)-\pi_m(p_0).
$$

An ordinary percentage profit change is shown only when starting profit is strictly positive: $100\Delta\pi_m/\pi_m(p_0)$. At zero or negative starting profit the pound change remains useful, while that percentage is withheld to avoid division by zero or a misleading interpretation of loss reduction. A starting price outside $[L,U]$ remains a labelled hypothetical reference; it is not a feasible pricing choice. Graph zoom does not change the permitted interval. Period labels require quantity and fixed cost to be supplied consistently; changing the label does not convert them.

### Financial risk from the assumed demand curve

Evaluate each model's suggested price under **both** curves, keeping the same costs and feasible interval. For evaluating model $m$, define lost model-implied profit, or regret, by

$$
\operatorname{regret}_m(p)=\max_{x\in[L,U]}\pi_m(x)-\pi_m(p)\geq0.
$$

Using the benchmark equations gives:

| Suggested price | Evaluating demand curve | Profit per week | Lost model-implied profit per week |
|---|---|---:|---:|
| Linear: £10.50 | Linear | £405.00 | £0.00 |
| Linear: £10.50 | Constant elasticity | £408.16 | £8.50 |
| Constant elasticity: £12.00 | Linear | £360.00 | £45.00 |
| Constant elasticity: £12.00 | Constant elasticity | £416.67 | £0.00 |

For example, $\pi_L(12)=(12-6)(300-20\times12)=360$, so linear regret is $405-360=45$. Conversely,

$$
\pi_C(10.50)=\frac{(10.50-6)10000}{10.50^2}
=\frac{20000}{49}\approx408.1633,
$$

$$
\operatorname{regret}_C(10.50)=\frac{1250}{3}-\frac{20000}{49}
=\frac{1250}{147}\approx8.5034.
$$

The comparison and export recalculate from current inputs. For non-unique optima, the smallest permitted optimal price is the stated representative; other tied choices can have different consequences under the other demand curve. These are conditional financial consequences, not model probabilities, statistical confidence intervals or an expected-profit estimate. Neither row establishes which curve describes customers.

## 7. Revenue versus profit: choosing the financial objective

Revenue measures sales receipts; profit deducts variable and fixed cost. Their preferred prices can therefore differ substantially.

For any differentiable, positive demand function,

$$
R'(p)=Q(p)+pQ'(p)=Q(p)[1-E(p)],
$$

where $E(p)=-pQ'(p)/Q(p)$ is the positive elasticity magnitude. Revenue rises when demand is inelastic, falls when demand is elastic and is stationary when elasticity equals one. Profit has a different derivative:

$$
\pi'(p)=Q(p)+(p-c)Q'(p).
$$

The marginal revenue from a price change must therefore be considered alongside the change in variable cost. Fixed cost affects the resulting profit level but neither derivative.

### Linear revenue optimum

Before the cutoff $z=a/b$,

$$
R_L(p)=ap-bp^2,\qquad R_L'(p)=a-2bp,
\qquad R_L''(p)=-2b<0.
$$

The stationary revenue price is $z/2$. If some permitted price has positive demand, restrict this candidate to the permitted positive-demand region and compare the boundaries. If $L\geq z$, revenue is zero throughout the interval and every permitted price is a revenue maximiser. The zero-revenue plateau cannot beat a feasible positive-revenue price.

At the benchmark, $z/2=15/2=7.50$, which is permitted. The model gives

$$
Q_L(7.50)=300-20(7.50)=150,
$$

$$
R_L(7.50)=7.50(150)=1125,\qquad
\pi_L(7.50)=(7.50-6)(150)=225.
$$

The profit optimum instead earns £405 at £10.50, with revenue £945. A hypothetical business accepting £180 less revenue earns £180 more profit because its variable cost falls by £360. This is a comparison within the stated model, holding fixed cost at zero.

### Constant-elasticity revenue optimum

$$
R_C(p)=Kp^{1-e},\qquad R_C'(p)=K(1-e)p^{-e}.
$$

The revenue-maximising price is $U$ if $0<e<1$, every price in $[L,U]$ if $e=1$, and $L$ if $e>1$. The equal-revenue case is reported as a set rather than a falsely unique price. Neither $c$ nor $F$ changes revenue, although both matter when assessing profit at the revenue optimum.

At the benchmark $e=2$, revenue decreases with price, so its bounded maximum is at £1:

$$
Q_C(1)=100(1/10)^{-2}=10000,\quad R_C(1)=10000,
$$

$$
VC_C(1)=6(10000)=60000,\quad \pi_C(1)=-50000.
$$

The profit optimum at £12 earns about £416.67 despite revenue of about £833.33. Maximising sales receipts alone would select a loss-making price because the model assumes all 10,000 units can be supplied at £6 each. This extreme comparison highlights the commercial importance of contribution, capacity and the credibility of the extrapolated demand curve.

The implementation's revenue optimiser is separate from the profit optimiser. Revenue-optimal sets and financial quantities at a stated representative are exported alongside profit results; numerical tests separately check the revenue objective over the permitted interval.

## 8. Reproducible investigations and calculated summaries

The first four investigations use $p_0=10$ and $Q_0=100$ units per week with the £1–£15 interval unless the price-cap scenario changes its upper bound. Each changes one named assumption from its stated baseline. The fifth holds fixed cost at £50 and the interval at £1–£20 while changing unit cost. The report generator recalibrates $a$ and $b$ whenever $e$ changes, preserving the matched starting conditions in every scenario.

### Elasticity: $e=0.5,1,1.5,2,3$

Hold $c=6$ and $F=0$ constant.

| $e$ | Linear optimal price | Linear profit | Constant-elasticity optimal price | Constant-elasticity profit | Boundary information |
|---|---|---|---|---|---|
| 0.5 | £15.00 | £675.00 | £15.00 | £734.85 | Both are at the upper bound. |
| 1 | £13.00 | £490.00 | £15.00 | £600.00 | Constant elasticity is at the upper bound. |
| 1.5 | £11.33 | £426.67 | £15.00 | £489.90 | Constant elasticity is at the upper bound; unrestricted candidate is £18. |
| 2 | £10.50 | £405.00 | £12.00 | £416.67 | Both are interior. |
| 3 | £9.67 | £403.33 | £9.00 | £411.52 | Both are interior. |

Calculated summary: optimal prices and profits decrease across these sampled scenarios, but the models predict different values. The constant-elasticity results at low $e$ are governed by the £15 bound. Changing $e$ recalibrates each entire curve about the common starting point; these sample trends do not establish a general monotonic rule or how a real firm’s profit responds to an estimated elasticity change. A different permitted interval may change boundary-driven conclusions.

This is sensitivity to **own-price elasticity**, not an independently identified substitution effect. No competitor-price response or compensated-demand model is specified, so the investigation cannot separate substitution from income effects or estimate switching to particular alternatives.

### Unit cost: £6 versus £7

Hold $e=2$ and $F=0$ constant.

| Unit cost | Linear optimal price/profit | Constant-elasticity optimal price/profit |
|---|---|---|
| £6 | £10.50 / £405.00 | £12.00 / £416.67 |
| £7 | £11.00 / £320.00 | £14.00 / £357.14 |

For linear demand, $a=300$, $b=20$ and $z=15$ remain unchanged. At $c=7$,

$$
v_L=(15+7)/2=11,\quad Q_L(11)=80,
\quad R_L=880,\quad VC_L=560,\quad \pi_L=320.
$$

For constant elasticity,

$$
v_C=2(7)/(2-1)=14,\quad Q_C(14)=10000/196=2500/49,
$$

$$
R_C=35000/49\approx714.2857,\quad
VC_C=17500/49\approx357.1429,\quad
\pi_C=17500/49\approx357.1429.
$$

Both stationary prices lie in £1–£15 and satisfy the maximum conditions derived earlier. Compared with $c=6$, linear quantity falls from 90 to 80 and profit falls by £85; constant-elasticity quantity falls from about 69.4444 to 51.0204 and profit falls by about £59.5238.

The preferred prices rise by £0.50 and £2 respectively because, while interior, $dv_L/dc=1/2$ and $dv_C/dc=e/(e-1)=2$. These are model-dependent pass-through rates, not a universal rule that a £1 cost increase should prompt either price change. A hypothetical business would need to reassess both sales volume and contribution after a supplier cost increase. The result changes once a boundary binds; constant unit cost and an unchanged demand curve are also assumptions.

### Fixed cost: £0 versus £50 per week

Hold $e=2$ and $c=6$ constant.

| Fixed cost | Linear optimal price/profit | Constant-elasticity optimal price/profit |
|---|---|---|
| £0 | £10.50 / £405.00 | £12.00 / £416.67 |
| £50 | £10.50 / £355.00 | £12.00 / £366.67 |

Calculated summary: both profit curves move down by £50 and both optimal-price sets remain unchanged. The argument in section 5 establishes this generally for an unchanged interval, including ties. It does not cover a shutdown comparison with avoidable fixed costs.

### Price-cap investigation

Keeping the benchmark’s lower price £1, change the upper price from £15 to £11 for both models. The linear optimum stays £10.50. Constant elasticity becomes a boundary solution at £11, with

$$
\pi_C(11)=(11-6)\frac{10000}{121}
=\frac{50000}{121}\approx413.2231.
$$

At £11, constant-elasticity demand is $10000/121\approx82.6446$, revenue is $110000/121\approx909.0909$ and variable cost is $60000/121\approx495.8678$. Maximum profit falls from $1250/3$ to $50000/121$, a reduction of about £3.4435 per week, while the linear maximum remains £405. This is the opportunity cost of this particular restriction under the models. The upper boundary prevents constant elasticity from reaching its unrestricted stationary price of £12. It also produces higher modelled sales and revenue than at £12, showing why a revenue increase need not improve profit. A different cap or estimated elasticity would change the amount.

This changes an explicit permitted interval. Zooming a graph leaves that economic interval and its optimum unchanged.

### High-cost and zero-demand-plateau investigation

Use $p_0=10$, $Q_0=100$, $e=2$, $F=50$ and $[L,U]=[1,20]$ throughout. Compare $c=6$ with $c=20$.

| Model | Unit cost | Complete profit-optimal set | Quantity at the stated representative | Maximum profit |
|---|---:|---|---:|---:|
| Linear | £6 | $\{10.50\}$ | 90 | £355.00 |
| Linear | £20 | $[15,20]$ | 0 at every tied price | −£50.00 |
| Constant elasticity | £6 | $\{12\}$ | 69.4444 | £366.67 |
| Constant elasticity | £20 | $\{20\}$ | 25 | −£50.00 |

For linear demand the cutoff remains £15. At every positive-demand price $p<15$, the margin $p-20$ is negative, so profit is strictly less than −£50. At every permitted $p\geq15$, demand is zero and profit equals −£50. Thus every price in the interval $[15,20]$ is optimal. Substituting $c=20$ into the quadratic vertex gives £17.50, but this lies beyond the positive-demand region and cannot establish a unique optimum.

For constant elasticity the unrestricted stationary candidate is $2(20)/(2-1)=40$, above the £20 upper limit. The derivative is positive throughout the permitted interval, so the bounded optimum is £20:

$$
Q_C(20)=100(20/10)^{-2}=25,\quad
R_C(20)=500,\quad VC_C(20)=500,
$$

$$
TC_C(20)=550,\qquad \pi_C(20)=(20-20)(25)-50=-50.
$$

The maximum profit falls by £405 for linear demand and about £416.67 for constant elasticity relative to this investigation's own $c=6$ baseline. Neither curve offers positive contribution under the high-cost assumptions. Linear demand achieves its least loss with no sales across a plateau, whereas constant elasticity sells 25 units at zero unit margin. This distinction matters when evaluating sales targets and cost exposure even when headline profit is identical. An operating decision requires avoidable-cost, capacity and alternative-use information absent from this model; a mathematical least-loss price alone does not settle whether the hypothetical business should continue trading.

### Reading the investigations together

The cost comparison makes demand shape financially consequential: the same supplier cost increase generates different prices and quantities. The price cap shows the cost of a binding constraint. Fixed cost changes the profit level while preserving all operating-price ties. Elasticity and the permitted interval can alter both whether an optimum is interior and the apparent price response. The high-cost case demonstrates why the complete optimal set and contribution provide information that a single price and profit figure can miss.

The website's complete findings report expands each investigation into its economic question, assumptions, theoretical prediction, equations, worked results, before-and-after comparisons, interpretation, financial implications, supported conclusion and follow-up. These sections are generated from calculated scenario rows in `analysis.py`.

## 9. Numerical and automated verification

The analytical method uses calculus and a complete comparison of permitted endpoints, cutoff and plateau. Independently, the implementation uses [SciPy’s bounded scalar minimiser](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize_scalar.html) on suitable transformed contribution objectives. Maximising contribution is equivalent to maximising profit because fixed cost is constant. The numerical method does not seed its search with the analytical optimal-price formula.

For linear demand, the numerical method splits the interval at the cutoff, searches the positive-demand quadratic in rescaled price coordinates, compares endpoints/cutoff explicitly, and includes the constant zero-demand segment. An interval wholly beyond the cutoff is flat and needs no artificial stationary-point search.

For constant elasticity with positive cost and prices above cost, write $t=\log(p/c)$. Apart from a positive constant, contribution is

$$
(\exp(t)-1)\exp(-et).
$$

Maximising its logarithm preserves the best price and improves numerical scaling. If the interval ends at or below cost, contribution is non-positive; the numerical method instead minimises a logarithmic loss objective and explicitly checks endpoints. If $c=0$, a log-price power objective handles increasing/decreasing cases, and the identity $e=1,c=0$ identifies the entire flat interval. Exact flat identities and optimal intervals are treated explicitly rather than interpreting optimiser noise as meaningful price differences.

Numerical answers have tolerances. For a unique optimum, analytical and numerical prices and profit should agree within the stated test tolerance. With multiple optima, a numerical representative should belong to the analytical set and attain the same best profit; different equally optimal representatives are not a contradiction. A sampled grid or plotted peak is useful for illustration but not proof of an exact maximum.

Run `python -m pytest -q` to check the model, analysis engine and interface in your environment. Model tests cover starting quantity, slope and elasticity, the benchmark, numerical agreement, both boundaries, cutoff and plateau, ties, zero cost, all elasticity cases, fixed-cost invariance and invalid inputs. Marginal-revenue tests use independent changes in revenue and quantity, check the exceptions, and retain regressions for very large fixed cost and finite log-domain demand calculations. Analysis tests use direct financial equations and separate numerical searches to check the 26 investigation rows, revenue optima, complete optimal sets, chosen-price comparisons and cross-model regret. Interface checks exercise the financial comparisons and generated exports. Passing checks assesses the specified implementation, not empirical validity.

## 10. Limitations and further investigation

Both curves use illustrative assumptions rather than fitted customer observations. Agreement in quantity, slope and elasticity at one point does not establish accuracy over the full price interval. The linear curve has a finite cutoff; constant elasticity has no cutoff and may predict unrealistic quantities near low prices. Changing the permitted interval can change a boundary-driven finding substantially.

The models assume continuous quantities, constant unit cost, no capacity limit and no competitor or time response. They also treat fixed cost as unavoidable. Extending the financial decision would require estimated demand at several prices, uncertainty ranges, avoidable-cost information and operational constraints. Sensitivity analysis identifies which assumptions matter within the model; it does not show how real customers will behave.

The definitions have an external source; model-specific formulas and examples are derived here from the stated assumptions. The complete investigation and its downloadable results provide an auditable mathematical basis for discussing pricing decisions, with empirical validation left as a clearly identified extension.
