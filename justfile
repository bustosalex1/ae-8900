# bash only
set shell := ["bash", "-c"]

# setup the environment, I don't know of a better way to do this right now
_setup-environment:
    @read -p "Enter host IP address: " ip_address && \
    echo "PUBLIC_HOST_IP=$ip_address" > .env

# clear the environment
_clear-environment:
    echo "PUBLIC_HOST_IP=" > .env

# start the frontend development server
start-frontend: _clear-environment
    cd frontend && pnpm run dev

# start the backend development server
start-backend: _clear-environment
    cd backend/src && uvicorn ae8900.main:app --reload

# start the backend development server and expose it on the network
host-backend:
    cd backend && uvicorn src.main:app --host 0.0.0.0 --port 8000

# start the frontend development server and expose it on the network
host-frontend:
    cd frontend && pnpm run dev --host

# start both the frontend and backend servers exposed to the network in a tmux session
host: stop _setup-environment
    tmuxp load config/host.yaml

# start both the frontend and backend development servers in a tmux session
start: stop
    tmuxp load config/session.yaml

# kill the active tmux session associated with the AE 8900 project
stop:
    -tmux kill-session -t servers

# see whether or not the development servers are running
@status:
    -tmux has-session -t servers && printf "\033[1;32mDevelopment server is running.\033[0m" || printf "\033[1;31mDevelopment server is not running.\033[0m"

# generate typescript API from FastAPI backend and format it with prettier. Make sure the backend server is running!
generate-api:
    npx openapi-typescript http://localhost:8000/openapi.json --output frontend/src/lib/api/schema.d.ts
    cd frontend && pnpm prettier --plugin-search-dir . --write src/lib/api/schema.d.ts

# lint the backend with ruff
lint-backend:
    -ruff backend/src

# lint the frontend with prettier, eslint, and typescript... I think.
lint-frontend:
    -cd frontend && pnpm lint

# see what packages on the frontend are outdated
frontend-dependency-status:
    -cd frontend && pnpm outdated

# run a general health check on the entire project
check-health: lint-backend lint-frontend frontend-dependency-status

# remove old projects
remove-projects:
    rm -rf backend/projects/*
