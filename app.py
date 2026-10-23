"""Financial dashboard; models.py calculates, analysis.py explains and exports."""

from dataclasses import asdict
import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from models import (
    MODEL_LABELS, Parameters, analytical_optimum, evaluate,
    mr_mc_check, numerical_optimum, unconstrained_summary, zero_demand_price,
)
from analysis import (
    INVESTIGATION_LABELS, METHODOLOGY, build_investigation, chosen_price_rows,
    model_risk_rows, report_markdown, revenue_optimum, summary_markdown,
)

MODELS = ("linear", "constant_elasticity")
COLORS = {"linear": "#176B87", "constant_elasticity": "#D96C35"}
LOCATIONS = {
    "interior": "Interior maximum", "lower_boundary": "Lower permitted boundary",
    "upper_boundary": "Upper permitted boundary", "multiple": "Multiple equally optimal prices",
}


def reset_inputs():
    for key, value in asdict(Parameters()).items():
        st.session_state[key] = value
    st.session_state["period"] = "week"
    st.session_state["test_price"] = 10.0


def price_set(intervals):
    return "; ".join(f"£{lo:,.2f}" if lo == hi else f"£{lo:,.2f}–£{hi:,.2f}"
                     for lo, hi in intervals)


def show_table(frame, signed=()):
    formats = {}
    for col in frame.columns:
        if pd.api.types.is_numeric_dtype(frame[col]):
            formats[col] = "{:+,.2f}" if col in signed or col.startswith("Δ") else "{:,.2f}"
            if col.startswith("Quantity"):
                formats[col] = "{:,.4f}"
    st.dataframe(frame.style.format(formats), hide_index=True, width="stretch")


def result_table(rows, period):
    names = {
        "model_label": "Demand model", "price": "Displayed price (£)",
        "quantity": f"Quantity / {period}", "revenue": f"Revenue (£ / {period})",
        "total_cost": f"Total cost (£ / {period})", "profit": f"Profit (£ / {period})",
        "optimal_set": "All optimal prices", "location": "Maximum type",
        "feasible": "Permitted price?",
    }
    frame = pd.DataFrame(rows)
    show_table(frame[[key for key in names if key in frame]].rename(columns=names))


