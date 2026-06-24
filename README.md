# Explainable Chess Engine

A full-stack chess engine built with React, Flask, and python-chess. It uses Minimax with Alpha-Beta pruning and features an explainability panel to justify the AI's moves based on evaluation metrics (Material, Position, Mobility, King Safety).

## Features
- **Custom Engine:** Minimax search with variable depth (Easy, Medium, Hard, Expert).
- **Explainability:** AI explains its reasoning for each move.
- **Premium UI:** Dark mode aesthetic with beautiful components.

## Prerequisites
- Node.js (v16+)
- Python 3.9+

## Local Setup

### Backend (Flask)
1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask server:
   ```bash
   python app.py
   ```
   *The API will run at `http://127.0.0.1:5000`.*

### Frontend (React + Vite)
1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The app will run at `http://localhost:5173`.*

## Deployment

### Backend (Render)
- Connect your GitHub repository to Render.
- Create a new "Web Service".
- Set the root directory to `backend`.
- The `render.yaml` file should automatically configure the build and start commands (`gunicorn app:app`).

### Frontend (Vercel)
- Connect your GitHub repository to Vercel.
- Set the root directory to `frontend`.
- Vercel will automatically detect Vite and use `npm run build` with the `vercel.json` config.
- *Note: Don't forget to update the `API_URL` in `src/App.jsx` to point to your deployed Render URL before deploying.*
