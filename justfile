# start the frontend development server
start-frontend:
    cd frontend && pnpm run dev

start-backend:
    cd backend/src && uvicorn main:app --reload

generate-api:
    npx openapi-typescript http://localhost:8000/openapi.json --output frontend/src/lib/api/schema.d.ts
    
