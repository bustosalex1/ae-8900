# setup the frontend
setup-frontend:
    cd frontend && pnpm install

# setup the backend
setup-backend:
    cd backend && python -m venv 8900-env
    backend/8900-env/bin/pip install -r backend/requirements.txt

# start the frontend development server
start-frontend:
    cd frontend && pnpm run dev

# start the backend development server
start-backend:
    set PYTHONPATH $(pwd)
    cd backend && uvicorn src.main:app --reload

# start both the frontend and backend development servers in a tmux session
start: stop
    tmuxp load session.yaml

# kill the active tmux session associated with the AE 8900 project
stop:
    -tmux kill-session -t development-servers

# see whether or not the development servers are running
@status:
    -tmux has-session -t development-servers && printf "\033[1;32mDevelopment server is running.\033[0m" || printf "\033[1;31mDevelopment server is not running.\033[0m"

# generate typescript API from FastAPI backend and format it with prettier. Make sure the backend server is running!
generate-api:
    npx openapi-typescript http://localhost:8000/openapi.json --output frontend/src/lib/api/schema.d.ts
    cd frontend && pnpm prettier --plugin-search-dir . --write src/lib/api/schema.d.ts

# lint the backend with ruff
lint-backend:
    -ruff backend/src

# lint the frontend with... prettier and eslint.
lint-frontend:
    -cd frontend && pnpm lint

# see if any new packages have been added to the env that are not in requirements.txt
backend-dependency-diff:
    -pip freeze | diff backend/requirements.txt -

# run a general health check on the backend
check-backend-health: lint-backend backend-dependency-diff

# run a general health check on the entire project
check-health: lint-backend backend-dependency-diff lint-frontend
