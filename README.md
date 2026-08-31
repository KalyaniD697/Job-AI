# Job AI

Job AI is a full-stack application that helps users discover job opportunities and generate professional email outreach. It combines a Django REST API backend with a React frontend for a smooth end-to-end experience.

## Features

- Search for jobs from public job sources
- Analyze job descriptions and extract relevant details
- Generate polished outreach emails
- View job cards and contact information in the frontend
- REST API endpoints powered by Django and Django REST Framework

## Tech Stack

- Backend: Python, Django, Django REST Framework
- Frontend: React, Vite, JavaScript
- Database: SQLite for local development

## Project Structure

```text
job-ai/
├── backend/
│   ├── config/
│   ├── jobs/
│   ├── .env
│   ├── db.sqlite3
│   ├── manage.py
│   └── venv/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── .gitignore
├── README.md
└── package-lock.json
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm

## Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

If the project uses a `.env` file, make sure it exists in the backend folder and contains your environment variables.

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Running the App

1. Start the Django backend.
2. Start the React frontend.
3. Open the frontend URL shown by Vite in the browser.

## Notes

- The backend is configured for local development.
- Secret keys and private environment configuration should stay in `.env` and should not be committed to Git.

## License

This project is for educational and personal use.
