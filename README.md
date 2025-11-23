# Student Management System (Streamlit + Python OOP)

## Quick start

1. Clone / extract this project and open folder in VS Code.
2. Create and activate virtual environment:
   - `python -m venv venv`
   - `venv\Scripts\activate`  (Windows CMD) or `venv\Scripts\Activate.ps1` (PowerShell)
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Run the app:
   - `python -m streamlit run ui/app.py`
5. Open the browser page Streamlit shows (usually http://localhost:8501).

## Structure
- `models/` — Student dataclass
- `services/storage.py` — JSON read/write
- `services/manager.py` — CRUD, validation, search
- `ui/` — Streamlit app
- `data/students.json` — data file
