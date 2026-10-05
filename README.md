# VYB Labs

Professional client-facing website built with Flask, SQLAlchemy, HTML, CSS and JavaScript.

## Local setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Admin dashboard

Create a `.env` file from `.env.example` and set a strong `ADMIN_PASSWORD`.
Then open `/admin`.

## Before deployment

- Verify the public contact email: `vyblabs1@gmail.com`.
- Set a strong `SECRET_KEY` and `ADMIN_PASSWORD`.
- Use PostgreSQL through `DATABASE_URL` for production.
- Replace project placeholders/links as more project details become available.
- Add your LinkedIn URL when ready.
