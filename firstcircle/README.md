# FirstCircle

FirstCircle is an online-to-offline connection platform that aggregates activity proposals called "Drops" and matches users into small "Circles" (3-6 people) based on interests, schedules, and reliability scores. 

## Project Structure

```text
firstcircle/
├── frontend/           # Vite, React, Tailwind CSS dashboard UI
├── backend/            # FastAPI, SQLite matching and business services
├── database/           # Relational schema and initial seed data
└── docs/               # Project spec and logic documentation
```

## Setup & Running

### Prerequisites
*   Node.js (v18+)
*   Python (3.8+)

### Backend setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a python virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install npm packages:
   ```bash
   npm install
   ```
3. Launch the Vite dev server:
   ```bash
   npm run dev
   ```

## Development Features
*   **Automatic Matching**: Proposes groups based on TF-IDF cosine similarity of user interests, calendar slot alignment, and geographic distances.
*   **Reliability Ratings**: Penalizes no-shows and flakes dynamically.
*   **Safety Soft-Blacklists**: Suppresses matches for reported or skipped users.
