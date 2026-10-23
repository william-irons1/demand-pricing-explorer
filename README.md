# Demand & Pricing Explorer

**How does the assumed relationship between price and quantity demanded affect the profit-maximising price?**

A mathematics and economics investigation of pricing, revenue, costs and profitability. Two hypothetical demand curves match starting quantity, slope and elasticity, yet imply different optimal prices. Calculus, independent numerical optimisation and controlled sensitivities show the financial consequences of those assumptions. No customer dataset has been fitted.

The interactive Streamlit app compares starting, chosen and optimal prices; explains marginal revenue and cost; evaluates model-dependent pricing risk; and retains five completed investigations with graphs, worked calculations and downloads.

**Start here:** [Concise findings](FINDINGS_SUMMARY.md) · [Full investigation](investigation_worksheet.md) · [Mathematics](maths_explanation.md) · [Publish on GitHub and Streamlit](PUBLISHING.md)

**Publication status:** this package is ready for upload. It does not yet have an assigned GitHub repository or public app URL. Add the real links here after publishing and checking them; localhost is only a local preview.

## Reproducible benchmark and findings

Inputs: `p0=10`, `Q0=100 units/week`, `e=2`, `c=6`, `F=0`, `[L,U]=[1,15]`, with GBP per unit for prices/costs and GBP per week for financial totals.

| Result | Linear demand | Constant elasticity |
|---|---:|---:|
| Demand | max(0, 300 − 20p) | 10000/p² |
| Profit at £10 | £400.00/week | £400.00/week |
| Profit-optimal price | £10.50 | £12.00 |
| Quantity at optimum | 90.0000/week | 69.4444/week |
| Revenue at optimum | £945.00/week | £833.33/week |
| Profit at optimum | £405.00/week | £416.67/week |
| MR and MC at optimum | £6/unit | £6/unit |

At £12 the linear curve gives £360 profit, **£45 below its maximum**. At £10.50 the constant-elasticity curve gives approximately £408.1633 profit, **£8.5034 below its maximum**. Regret is the lost profit relative to the maximum under the evaluated curve over the same interval. These are hypothetical financial consequences, with no assigned probabilities or claim of forecast accuracy.

Raising unit cost to £7 moves the optima to £11 and £14 and profits to £320 and approximately £357.14. A cap of £11 leaves the linear optimum unchanged and constrains constant elasticity to £11 with approximately £413.2231 profit. Adding £50 unavoidable fixed cost subtracts £50 at every price and preserves the entire optimal set.

## Mathematical approach

Inputs satisfy p0, Q0, e > 0; c, F ≥ 0; and 0 < L < U. Demand is

```text
QL(p) = max(0, Q0[1 − e(p/p0 − 1)])
QC(p) = Q0(p/p0)^(−e)
R = pQ; VC = cQ; TC = cQ + F; contribution = (p−c)Q; profit = contribution−F
```

Both demand curves share Q0, derivative −eQ0/p0 and elasticity magnitude e **locally** at p0. Linear demand has constant slope, with changing elasticity. Curvature differs elsewhere. The engine considers valid stationary points, endpoints, the linear cutoff and flat optimal intervals. The constant-elasticity formula ec/(e−1) applies only to the positive-cost interior case e>1; the remaining cases are handled separately. Some unrestricted problems have no finite maximiser even though the bounded problem has one.

For differentiable positive-demand interior solutions with nonzero Q′, `MR = p + Q/Q′ = c = MC`. A binding boundary, corner or zero-demand region need not satisfy this condition. Flat tied optima do not identify a unique price. Numerical verification uses a separate SciPy objective search with endpoint checks, independent of the analytical stationary price and graph grid. Large fixed costs are excluded from the search objective to avoid cancellation. Regret and profit changes use algebraically equivalent contribution differences for the same reason.

## Five completed investigations

The standard baseline is the benchmark above. Only the stated variable changes in each comparison.

| Investigation | Controlled change |
|---|---|
| Elasticity | e = 0.5, 1, 1.5, 2, 3 |
| Unit cost | c = £6 versus £7 |
| Price restrictions | upper limit £15 versus £11 |
| Fixed cost | F = £0 versus £50/week |
| High cost and zero-demand plateau | c = £6 versus £20, holding F = £50/week and bounds £1–£20 |

