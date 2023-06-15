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

# lint the backend with ruff
lint-backend:
    -ruff backend/src

# lint the frontend with... eslint I guess?
lint-frontend:
    cd frontend && pnpm lint

# see if any new packages have been added to the env that are not in requirements.txt
backend-dependency-diff:
    -pip freeze | diff backend/requirements.txt -

# run a general health check on the backend
check-backend-health: lint-backend backend-dependency-diff

# run a general health check on the entire project
check-health: lint-backend backend-dependency-diff lint-frontend