def make_chart(kind, params, optima, left, right, period="week", test_price=None):
    """Sampling is for drawing only. Both curves use the same economic interval."""
    fig = go.Figure()
    lower, upper = max(left, params.price_min), min(right, params.price_max)
    if lower <= upper:
        for model in MODELS:
            prices = sorted(set(np.linspace(lower, upper, 400)) | {
                p for p in (params.p0, optima[model].price, zero_demand_price(params),
                            test_price if test_price is not None else params.p0)
                if lower <= p <= upper
            })
            values = [evaluate(model, p, params)[kind] for p in prices]
            fig.add_trace(go.Scatter(
                x=prices, y=values, name=MODEL_LABELS[model], mode="lines",
                line=dict(color=COLORS[model], width=3),
                hovertemplate="Price £%{x:.4f}<br>Value %{y:.4f}<extra>%{fullData.name}</extra>",
            ))
            optimum = optima[model]
            for lo, hi in optimum.optimal_intervals:
                a, b = max(lo, lower), min(hi, upper)
                if a < b:
                    # A thicker segment identifies every optimal price, not one arbitrary choice.
                    xs = np.linspace(a, b, 100)
                    fig.add_trace(go.Scatter(
                        x=xs, y=[evaluate(model, float(p), params)[kind] for p in xs],
                        mode="lines", line=dict(color=COLORS[model], width=7, dash="dot"),
                        name=f"{MODEL_LABELS[model]} profit-optimal set", showlegend=False,
                    ))
            if lower <= optimum.price <= upper:
                label = "Linear" if model == "linear" else "CE"
                suffix = "profit-optimal representative" if optimum.boundary == "multiple" else "profit optimum"
                # Put endpoint labels towards the inside of the graph.
                side = "left" if optimum.price > (lower + upper) / 2 else "right"
                fig.add_trace(go.Scatter(
                    x=[optimum.price], y=[getattr(optimum, kind)], mode="markers+text",
                    text=[f"{label}<br>£{optimum.price:.2f}"],
                    textposition=f"{'top' if model == 'linear' else 'bottom'} {side}",
                    marker=dict(size=11, color=COLORS[model], symbol="diamond"),
                    showlegend=False, cliponaxis=False,
                    hovertemplate=f"{label} {suffix}<br>Price £%{{x:.4f}}<br>Value %{{y:.4f}}<extra></extra>",
                ))
            if test_price is not None and lower <= test_price <= upper:
                fig.add_trace(go.Scatter(
                    x=[test_price], y=[evaluate(model, test_price, params)[kind]],
                    mode="markers", marker=dict(size=12, color=COLORS[model], symbol="square",
                                                line=dict(color="white", width=1.5)),
                    name=f"{MODEL_LABELS[model]} at chosen price", showlegend=False,
                    hovertemplate="Chosen price £%{x:.4f}<br>Value %{y:.4f}<extra>%{fullData.name}</extra>",
                ))
    if test_price is not None and left <= test_price <= right:
        fig.add_vline(x=test_price, line_dash="dashdot", line_color="#7053A1",
                      annotation_text=f"Chosen £{test_price:,.2f}", annotation_position="bottom right")
    if left <= params.p0 <= right:
        reference = evaluate("linear", params.p0, params)
        feasible = params.price_min <= params.p0 <= params.price_max
        fig.add_trace(go.Scatter(
            x=[params.p0], y=[reference[kind]], mode="markers+text",
            text=["p₀" if feasible else "p₀ (outside interval)"],
            textposition="bottom left", marker=dict(color="#596579", size=11, symbol="x"),
            showlegend=False,
            hovertemplate="Starting price £%{x:.4f}<br>Value %{y:.4f}<extra></extra>",
        ))
    cutoff = zero_demand_price(params)
    if left <= cutoff <= right:
        fig.add_vline(x=cutoff, line_dash="dot", line_color=COLORS["linear"],
                      annotation_text="Linear cutoff", annotation_position="top left")
    for bound, label in ((params.price_min, "Lower permitted price"),
                         (params.price_max, "Upper permitted price")):
        if left <= bound <= right:
            fig.add_vline(x=bound, line_dash="dash", line_color="#929CAA")
    if kind == "profit":
        fig.add_hline(y=-params.F, line_dash="dot", line_color="#7B4967",
                      annotation_text="No sales: −F", annotation_position="bottom left")
    axis = {"quantity": f"Quantity (continuous units / {period})",
            "profit": f"Profit (£ / {period})", "revenue": f"Revenue (£ / {period})"}
    fig.update_layout(
        template="plotly_white", height=430, margin=dict(l=15, r=30, t=60, b=30),
        xaxis_title="Selling price p (£ per unit)", yaxis_title=axis[kind],
        xaxis=dict(range=[left, right]), legend=dict(orientation="h", y=1.17, x=0),
        font=dict(family="sans-serif", size=12),
    )
    # Leave room for marker labels, especially when the legend wraps on a phone.
    plotted = [float(value) for trace in fig.data for value in trace.y]
    if plotted:
        if kind == "profit":
            plotted.append(-params.F)
        low, high = min(plotted), max(plotted)
        padding = 0.15 * max(high - low, abs(high) * 0.1, 1.0)
        fig.update_yaxes(range=[low - padding if kind == "profit" else 0,
                                high + padding])
    return fig


def numerical_checks(params, optima):
    rows, prices = [], {}
    for model in MODELS:
        try:
            result = numerical_optimum(model, params)
            prices[model] = result.price
            # Tied optima need not have the same representative price.
            membership = any(lo - 2e-6 * max(1, abs(lo)) <= result.price <=
                             hi + 2e-6 * max(1, abs(hi))
                             for lo, hi in optima[model].optimal_intervals)
            agrees = membership and np.isclose(result.contribution, optima[model].contribution,
                                               rtol=2e-6, atol=1e-7)
            rows.append({"Model": MODEL_LABELS[model], "Numerical price (£)": result.price,
                         "Numerical profit (£)": result.profit,
                         "Check": "Agrees with optimal set and value" if agrees else "Needs investigation"})
            if not agrees:
                st.warning(f"Numerical check needs investigation for {MODEL_LABELS[model]}.")
        except (ValueError, RuntimeError, OverflowError) as exc:
            st.warning(f"Numerical check unavailable for {MODEL_LABELS[model]}: {exc}")
    return rows, prices


