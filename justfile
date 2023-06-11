# start the frontend development server
start-frontend:
    cd frontend && pnpm run dev

start-backend:
    cd backend/src && uvicorn main:app --reload