The last scenario has a deliberately different baseline. At c=20 the linear optimal set is £15–£20, zero sales, profit −£50. Constant elasticity has optimum £20, 25 units/week and profit −£50. Equal profits need not mean equal quantities or a unique solution.

`investigation_worksheet.md` retains its original filename but is a **complete generated findings report**, not an unfinished worksheet. Its equations, substitutions, calculations and interpretations remain available. `FINDINGS_SUMMARY.md` gives a shorter account, including model-dependent pricing risk.

## What to explore

- **Pricing dashboard:** conditional optimal-price cards, a chosen test price, starting/chosen/optimal financial comparisons, cross-model regret, and demand/profit/revenue graphs. Download full-precision CSVs with all assumptions.
- **Mathematics and verification:** local demand matching, derivatives, maximum checks, complete tied price sets, independent numerical search and the applicable MR = MC condition.
- **Investigations and findings:** five completed controlled investigations, workings, CSVs, full report and concise findings summary.
- **Methodology and limitations:** the distinction between a result proved within assumptions and evidence that those assumptions describe real demand.

Use the sidebar to change shared inputs. Both models use the same **economic** interval. Graph zoom affects only the view. The chosen price is restricted to the permitted interval and moves to the nearest bound if an interval change excludes it. Starting-price results remain available, with a warning, when that calibration price is infeasible. Period selection **relabels** quantities and fixed costs; it does not convert days, weeks or months. Enter consistent period totals.

Financial comparisons include quantity, revenue, variable cost, contribution, profit and change from starting profit. Profit percentages appear only with a positive starting-profit denominator. Full optimal sets are preserved: tables and cross-model comparisons use the smallest tied price as a representative; other prices in that set can have different quantities or outcomes under the other curve.

## Methodology and limitations

AI assisted with code implementation, review and explanatory drafting. Financial results are calculated deterministically from the stated equations; automated tests and independent equation scripts check the implementation. Will's personal contribution and understanding checks are not verified by those automated results. `APPLICATION_NOTES.md` keeps draft application wording and an unchecked personal checklist outside the public app and findings report.

These are illustrative demand functions, continuous quantities and constant unit costs. There is no fitted empirical dataset, capacity limit, competitor response, demand uncertainty distribution or shutdown option. The constant-elasticity benchmark predicts 10,000 units/week at £1, £10,000 revenue and a £50,000 loss: an implication of the assumed curve and absent capacity limits, not a realistic forecast. Linear demand has an abrupt finite cutoff. A higher model-implied profit does not prove a curve is better.

Changing own-price elasticity does not independently identify a substitution effect; there is no competitor-price or compensated-demand model. Fixed cost is unavoidable even with zero sales. A real decision would need evidence about demand across prices, costs and capacity. Finite floating-point range also limits extreme inputs: unavailable secondary comparisons show warnings while safe results remain visible.

## Run locally

Use **Python 3.12** (the verified version). Extract this ZIP, open a terminal in `demand-pricing-explorer`, then run:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
bash run.sh
```

Open **http://127.0.0.1:8501/** on the same computer. The Bash launcher starts a background process and checks its health; the computer must stay on. To manage it:

```bash
bash run.sh status
bash run.sh stop
bash run.sh foreground
```

The launcher selects the project's `.venv`, the activated environment or Python on PATH. Missing packages produce setup instructions. Its fixed port is 8501; an unrelated service occupying that port is left running. Use `.runtime/streamlit.log` for diagnostics. A running but unhealthy project process remains available to `stop`. The launcher checks process ownership before stopping anything.

### Reopen next time on your Mac

After the one-time setup, open Terminal in this project folder and run:

```bash
bash run.sh
bash run.sh status
```

Then open **http://127.0.0.1:8501/**. No environment activation or package installation is needed again: the launcher automatically uses this folder's `.venv`. Repeating `bash run.sh` reuses a healthy running instance. Keep the project folder and `.venv` together.

The server runs locally on your Mac, in a separate process session, and remains running after the launch command or terminal finishes. It must be started again after a Mac restart or an explicit `bash run.sh stop`. Merely reopening a saved browser tab does not start Python; if no server is listening, the browser reports `ERR_CONNECTION_REFUSED`. The ZIP deliberately excludes virtual environments and runtime files, so another extracted copy needs the one-time setup first. A forwarded-port URL is only needed when you deliberately run Streamlit on another machine.

The portable foreground alternative, also useful for diagnosing errors, is:

```bash
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Stop foreground mode with **Ctrl+C**. `run.sh` requires Bash and is tested on macOS. On **Windows PowerShell**, use Python 3.12 and run (activation is unnecessary):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