def maths_section(params, check_rows):
    st.subheader("From demand assumptions to a pricing decision")
    st.write("Both curves match quantity, slope and elasticity at the starting price. Their curvature "
             "away from that point changes the trade-off between sales volume and contribution per unit.")
    st.latex(r"a=Q_0(1+e),\quad b=\frac{eQ_0}{p_0},\quad Q_L(p)=\max(0,a-bp),\quad Q_C(p)=Q_0(p/p_0)^{-e}")
    st.latex(r"R=pQ,\quad TC=cQ+F,\quad \pi=(p-c)Q-F,\quad E(p)=-\frac{pQ'(p)}{Q(p)}")
    st.latex(r"Q_L(p_0)=Q_C(p_0)=Q_0,\quad Q'_L(p_0)=Q'_C(p_0)=-eQ_0/p_0,\quad E_L(p_0)=E_C(p_0)=e")
    st.write(f"At the current starting price £{params.p0:,.2f}, a small 1% price rise implies "
             f"approximately a {params.e:g}% quantity fall locally. The linear model's elasticity "
             "changes with price; constant elasticity keeps this responsiveness throughout.")
    with st.expander("Differentiation and maximum checks", expanded=True):
        st.latex(r"\pi'=Q+(p-c)Q',\qquad \pi'_L=a+bc-2bp,\quad \pi''_L=-2b<0")
        st.latex(r"p^*_L=\frac{a+bc}{2b},\qquad p_z=\frac{a}{b}")
        st.write("The positive-demand linear profit curve is strictly concave. Compare the feasible "
                 "stationary point, both endpoints and the cutoff. Beyond the cutoff, profit is −F; "
                 "the entire plateau can tie. Reporting one representative does not imply uniqueness.")
        st.latex(r"\pi'_C=Q_0p_0^e p^{-e-1}[(1-e)p+ec],\qquad p^*_C=\frac{ec}{e-1}\ \ (e>1,\ c>0)")
        st.write("For e > 1 and c > 0, the derivative changes from positive to negative at the candidate. "
                 "A permitted boundary replaces it if it lies outside the interval. The remaining cases "
                 "follow directly from the derivative's sign:")
        st.dataframe(pd.DataFrame([
            ["0 < e < 1; c ≥ 0", "Strictly increasing", "Upper boundary", "Unbounded as p → ∞"],
            ["e = 1; c > 0", "Strictly increasing", "Upper boundary", "Unattained finite supremum"],
            ["e = 1; c = 0", "Constant profit", "Every permitted price", "Every positive price"],
            ["e > 1; c = 0", "Strictly decreasing", "Lower boundary", "Unbounded as p → 0⁺"],
        ], columns=["Assumptions", "Profit behaviour", "Bounded optimum", "Without bounds"]),
            hide_index=True, width="stretch")
    st.subheader("Numerical verification for the current inputs")
    st.caption("A separate SciPy search checks profit without using the analytical optimal-price formula "
               "or the graph grid. Endpoints and the linear cutoff are checked explicitly. Tied solutions "
               "are compared by value and membership of the whole optimal set.")
    if check_rows:
        st.dataframe(pd.DataFrame(check_rows).style.format({"Numerical price (£)": "{:.8f}",
                                                          "Numerical profit (£)": "{:.8f}"}),
                     hide_index=True, width="stretch")
    st.info("A continuous profit function on the shared closed interval has a maximum. This guarantee "
            "does not imply a finite unrestricted optimum. Fixed cost subtracts the same amount at every "
            "price, preserving the whole set of optimal operating prices.")
    st.subheader("Marginal revenue and marginal cost")
    st.latex(r"MR=\frac{d(pQ)/dp}{dQ/dp}=p+\frac{Q}{Q'},\qquad MC=c")
    st.write("At a differentiable interior optimum with positive demand and nonzero demand slope, "
             "the stationary condition gives MR = MC. This is a check on the marginal trade-off, "
             "alongside the maximum and endpoint checks above.")
    for model in MODELS:
        check = mr_mc_check(model, params)
        if check['applicable'] and check['marginal_revenue'] is not None:
            st.write(f"{MODEL_LABELS[model]}: MR = £{check['marginal_revenue']:,.6f}/unit; "
                     f"MC = £{check['marginal_cost']:,.6f}/unit. {check['explanation']}")
        else:
            st.write(f"{MODEL_LABELS[model]}: {check['explanation']}")
    with st.expander("Unrestricted problem under the current assumptions"):
        for model in MODELS:
            try:
                summary = unconstrained_summary(model, params)
                extra = (f" Price: £{summary['price']:,.4f}."
                         if summary['status'] == 'unique' and summary['price'] is not None else "")
                st.markdown(f"**{MODEL_LABELS[model]}:** {summary['explanation']}{extra}")
            except (ValueError, OverflowError) as exc:
                st.warning(f"Unrestricted result exceeds the numerical range: {exc}")
    with st.expander("Full derivations and boundary cases"):
        st.markdown(Path(__file__).with_name("maths_explanation.md").read_text(encoding="utf-8"))


