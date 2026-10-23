# Verification and deployment scope

Publication preparation completed on 23 October 2026. All checks below are automated or agent-operated software checks; they do not establish which checks Will personally completed.

## Latest publication package

The latest completed local project was copied into a clean source folder. The Python application, model engine, analysis functions, launcher, tests, mathematical explanations, five investigations and supporting evidence were retained. Byte comparisons confirmed these existing files were unchanged; regeneration reproduced the saved reports and numerical evidence.

Changes for publication were limited to the README, this record, publishing instructions, dependency declarations and `.gitignore`. No calculator feature or model formula was changed.

### Fresh runtime environment

- Created an isolated Python 3.12 environment and installed only the new `requirements.txt`.
- Confirmed pytest was absent: the website does not require the test runner to execute.
- Ran Streamlit AppTest against `app.py`: no application exception/error, correct benchmark prices (£10.50/£12), profits (£405/approximately £416.67), four tabs and a Plotly chart.
- Captured and checked all eight non-empty export payloads in that runtime-only environment.
- Launched the actual `app.py` entry point in Streamlit on a separate local test port. Its health endpoint returned HTTP 200 with body `ok` in an independent call.
- `pip check`: no broken requirements.

### Complete checks with development dependencies

After installing `requirements-dev.txt` in the same fresh environment:

```text
python -m pytest -q                 407 passed
python evidence/verify_worksheet.py All 26 independent scenario rows agreed with both optimisers
python generate_report.py          Full report, summary and both comparison CSVs regenerated
python -m pip check                No broken requirements
```

The suite covers demand matching, financial equations, analytical and separate numerical optimisation, boundaries, tied optima, zero costs, elasticity below/equal/above one, fixed-cost invariance, MR = MC applicability, chosen-price comparisons, cross-model regret, full-precision exports, interface behaviour and launcher ownership/lifecycle.

### Linux deployment compatibility

A pip dry-run resolved all runtime requirements to Python 3.12 manylinux x86-64 or platform-independent wheels. This checks package availability and resolver compatibility for Linux, including the compiled NumPy, pandas and SciPy dependencies. It does not run the app on Linux or execute a Streamlit Community Cloud deployment. The app requires no non-Python system package, secret, database or external API.

The retained `.streamlit/config.toml` has theme/usage settings and no forced localhost address or port. Community Cloud launches `app.py` and uses its own server settings; the Bash launcher is for local use.

### Source and archive hygiene

- Checked `.gitignore` with Git itself: example environments, caches, logs, temporary files and credentials were excluded; application files, `.streamlit/config.toml`, tests and evidence were retained.
- The ZIP excludes virtual environments, runtime logs, cache directories, `.git` metadata, temporary files and credentials.
- The ZIP contains the root-level `app.py`, runtime requirements and every supporting file the application reads.
- A separate extraction was checked for integrity, required files, relative documentation links and preserved source/evidence contents.

## Earlier investigation verification

Before the original completion work, the existing project passed 329 tests and all 26 independently calculated scenario results. After the additions, 407 tests passed, and desktop/mobile layouts were inspected at 1280 × 720 and 390 × 844. The completed chosen-price CSV and full Markdown report downloads matched their calculations/generated text. The original benchmark, five investigations and all supported mathematical edge cases were retained.

The source has also passed real macOS local-launcher start, separate-shell status, repeated start, safe stop and restart checks. Its detached-process session fix is covered by regression tests. A prior startup follow-up created a local environment in the original finished folder and left that local server running. That environment/process is separate from this portable publication package.

## Limits and publication status

- Nothing was uploaded to GitHub or deployed to Streamlit Community Cloud during preparation. There is no assigned repository or public website URL.
- The full suite and runtime execution were checked on macOS with Python 3.12. Linux dependencies were resolved, but a Linux execution and actual Cloud build remain unperformed.
- Visual layout was inspected during the earlier completion work. This packaging pass did not repeat browser inspection; app source and graphs were unchanged and AppTest checked runtime behaviour.
- Windows instructions are supplied but were not executed on Windows.
- Local tests cannot confirm the eventual Cloud sharing permissions, availability or public URLs. Follow PUBLISHING.md to deploy and perform the hosted-app checks before using links in applications.
- The demand functions are illustrative, not fitted customer evidence. Automated agreement does not validate either curve or establish real-world savings. APPLICATION_NOTES.md retains an intentionally unchecked personal-understanding checklist.