If `python3.12` (or `py -3.12` on Windows) is unavailable, install Python 3.12 and reopen the terminal before setup. Do not use the macOS system Python 3.9 for these pinned dependencies. Dependencies require an internet connection on first installation; the application then needs no account, API key or remote service. `requirements.txt` contains the Cloud/runtime packages, including Jinja2 for formatted financial tables. `requirements-dev.txt` adds pytest. `requirements-lock.txt` records the full earlier tested environment for optional exact reproduction; Community Cloud uses `requirements.txt`.

## Reproduce and verify

With the environment active, run:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python evidence/verify_worksheet.py
python generate_report.py
```

The verification script independently computes all 26 saved scenario rows from direct equations, checks both optimisers, and regenerates the five scenario CSVs and JSON. The report generator rebuilds the full report, concise summary and benchmark chosen-price/model-risk CSVs. The chosen-price saved example uses £12. Live comparisons use the current input.

Tests include direct equations for new comparisons, zero/loss percentage denominators, interval boundaries, tied solutions, full-precision exports, numerical search, MR = MC exceptions, launcher ownership and interface interactions. See `VERIFICATION.md` for checks actually performed and their limits. Automated agreement is evidence about the software; it does not establish a personal handwritten check or empirical accuracy.


These checks are automated. They do not mean the project owner personally performed each check. The original and publication-preparation results are recorded separately in [VERIFICATION.md](VERIFICATION.md).

## Project files

| File | Purpose |
|---|---|
| `app.py` | Streamlit dashboard, charts, investigations and downloads |
| `models.py` | Validation, demand, finances, analytical/numerical optimisation and MR check |
| `analysis.py` | Comparison calculations, controlled investigations and generated reports |
| `generate_report.py` | Rebuild report, summary and comparison evidence |
| `maths_explanation.md` | Detailed derivations and exceptions |
| `investigation_worksheet.md` | Complete generated findings report |
| `FINDINGS_SUMMARY.md` | Concise generated findings |
| `APPLICATION_NOTES.md` | Draft CV/statement/interview material and personal checks |
| `evidence/` | Reproducible CSV/JSON results and independent equation audit |
| `tests/` | Model, comparison, analysis, UI and launcher checks |
| `requirements.txt` | Runtime dependencies for Streamlit Community Cloud |
| `requirements-dev.txt` | Runtime packages plus pytest for local checks |
| `requirements-lock.txt` | Full package snapshot for optional reproduction |
| `PUBLISHING.md` | Step-by-step GitHub upload, Cloud deployment and link checks |
| `VERIFICATION.md` | Baseline, final validation and known verification limits |

## Publish on GitHub and Streamlit Community Cloud

Follow [PUBLISHING.md](PUBLISHING.md) for beginner-friendly instructions. Upload this folder's **contents** to the repository root so `app.py`, `requirements.txt`, `models.py`, `analysis.py`, `maths_explanation.md` and `.streamlit/config.toml` retain their relative paths. Keep `tests/`, `evidence/` and all Markdown documentation too.

Use repository `demand-pricing-explorer`, branch `main`, **main file path `app.py`**, and **Python 3.12** in Advanced settings. No secrets are needed. Community Cloud launches the Python entry point; `run.sh` manages the local preview only. No database, API account or system-package file is required for the supplied app. [Official deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).

After deployment, test the real HTTPS app in a private browser window and add that URL and your real repository link to your CV. No repository, live URL, deployment or personal test result has been invented here.

## Localhost and hosted links

`http://127.0.0.1:8501/` works only on the computer running the local server; it is not a link for recruiters. A Community Cloud deployment runs independently of your Mac and supplies an HTTPS `streamlit.app` address. Keep the GitHub source repository available as the evidence behind that app.

In a remote development environment, a development server may instead need a forwarded-port preview. That is separate from a Community Cloud deployment. Local startup remains available through the retained Bash launcher.