def financial_comparison(params, optima, period):
    st.subheader("Revenue and profit answer different questions")
    st.write("Revenue measures sales income. Profit deducts variable and fixed costs. Selling more "
             "units can increase revenue while reducing profit when contribution per unit is too small.")
    rows = []
    for model in MODELS:
        try:
            rev = revenue_optimum(model, params)
        except (ValueError, OverflowError) as exc:
            st.warning(f"Revenue-objective comparison unavailable for {MODEL_LABELS[model]} at these scales: {exc}")
            continue
        profit = optima[model]
        for objective, result in (("Maximum revenue", rev), ("Maximum profit", asdict(profit))):
            rows.append({**asdict(params), **result, "model": model, "period": period,
                         "objective": objective, "model_label": MODEL_LABELS[model]})
        gain = profit.contribution - rev['contribution']
        gain = 0.0 if abs(gain) < .005 else gain
        sacrifice = rev['revenue'] - profit.revenue
        sacrifice = 0.0 if abs(sacrifice) < .005 else sacrifice
        st.markdown(f"**{MODEL_LABELS[model]}:** revenue is maximised at **{price_set(rev['optimal_intervals'])}** "
                    f"(representative revenue £{rev['revenue']:,.2f}, profit £{rev['profit']:,.2f}/{period}). "
                    f"Choosing the profit-optimal price yields **£{gain:,.2f} more profit/{period}**, "
                    f"with £{sacrifice:,.2f} less revenue/{period} at these representatives.")
        if len(rev['optimal_intervals']) > 1 or any(lo != hi for lo, hi in rev['optimal_intervals']):
            st.caption("Revenue has tied maximisers. The comparison uses the smallest price in that "
                       "set; their profits can differ when unit cost is positive.")
    if not rows:
        return
    frame = pd.DataFrame(rows)
    names = {"model_label": "Demand model", "objective": "Objective", "price": "Price (£)",
             "quantity": f"Quantity / {period}", "revenue": f"Revenue (£ / {period})",
             "contribution": f"Contribution (£ / {period})", "profit": f"Profit (£ / {period})"}
    show_table(frame[list(names)].rename(columns=names))
    if frame['profit'].min() < 0:
        st.caption("A revenue-maximising solution can operate at a loss. Very large sales at low prices "
                   "also expose the absence of capacity limits in these illustrative demand assumptions.")
    benchmark = Parameters()
    low_price_result = evaluate('constant_elasticity', benchmark.price_min, benchmark)
    st.caption(f"For comparison, the constant-elasticity benchmark predicts {low_price_result['quantity']:,.0f} "
               f"units/week at £{benchmark.price_min:g}. This follows from the assumed curve and absent "
               "capacity constraint; it is not a realistic sales forecast.")
    export = frame.copy()
    export['optimal_intervals'] = export['optimal_intervals'].map(json.dumps)
    st.download_button("Download financial comparison CSV", export.to_csv(index=False).encode("utf-8"),
                       file_name="financial_objectives.csv", mime="text/csv")


