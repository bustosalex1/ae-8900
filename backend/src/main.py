"""Entrypoint into AE-9000 backend."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import crud, websocket

app = FastAPI()
app.include_router(crud.router)
app.include_router(websocket.router)

origins = [
    "http://localhost:5173",
    "https://localhost:5173",
    "http://localhost",
    "https://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
