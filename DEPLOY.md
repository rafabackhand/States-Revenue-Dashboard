# Deploy the dashboard online (free)

This guide puts your dashboard on the internet at a public URL like
`https://bihar-revenue.onrender.com`, using **GitHub** (to hold your code)
and **Render.com** (to run it). Both free. One-time setup takes about
15 minutes.

---

## What was already prepared

Before you start, these files have been set up for you:

| File | What it does |
|---|---|
| `app.py` | The dashboard (was `05_dashboard.py` — renamed because hosting platforms can't import a Python file whose name starts with a digit) |
| `requirements.txt` | Shopping list of Python libraries Render needs to install |
| `.gitignore` | Tells Git what NOT to upload (the `venv/` folder etc.) |
| `DEPLOY.md` | This guide |

You do **not** need to install anything on your laptop. Everything below
happens in your browser.

---

## Step 1 — Create a GitHub account (skip if you already have one)

1. Go to **https://github.com/signup**
2. Pick any username, email, password. Use a personal email if you don't
   want this tied to work.
3. Verify email. You're done.

---

## Step 2 — Create an empty repository

"Repository" is just a folder that lives on GitHub.

1. Once logged in, click the **+** icon (top right) → **New repository**
2. Repository name: **`bihar-revenue-dashboard`** (or any name you like)
3. Description: "Indian state revenue explorer — Dash app"
4. Choose **Public** (required for the free Render tier to work cleanly)
5. Leave all other options unchecked (don't add README, .gitignore, or licence — we already have files)
6. Click **Create repository**

GitHub shows you an empty repo page. Leave that tab open.

---

## Step 3 — Upload your project files

On that empty-repo page, look for the link: **"uploading an existing file"**
(it's in the "Quick setup" box).

1. Click **uploading an existing file**.
2. Open **Finder** → navigate to:
   `OneDrive - A c GeM CAG of INDIA` → `bihar-revenue-analysis`
3. Select **all files and folders** inside (⌘+A), including:
   - `app.py`
   - `01_explore.py`, `02_build_master.py`, `03_peer_analysis.py`, `04_visualize.py`
   - `requirements.txt`
   - `.gitignore` (it's hidden — press ⌘+Shift+. in Finder to show hidden files)
   - `DEPLOY.md`
   - `data/` folder (the CSV + Excel go along with the code)
   - `outputs/` folder (optional — nice to have)
   - `notebooks/` folder (optional — it's empty)

   **Do not include** the `venv/` folder (it's not there anyway since we
   left it behind on your laptop).

4. Drag and drop everything into the GitHub upload zone.
5. Scroll down. In the "Commit changes" box, type a message like
   "Initial upload".
6. Click **Commit changes**.

Wait 30 seconds. Your files appear. Leave this tab open.

---

## Step 4 — Create a Render account

1. Go to **https://render.com**
2. Click **Get Started** → choose **GitHub** to sign up (easiest path —
   it auto-connects your GitHub account)
3. Authorise Render to see your GitHub repos when prompted.

---

## Step 5 — Deploy your dashboard

1. From the Render dashboard, click **New +** → **Web Service**
2. Under "Connect a repository", find **`bihar-revenue-dashboard`** and
   click **Connect**.
3. Fill in the form:

   | Field | Value |
   |---|---|
   | **Name** | `bihar-revenue` (or anything — becomes part of your URL) |
   | **Region** | Singapore (closest to India) |
   | **Branch** | `main` |
   | **Root Directory** | *(leave blank)* |
   | **Runtime** | Python 3 *(auto-detected)* |
   | **Build Command** | `pip install -r requirements.txt` *(auto-filled)* |
   | **Start Command** | `gunicorn app:server` |
   | **Instance Type** | **Free** |

4. Scroll down. Click **Create Web Service**.

Render starts building. You'll see live logs scrolling. It does three
things:
- Downloads your code from GitHub
- Runs `pip install -r requirements.txt` (installs Dash, pandas, etc.)
- Runs `gunicorn app:server` (starts your dashboard)

Build takes **3–5 minutes**. When done, a green **"Live"** badge appears
at the top, along with your public URL (looks like
`https://bihar-revenue-abcd.onrender.com`).

Click the URL. Your dashboard is live. Share the URL with anyone.

---

## After it's live — things to know

### Free-tier sleep

Render's free tier **puts the app to sleep after 15 minutes of no
visitors**. The next visitor waits ~30 seconds for it to wake up. After
that, fast again. For personal use / showing a few people, this is fine.

If you want to keep it awake 24/7, you can:
- Upgrade Render to their $7/month Starter plan, OR
- Use a free uptime monitor like **UptimeRobot** to ping your URL every
  5 minutes (borderline — Render may detect and throttle).

### Making updates later

After the initial deploy, Render watches your GitHub repo. **Every time
you push a new commit to GitHub, Render redeploys automatically** within
a couple minutes. No re-configuration needed.

To update a file:
- Edit the file on your laptop (in the OneDrive folder)
- Go to your GitHub repo in the browser
- Click the file → pencil icon (edit) → paste new content → Commit
- OR upload-and-replace via the "Add file" → "Upload files" button
- Render picks it up and redeploys automatically

For frequent changes, it's worth learning **GitHub Desktop** (the GUI
client) — it makes edit-and-sync one button. But the web upload method
above works fine for occasional updates.

### Your data

The CSV (`data/master_revenue.csv`) is uploaded to GitHub as part of the
repo, and copied into Render when it deploys. Anyone visiting your
dashboard sees this data. Since it's all public-domain MoF data, that's
fine.

If you later want to add **private** data, don't put it in a public
GitHub repo — use Render's environment variables or a private repo
(paid plan required).

---

## Troubleshooting

**"Build failed" on Render**
Click the deploy in Render's UI and read the log — usually a missing
Python package. Add it to `requirements.txt`, commit to GitHub, Render
redeploys.

**"Application failed to respond"**
Usually means the start command is wrong or `app.py` doesn't have a
`server` variable. Check that the start command is exactly
`gunicorn app:server`.

**"Module not found" for `dash` or `pandas`**
`requirements.txt` wasn't uploaded or was misnamed. Verify it's in the
repo root.

**The URL loads but charts don't render**
Open the browser DevTools (⌘+Option+I) → Console tab. Look for errors.
Usually it's a missing callback output or a data file that wasn't
uploaded. Check that `data/master_revenue.csv` is in your GitHub repo.

**"Deploy stuck" for >10 min**
Render free-tier build servers are sometimes slow. Give it up to 15
minutes on first deploy. If still stuck, click "Manual Deploy" →
"Clear build cache & deploy".

---

## Hugging Face Spaces — alternative

If Render doesn't work out, **Hugging Face Spaces** is another free
option: https://huggingface.co/spaces. It uses Docker; slightly more
technical but no sleep timer. Ask me for a walkthrough if you want it.