def investigation_section():
    st.subheader("Complete investigations")
    st.download_button("Download concise findings summary", summary_markdown().encode('utf-8'),
                       file_name='FINDINGS_SUMMARY.md', mime='text/markdown')
    st.write("Each experiment changes one assumption and recalculates both demand models. These "
             "controlled weekly scenarios are separate from the live sidebar, so comparisons stay reproducible.")
    selection = st.selectbox("Choose an investigation", list(INVESTIGATION_LABELS.values()), key="investigation")
    key = next(key for key, label in INVESTIGATION_LABELS.items() if label == selection)
    item = build_investigation(key)
    st.markdown(f"### {item['title']}")
    st.markdown(f"**Economic question:** {item['question']}")
    with st.container(border=True):
        st.markdown("**Starting assumptions and controlled variables**")
        st.write(item['changed'])
        st.write(item['held'])
        st.caption("All quantities and period totals in these investigations are weekly.")
    st.markdown("#### Theoretical Prediction and Mathematical Reasoning")
    st.write(item['theory'])
    for equation in item['equations']:
        st.latex(equation)
    st.markdown("#### Calculated Results: Before and After")
    frame = pd.DataFrame(item['rows'])
    columns = {"scenario": "Scenario", "model_label": "Demand model", "price": "Displayed price (£)",
               "quantity": "Quantity / week", "revenue": "Revenue (£ / week)", "profit": "Profit (£ / week)",
               "price_change": "Δ price (£)", "profit_change": "Δ profit (£ / week)"}
    shown = frame[list(columns)].rename(columns=columns)
    shown["All optimal prices"] = frame['optimal_intervals'].map(price_set)
    shown["Maximum type"] = frame['boundary'].map(LOCATIONS)
    show_table(shown)
    st.caption("Changes are measured against the starting scenario of the same model. Full precision "
               "is retained in calculations and CSV exports; displayed money is rounded to two decimals.")
    st.markdown("#### Worked Calculations and Maximum Checks")
    for working in item['workings']:
        with st.expander(f"{MODEL_LABELS[working['model']]} · {working['scenario']}"):
            for index, step in enumerate(working['steps'], 1):
                st.markdown(f"{index}. {step}")
    st.markdown("#### Interpretation of Findings")
    st.write(item['interpretation'])
    st.markdown("#### Financial Implications")
    st.write(item['financial_implications'])
    st.success(item['conclusion'])
    st.markdown("#### Limitations and Further Investigation")
    st.write(item['limitation'])
    csv = frame.copy()
    csv['optimal_intervals'] = csv['optimal_intervals'].map(json.dumps)
    cols = st.columns(2)
    with cols[0]:
        st.download_button("Download investigation CSV", csv.to_csv(index=False).encode("utf-8"),
                           file_name=f"investigation_{key}.csv", mime="text/csv", width="stretch")
    with cols[1]:
        st.download_button("Download investigation report", report_markdown([key]).encode("utf-8"),
                           file_name=f"investigation_{key}.md", mime="text/markdown", width="stretch")
    st.divider()
    with st.expander("Complete Mathematical Investigation and Findings"):
        st.markdown(report_markdown())
    st.download_button("Download complete findings report", report_markdown().encode("utf-8"),
                       file_name="mathematical_investigation_and_findings.md", mime="text/markdown")


def methodology_section():
    st.subheader("Methodology and scope")
    st.write("The investigation calibrates linear and constant-elasticity demand to the same starting "
             "quantity and local responsiveness, then maximises operating profit on a shared positive "
             "price interval. Sensitivity experiments isolate elasticity, unit cost, a price cap, fixed "
             "cost and a high-cost case. Algebraic results are checked using numerical optimisation.")
    st.markdown("#### What the results establish")
    st.write("The calculations identify the best price within each specified model and feasible "
             "interval. Agreement at one price does not identify a demand curve: different curvature "
             "produces different quantities, margins and optimum prices elsewhere. The model gap "
             "therefore measures sensitivity to assumptions, rather than forecast accuracy.")
    st.markdown("#### Limits to a business decision")
    st.write("Demand is illustrative and has not been fitted to customer observations. Quantity is "
             "continuous; marginal cost is constant; capacity, competition, inventory, customer "
             "segments and time effects are omitted. Before applying a price, estimate demand from "
             "observations at several prices and test cost, capacity and competitor scenarios.")
    st.write("Changing own-price elasticity tests an assumed responsiveness. It does not independently "
             "identify a substitution effect: no competitor-price or compensated-demand model is used.")
    st.write("Fixed cost is unavoidable in the operating model. Zero sales therefore gives profit −F. "
             "A shutdown decision needs a separate payoff and evidence about avoidable costs.")
    st.markdown("#### Reproducibility")
    st.write("Live results include their input assumptions, permitted bounds, period label and full "
             "optimal sets in the CSV. The completed report includes equations, substituted working, "
             "scenario comparisons and conclusions. The downloaded project includes automated "
             "model, analysis and interface tests; the numerical-check tab reports the current run.")
    st.caption(METHODOLOGY)
    st.markdown("**References:** [OpenStax: price elasticity of demand](https://openstax.org/books/principles-economics-3e/pages/5-1-price-elasticity-of-demand-and-price-elasticity-of-supply) "
                "for percentage responsiveness; [SciPy scalar optimisation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize_scalar.html) "
                "for the numerical search method. Demand calibration, derivations and financial "
                "comparisons are implemented in this project.")


def comparison_csv(rows):
    """Retain numerical precision and machine-readable optimal sets in downloads."""
    frame = pd.DataFrame(rows)
    for column in frame.columns:
        if 'intervals' in column:
            frame[column] = frame[column].map(json.dumps)
    return frame.to_csv(index=False).encode('utf-8')


