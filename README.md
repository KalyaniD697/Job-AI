# Job AI

Job AI is a full-stack job discovery and outreach assistant that helps users find relevant opportunities and generate professional emails for recruiters or hiring teams.

The application combines a Django REST API backend with a React frontend to make job searching, analysis, and outreach easier in one workflow.

## Overview

This project is designed to:

- search and review job listings
- extract useful details from job descriptions
- analyze roles and requirements
- generate polished outreach messages
- present results in a simple and user-friendly interface

## Features

- Job search and listing flow
- Job description analysis
- Contact and email generation support
- Structured backend APIs for frontend integration
- Responsive React-based UI
- Local SQLite database for development

## Tech Stack

- Backend: Python, Django, Django REST Framework
- Frontend: React, Vite, JavaScript
- Database: SQLite
- Version Control: Git / GitHub

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
├── package-lock.json
└── .env
```

## Prerequisites

Before running the app, make sure you have:

- Python 3.10+
- Node.js 18+
- npm
- Git

## Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

> If the project uses a `.env` file, keep your environment variables in `backend/.env` and do not commit sensitive values.

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Run the Application

1. Start the Django backend
2. Start the React frontend
3. Open the local address provided by Vite in your browser

## Development Notes

- The app is currently set up for local development.
- Secret keys and private configuration should remain in environment variables.
- The repository includes a root-level `.gitignore` to avoid committing generated files and local secrets.

## License

This project is for educational and personal use.

## Author

Kalyani Dukka
