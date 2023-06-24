"""Entrypoint into my AE 8900 backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.management.dependencies import get_settings
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

settings = get_settings()

if settings.host_ip is not None:
    origins.extend(
        [
            f"http://{settings.host_ip}:5173",
            f"https://{settings.host_ip}:5173",
            f"http://{settings.host_ip}",
            f"https://{settings.host_ip}",
        ]
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