def chosen_price_section(params, period):
    st.subheader("What if I charged this price?")
    previous = st.session_state.get('test_price', params.p0)
    bounded = max(params.price_min, min(params.price_max, previous))
    if bounded != previous:
        st.info("The chosen price has been moved into the updated permitted interval.")
    st.session_state['test_price'] = bounded
    test_price = st.number_input("Chosen test price (£)", min_value=params.price_min,
                                 max_value=params.price_max, step=.25, format="%.4f", key='test_price')
    rows = []
    fields = [('price', 'Selling price (£)'), ('quantity', f'Quantity / {period}'),
              ('revenue', f'Revenue (£ / {period})'), ('variable_cost', f'Variable cost (£ / {period})'),
              ('contribution', f'Contribution (£ / {period})'), ('profit', f'Profit (£ / {period})'),
              ('profit_change', f'Δ profit vs start (£ / {period})')]
    for model in MODELS:
        with st.container():
            st.markdown(f"**{MODEL_LABELS[model]} demand**")
            try:
                current = chosen_price_rows(params, test_price, period, models=(model,))
                rows.extend(current)
                display = {'Financial measure': [label for _, label in fields] + ['Δ profit vs start (%)']}
                for row in current:
                    display[row['scenario']] = [f"{row[field]:+,.2f}" if field == 'profit_change'
                                               else f"{row[field]:,.4f}" if field == 'quantity'
                                               else f"{row[field]:,.2f}" for field, _ in fields] + [
                        '—' if row['profit_change_percent'] is None else f"{row['profit_change_percent']:+.2f}%"]
                st.dataframe(pd.DataFrame(display), hide_index=True, width='stretch')
            except (ValueError, OverflowError) as exc:
                st.warning(f"Chosen-price comparison unavailable for {MODEL_LABELS[model]}: {exc}")
    st.caption("Changes compare with the starting price even if it is outside the permitted interval. "
               "A percentage is shown only for a positive starting profit; zero or loss baselines use £ changes. "
               "Profit-optimum columns use the smallest representative when prices tie.")
    if rows:
        st.download_button("Download chosen-price comparison CSV", comparison_csv(rows),
                           file_name='chosen_price_comparison.csv', mime='text/csv')
    return test_price


def model_risk_section(params, period):
    st.subheader("How much does choosing a demand model matter?")
    st.caption("Lost model-implied profit (regret) = that curve's permitted maximum profit − profit at the candidate price.")
    try:
        rows = model_risk_rows(params, period)
    except (ValueError, OverflowError) as exc:
        st.warning(f"Model-risk comparison unavailable at these numerical scales: {exc}")
        return
    names = {'candidate_source_label': 'Price suggested by', 'candidate_price': 'Candidate price (£)',
             'evaluated_model_label': 'Demand assumed', 'profit': f'Profit (£ / {period})',
             'regret': f'Lost profit (£ / {period})'}
    show_table(pd.DataFrame(rows)[list(names)].rename(columns=names))
    st.write("Each candidate is evaluated under both hypothetical demand curves. A larger maximum "
             "under one curve does not establish that it is a better description of real demand. "
             "No probabilities or expected profits are assigned.")
    st.caption("Tied suggestions use the smallest price in the full optimal set; another tied price can "
               "have a different outcome under the other model. Downloads preserve both full sets.")
    st.download_button("Download model-risk comparison CSV", comparison_csv(rows),
                       file_name='model_risk.csv', mime='text/csv')


