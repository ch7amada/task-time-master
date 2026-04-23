# Task Time Master

A minimal, fast timesheet management application built with FastAPI and HTMX.

## Features
- **CRUD Operations**: Manage timesheet entries with inline editing.
- **Fast UI**: Seamless updates powered by HTMX.
- **Export**: Download your data as CSV.
- **Auto-fill**: Intelligent defaults for quick entry.

## Stack
- **Backend**: FastAPI & SQLAlchemy
- **Frontend**: HTMX & Jinja2 — styled with Tailwind CSS + DaisyUI
- **Database**: SQLite (default)

## Getting Started
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Install Node dependencies and build CSS:
   ```bash
   npm install
   npm run build:css
   ```
   > `static/style.css` is not committed — it must be compiled locally from `app.css`.
3. Run the application:
   ```bash
   fastapi dev main.py
   ```
4. Open `http://localhost:8000` in your browser.
