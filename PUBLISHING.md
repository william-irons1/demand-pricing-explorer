# Publish Demand & Pricing Explorer

This guide prepares two different links: a GitHub repository containing the investigation and an HTTPS website hosted by Streamlit Community Cloud. Nothing has been uploaded or deployed for you. The steps below are actions for you to take when ready.

## 1. Extract and check the project

1. Download `demand-pricing-explorer-github.zip` and extract it.
2. Open its `demand-pricing-explorer` folder. You should see `app.py`, `README.md` and `requirements.txt` directly inside it.
3. On a Mac, press **Command + Shift + .** in Finder to show hidden files. Confirm `.gitignore` and `.streamlit/config.toml` are present.
4. Use this clean extracted copy for uploading. It contains no virtual environment, runtime logs, temporary files or credentials. `.gitignore` helps Git users exclude such files later; a manual browser upload still requires you to select the correct files.

The repository root should look like this (other supplied documents remain alongside these):

```text
demand-pricing-explorer/
├── app.py
├── models.py
├── analysis.py
├── generate_report.py
├── requirements.txt
├── requirements-dev.txt
├── requirements-lock.txt
├── README.md
├── PUBLISHING.md
├── maths_explanation.md
├── investigation_worksheet.md
├── FINDINGS_SUMMARY.md
├── APPLICATION_NOTES.md
├── VERIFICATION.md
├── run.sh
├── .gitignore
├── .streamlit/
│   └── config.toml
├── tests/
│   └── ... all supplied tests
└── evidence/
    └── ... all supplied CSVs, JSON and verification script
```

`APPLICATION_NOTES.md` contains clearly labelled draft application material and personal checks. It is supporting documentation, not a claim that you personally wrote or verified every part. It is not displayed in the app.

## 2. Upload to your existing GitHub account

1. Sign in to [GitHub](https://github.com/) and open [Create a new repository](https://github.com/new).
2. Choose your own account as **Owner**. Enter **demand-pricing-explorer** as the repository name.
3. Suggested description: **Mathematical and economic modelling of demand, pricing, revenue and profitability using matched demand curves and controlled investigations.**
4. Choose **Public** if you want recruiters and admissions tutors to read the source without an invitation. Leave automatic README and `.gitignore` creation off; this package supplies both. Click **Create repository** when you are ready to publish it.
5. On the empty repository page, select **uploading an existing file**. If there are already files, choose **Add file → Upload files**.
6. Open the extracted project folder in Finder. Select its **contents**, including hidden files and the `tests`, `evidence` and `.streamlit` folders, and drag them into GitHub's upload area. **Do not upload the ZIP or the outer project folder as an extra directory.**
7. Check the preview. `app.py` must be at the top level, rather than `demand-pricing-explorer/app.py` inside the repository. Use commit message **Prepare Demand and Pricing Explorer for publication**, then commit to `main`.
8. Open the repository's main page and check that README renders, `.gitignore` is present, `.streamlit/config.toml` opens, and `tests/` and `evidence/` contain their files. If the branch name differs from `main`, use that actual branch in the Cloud form.

If a hidden file did not upload, select **Add file → Create new file**, type its exact path (for example `.streamlit/config.toml`), paste the contents of the corresponding supplied file and commit it. Repeat for `.gitignore` if needed.

These steps follow GitHub's [repository quickstart](https://docs.github.com/en/repositories/creating-and-managing-repositories/quickstart-for-repositories) and [file upload guide](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).

## 3. Deploy the app

1. Open [Streamlit Community Cloud](https://share.streamlit.io/) and sign in, connecting your GitHub account when prompted.
2. Select **Create app**, then **Yup, I have an app** if asked.
3. Use these settings:

| Setting | Enter/select |
|---|---|
| Repository | Your GitHub username / `demand-pricing-explorer` |
| Branch | `main`, or the actual uploaded branch |
| Main file path | **`app.py`** |
| Advanced settings → Python version | **3.12** |
| Secrets | Leave blank; this project needs none |
| App URL/subdomain | Choose an available name, or accept the generated one |

4. Save the advanced settings and click **Deploy** when ready. Watch the build logs until the dashboard opens. This is the step that publishes the website.

These settings follow Streamlit's [deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy). Community Cloud reads the repository's runtime dependencies from `requirements.txt`; the main file is `app.py`, not `run.sh`. The theme file stays at `.streamlit/config.toml`. See [file organisation](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization) and [dependencies](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies).

## 4. Check the public website before adding it to applications

The deployed app provides its actual HTTPS `streamlit.app` address. Copy that address from the browser; do not use `127.0.0.1`, `localhost`, a deployment-log page or this guide's example names.

Open the real website in a private/incognito window and check:

- The page opens without a GitHub or developer login. If access is restricted, review **App settings → Sharing → Who can view this app**. Use the public-view setting when you intend to share it openly. [Official sharing guidance](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app).
- The benchmark gives optimal prices **£10.50** and **£12**, with profits **£405** and approximately **£416.67/week**.
- A chosen price of **£12** gives linear profit **£360/week**, and the model-risk table shows approximately **£45** and **£8.50** cross-model losses. These are illustrative model outputs.
- Profit, demand and revenue graphs render; a cost or price-limit change updates results.
- All five investigations, mathematical explanations and download buttons open correctly. Download a comparison CSV and a report.
- The page is readable on your phone. Check the actual links again shortly before submitting an application.

These are checks for **you to complete after deployment**; local automated checks do not establish that a hosted app has been tested. Community Cloud may put an inactive app to sleep; visiting it allows it to wake. See [app management and hibernation](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app). A cold start is different from a permanent broken link.

## 5. Add the real links

Once both are public and checked:

1. Copy your repository's actual URL from GitHub.
2. Copy your deployed app's actual HTTPS URL.
3. Edit README's publication-status paragraph to include **Live app** and **Source repository** links with those real addresses. Commit the edit.
4. Add the live app URL to the GitHub repository's **About → Website** field.
5. On your CV, use a short label such as **Demand & Pricing Explorer — live app | source and findings**, linking the two parts to the actual website and repository. Describe results as hypothetical and model-implied; do not claim real savings or personally completed checks you have not done.

No repository or live URL is supplied here because neither has been published by this preparation task.

## Common deployment problems

| Symptom | What to check |
|---|---|
| `app.py` cannot be found | Upload the extracted contents at the repository root and select the correct branch; enter exactly `app.py`. |
| Missing Python package | Ensure `requirements.txt` is committed beside `app.py`. Use Python 3.12 and inspect the first installation error in the Cloud logs. |
| Missing `maths_explanation.md` or local module | Upload every supplied Python/Markdown file; keep the exact filenames and case. |
| A dependency fails to build | Check the selected Python version and first failing package in the logs. Do not remove the pin or replace tested mathematics merely to suppress an error. |
| Localhost refuses to connect | That URL is only a local preview. Use the deployed HTTPS address for applications; use `bash run.sh` to start a local instance. |
| Website asks visitors to sign in | Check the public-view sharing setting and retest in a private window. |
| App is asleep | Visit it and follow the wake prompt; then recheck the dashboard. |

Use Cloud's **Manage app** logs for deployment failures. The prepared project was checked locally and its Linux package resolution was inspected, but a real Cloud deployment can only be confirmed after you publish it.

## Running or testing a local copy

On a Mac with Python 3.12 installed, open Terminal in the extracted project folder:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
bash run.sh
```

For automated checks, install the development requirements, then run:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python evidence/verify_worksheet.py
python generate_report.py
```

`requirements-dev.txt` adds pytest; Cloud only needs `requirements.txt`. The full README includes Windows commands and local start/status/stop instructions.
