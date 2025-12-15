
# Movie Ticket Booking — Installation

Follow these steps to set up and run this project locally.

## Requirements

- Python 3.10 or newer
- Git
- (Optional) A virtual environment tool such as `venv` or `virtualenv`

## 1. Clone the repository

```bash
git clone https://github.com/Hari-1710/movie-ticket-booking.git
cd "Movie ticket booking"
```

Note: if you already have the source, just `cd` into the project directory.

## 2. Create and activate a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

Install the Python packages listed in `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

The main dependencies used by the app are FastAPI, Uvicorn, SQLAlchemy, Jinja2 and ReportLab.

## 4. Run the application

This project exposes a FastAPI application in `main.py`. Start the development server with Uvicorn:

```bash
uvicorn main:app --reload
```

Then open your browser at:

```
http://127.0.0.1:8000/
```

## 5. Database

The app uses SQLite and will create `database.db` automatically the first time it runs. The SQLAlchemy models are declared in `models.py` and the engine is configured in `database.py`.

## 6. Default admin credentials

The simple admin check in `main.py` uses these default credentials (for development/testing only):

- Username: `admin`
- Password: `admin123`

Change this in production and replace with a secure auth method.

## 7. Generating invoices

Invoices are generated as PDF files in the `invoices/` folder using ReportLab. When a booking is completed the app writes `invoices/guest.pdf` which you can download from the `/invoice` endpoint.

## 8. Troubleshooting

- If a dependency fails to install, make sure your pip is up to date and you are using the correct Python version.
- If `uvicorn` isn't found after installation, run it via `python -m uvicorn main:app --reload`.
- If templates/static files don't load, check that you started the server from the project root (the directory that contains `templates/` and `static/`).

## 9. Next steps / suggestions

- Add proper authentication and session handling for users and admin.
- Add environment configuration (e.g., `.env`) to avoid hard-coded secrets.
- Add unit tests and a CI workflow for quality checks.

Enjoy! If you want, I can also add a small README or a one-command script to start the app.
