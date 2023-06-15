"""Entrypoint into AE-9000 backend."""
import asyncio
import random
from datetime import datetime
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from src.routers import crud

app = FastAPI()
app.include_router(crud.router)

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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Just an endpoint to test out websocket connections."""
    await websocket.accept()

    while True:
        await asyncio.sleep(0.1)
        await websocket.send_json({"data": random.random() * 150, "timestamp": datetime.now().timestamp()})