def dashboard_section(params, optima, reference_rows, numerical_prices, period):
    st.subheader("Profit-maximising pricing")
    st.caption("One shared set of assumptions · Two demand models · Full permitted interval")
    cards, optimum_rows = st.columns(2), []
    for column, model in zip(cards, MODELS):
        result = optima[model]
        reference = evaluate(model, params.p0, params)
        with column.container(border=True):
            st.markdown(f"### {MODEL_LABELS[model]}")
            st.metric("Optimal selling price", price_set(result.optimal_intervals))
            st.metric(f"Operating profit / {period}", f"£{result.profit:,.2f}",
                      delta=f"£{result.contribution-reference['contribution']:+,.2f} vs starting price")
            sub = st.columns(2)
            sub[0].metric(f"Revenue / {period}", f"£{result.revenue:,.2f}")
            sub[1].metric(f"Quantity / {period}", f"{result.quantity:,.2f}")
            st.caption(f"{LOCATIONS[result.boundary]} · Contribution £{result.contribution:,.2f}/{period}")
            volume_change = result.quantity - reference['quantity']
            st.write(f"Under this curve, the representative price predicts {result.quantity:,.2f} units/{period} "
                     f"({volume_change:+,.2f} vs start), with £{result.price-params.c:,.2f} contribution per unit. "
                     f"{LOCATIONS[result.boundary]}. " +
                     ("This assumes a constant demand slope until the zero-sales cutoff."
                      if model == 'linear' else "This assumes the same elasticity at every price."))
            if result.boundary == 'multiple':
                st.caption("Every price in the displayed set ties. Financial metrics use the smallest "
                           "optimal price as the representative.")
            if result.warning:
                st.warning(result.warning)
        optimum_rows.append(dict(asdict(result), model_label=MODEL_LABELS[model],
                                 optimal_set=price_set(result.optimal_intervals), location=LOCATIONS[result.boundary]))
    with st.expander("Full optimal-price financial results"):
        result_table(optimum_rows, period)
    st.caption("Calculated at full precision. Displayed money is rounded to two decimals; "
               "quantities are continuous model estimates.")
    linear, ce = (optima[model] for model in MODELS)
    st.info(f"Model sensitivity: representative prices differ by £{abs(ce.price-linear.price):,.2f} "
            f"and maximum profit by £{abs(ce.contribution-linear.contribution):,.2f}/{period}. Both models match "
            "at the starting point, so this difference arises from their demand shapes away from it.")
    with st.expander("Starting-price financial results"):
        result_table(reference_rows, period)
        if not params.price_min <= params.p0 <= params.price_max:
            st.warning("These reference results use an infeasible price outside the permitted interval.")
    export = []
    for scenario, rows in (("optimal", optimum_rows), ("reference", reference_rows)):
        for row in rows:
            export.append({**asdict(params), **row, "period": period, "scenario": scenario,
                           "feasible": scenario == "optimal" or params.price_min <= params.p0 <= params.price_max,
                           "optimal_intervals": json.dumps(row.get("optimal_intervals", [])),
                           "numerical_optimal_price": numerical_prices.get(row['model']) if scenario == 'optimal' else None})
    st.download_button("Download results CSV", pd.DataFrame(export).to_csv(index=False).encode("utf-8"),
                       file_name="demand_pricing_results.csv", mime="text/csv")
    test_price = chosen_price_section(params, period)
    model_risk_section(params, period)
    st.subheader("Price, demand and financial performance")
    st.caption("Diamonds identify profit-optimal prices in every view; thick dotted segments show "
               "tied profit optima. The cross marks the starting price, squares and a purple line mark "
               "the chosen price. CE means constant elasticity.")
    view = st.radio("Curve view", ["Profit", "Demand", "Revenue"], horizontal=True, key="curve_view")
    kind = {"Demand": "quantity", "Profit": "profit", "Revenue": "revenue"}[view]
    suggested = max(params.price_min, .55 * min(params.p0, *(r.price for r in optima.values())))
    suggested = min(suggested, params.price_min + .8 * (params.price_max-params.price_min))
    with st.expander("Graph display range — changes the view, never the optimum"):
        full_view = st.checkbox("Show the full permitted interval", key="full_view")
        left = st.number_input("Minimum displayed price (£)", value=float(suggested), format="%.4f",
                               key=f"view_min_{params}", disabled=full_view)
        right = st.number_input("Maximum displayed price (£)", value=float(params.price_max), format="%.4f",
                                key=f"view_max_{params}", disabled=full_view)
    if full_view:
        left, right = params.price_min, params.price_max
    if not np.isfinite(left) or not np.isfinite(right) or left <= 0 or right <= left:
        st.error("Graph limits require finite values with 0 < minimum < maximum. Economic results remain unchanged.")
    else:
        outside = [MODEL_LABELS[m] for m in MODELS if not left <= optima[m].price <= right]
        if outside:
            st.info("Representative optimum outside this graph view: " + ", ".join(outside) + ". The table uses the full permitted interval.")
        if not left <= test_price <= right:
            st.info("The chosen price is outside this graph view; its comparison still uses the permitted interval.")
        try:
            st.plotly_chart(make_chart(kind, params, optima, left, right, period, test_price), width="stretch")
        except (ValueError, OverflowError) as exc:
            st.warning(f"This graph range exceeds floating-point limits: {exc}")
    cutoff = zero_demand_price(params)
    st.caption(f"Linear demand reaches zero at £{cutoff:,.4f}. At and above that price, "
               f"profit is −F = £{-params.F if params.F else 0.0:,.2f}/{period} under the unavoidable fixed-cost assumption.")
    financial_comparison(params, optima, period)


