# Alex's AE 8900 Project

A repo for my AE 8900 project.

## Repository Structure

I'm not really sure if this is a bad idea, but right now I am managing this repository as a monorepo
with the frontend and backend in the same repository, like so:

```bash
.
├── backend
│   ├── 8900-env
│   └── requirements.txt
├── docs
│   ├── notes.org
│   ├── proposal.org
│   └── timeline.org
├── frontend
│   ├── node_modules
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── README.md
│   ├── src
│   ├── static
│   ├── svelte.config.js
│   ├── tsconfig.json
│   └── vite.config.ts
└── README.md
```

The main top-level directories for this project are `backend`, which is where the FastAPI backend
resides, `frontend` , where the SvelteKit frontend resides, and `docs`, where I am currently storing
notes and other documents relevant to the project as a whole. Eventually I will need to version
control firmware source code for the system under test demonstrator, but right now I'm not sure if I
want to put that here or in a different repository.
