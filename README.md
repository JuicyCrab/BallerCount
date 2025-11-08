# BallerCount

BallerCount is a lightweight, local-first tool for recording and exploring basketball player stats. It combines a Streamlit frontend, a simple sqlite3 database backend, and the nba_api Python client to fetch NBA data and store or export results locally. This repository is intended as a small, easy-to-run project for hobbyist scorekeepers, demos, and quick data exploration.

Features
- 🏀 Record game events: points, rebounds, assists, fouls
- 🔁 Persist fetched NBA data to a local sqlite file
- 🧭 Streamlit-driven UI for search, view, and export
- 📥 Import / 📤 Export CSV & JSON
- 🧰 Small, dependency-light codebase for local use

Tech stack
- Frontend: Streamlit
- Backend / storage: sqlite3 (local file)
- Data source: nba_api (Python client)
- Language: Python 3.9+ (adjust as needed)

Prerequisites
- Python 3.9 or newer
- pip
- (Optional) virtualenv or venv for an isolated environment

Quick start (run locally)
1. Clone the repo
   git clone https://github.com/<owner>/BallerCount.git
   cd BallerCount

2. Create and activate a virtual environment (recommended)
   python -m venv .venv
   - macOS / Linux: source .venv/bin/activate
   - Windows (PowerShell): .venv\Scripts\Activate.ps1

3. Install dependencies
   pip install -r requirements.txt
   If you don't have requirements.txt, install the essentials:
   pip install streamlit nba_api pandas

4. Configure (optional)
   - By default the project looks for a sqlite database file (e.g. database.db) in the project root.
   - If the app uses environment variables, create a .env file in the project root. Example:
     ```
     APP_PORT=8501
     DB_PATH=./database.db
     NBA_API_TIMEOUT=10
     ```
     (Adjust variable names if your project uses different config keys.)

5. Run the Streamlit app
   - If the Streamlit entry point is app.py:
     streamlit run app.py
   - Or:
     python -m streamlit run app.py
   - Then open the URL shown in the terminal (usually http://localhost:8501).

Notes about sqlite
- The database is a single file (defaults: database.db or db.sqlite). To reset data locally, stop the app and remove the file:
  rm database.db
- If the repo includes migration scripts, run them as described in the project; otherwise the app will create required tables on first run.

Using the app
- Use the Streamlit UI to:
  - Search and fetch NBA players / teams via the nba_api integration
  - Store fetched results into the local sqlite database
  - Record simple game events (if event recording is implemented)
  - Export selected datasets to CSV or JSON
- If the repo exposes scripts (e.g., scripts/fetch_player.py), run them directly:
  python scripts/fetch_player.py --player "LeBron James"

Examples
- Fetch data via Streamlit UI and export:
  1. Start the app: streamlit run app.py
  2. Use the "Fetch Player" control to search and save a player
  3. Use the "Export" control to download CSV


Why there is no full deployment guide
- This project is intended as a local demo/proof-of-concept. A full deployment pipeline (Docker, CI/CD, cloud hosting) is not included deliberately to keep the project small and easy to run.
- If you later want deployment suggestions, common minimal options:
  - Containerize with Docker (use an ephemeral sqlite file or mount a volume)
  - Deploy the Streamlit app to Streamlit Community Cloud, Heroku (buildpack), or a VM; for production use, replace sqlite with a server DB (Postgres)


Contributing
- Small improvements and bug fixes welcome. Suggested flow:
  1. Fork and create a feature branch (feature/...)
  2. Add changes and (where appropriate) tests
  3. Open a PR with a short description of what you changed
- Please include meaningful commit messages and keep changes small.