def main():
    st.set_page_config(page_title="Demand and Pricing Explorer", page_icon="📈", layout="wide")
    st.markdown("""<style>
    .block-container{padding-top:2.5rem;max-width:1440px;}
    h1{letter-spacing:-.035em;}h2,h3{letter-spacing:-.02em;}
    div[data-testid='stMetricValue']{font-variant-numeric:tabular-nums;}
    div[data-testid='stLatex']{overflow-x:auto;}
    div[data-testid='stMetricLabel']{color:#546477;}
    @media(max-width:640px){.block-container{padding:1.5rem 1rem;}
    div[data-testid='stHorizontalBlock']{flex-wrap:wrap;}
    div[data-testid='stColumn']{min-width:100%;}h1{font-size:2rem;}}
    </style>""", unsafe_allow_html=True)
    st.caption("MATHEMATICAL AND ECONOMIC MODELLING / PRICING & PROFITABILITY")
    st.title("Demand and Pricing Explorer")
    st.markdown("**How does the assumed relationship between price and quantity demanded affect the profit-maximising price?**")
    st.write("Compare two demand models, calculate profit-maximising prices and examine how elasticity, "
             "costs and price restrictions change the financial decision.")
    with st.sidebar:
        st.header("Pricing assumptions")
        st.caption("LIVE MODEL INPUTS")
        st.button("Load benchmark", on_click=reset_inputs, width="stretch")
        st.button("Reset to defaults", on_click=reset_inputs, width="stretch")
        st.selectbox("Demand and cost period", ["week", "month", "day", "chosen period"], key="period")
        period = st.session_state['period']
        st.caption("The period label does not convert values. Enter quantity and fixed cost for the same period.")
        p0 = st.number_input("Starting price p₀ (£)", min_value=0.0, value=10.0, step=.5, key="p0")
        Q0 = st.number_input(f"Starting quantity Q₀ (units / {period})", min_value=0.0, value=100.0, step=10.0, key="Q0")
        e = st.number_input("Starting elasticity magnitude e", min_value=0.0, value=2.0, step=.1, key="e",
                            help="Positive percentage responsiveness at the starting price; linear elasticity changes away from it.")
        c = st.number_input("Unit variable cost c (£)", min_value=0.0, value=6.0, step=.5, key="c")
        F = st.number_input(f"Fixed cost F (£ / {period})", min_value=0.0, value=0.0, step=10.0, key="F")
        st.subheader("Permitted price interval")
        lower = st.number_input("Lower permitted price (£)", min_value=0.0, value=1.0, step=.5, key="price_min")
        upper = st.number_input("Upper permitted price (£)", min_value=0.0, value=15.0, step=.5, key="price_max")
        st.caption("Both models use this same closed interval. Display zoom does not change it.")
    try:
        params = Parameters(p0=p0, Q0=Q0, e=e, c=c, F=F, price_min=lower, price_max=upper)
        optima = {model: analytical_optimum(model, params) for model in MODELS}
        reference_rows = [dict(evaluate(model, p0, params), model=model, model_label=MODEL_LABELS[model],
                               feasible="Yes" if lower <= p0 <= upper else "No: outside interval") for model in MODELS]
    except (ValueError, OverflowError) as exc:
        st.error(f"Please correct the assumptions: {exc}")
        st.write("Use finite p₀ > 0, Q₀ > 0, e > 0, c ≥ 0, F ≥ 0 and 0 < lower < upper. "
                 "Inputs exceeding floating-point range need smaller scales.")
        st.stop()
    st.caption(f"Starting point £{p0:g} · {Q0:g} units/{period} · Elasticity {e:g} · "
               f"Unit cost £{c:g} · Fixed cost £{F:g}/{period} · Permitted price £{lower:g}–£{upper:g}")
    if not lower <= p0 <= upper:
        st.warning("The starting price calibrates both curves but is outside the permitted interval. "
                   "Its reference results are hypothetical, infeasible choices.")
    dashboard, maths, investigations, methodology = st.tabs([
        "Pricing dashboard", "Mathematics and verification", "Investigations and findings", "Methodology and limitations",
    ])
    with maths:
        check_rows, numerical_prices = numerical_checks(params, optima)
        maths_section(params, check_rows)
    with dashboard:
        dashboard_section(params, optima, reference_rows, numerical_prices, period)
    with investigations:
        investigation_section()
    with methodology:
        methodology_section()


if __name__ == '__main__':
    main()
