# start the frontend development server
start-frontend:
    cd frontend && pnpm run dev

# start the backend development server
start-backend:
    set PYTHONPATH $(pwd)
    cd backend && uvicorn src.main:app --reload

# generate typescript API from FastAPI backend. Make sure the backend is running!
generate-api:
    npx openapi-typescript http://localhost:8000/openapi.json --output frontend/src/lib/api/schema.d.ts

