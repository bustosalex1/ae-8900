import asyncio
import random
from datetime import datetime
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

app = FastAPI()

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


class WebsocketMessage(BaseModel):
    message: str


@app.get("/")
async def root() -> WebsocketMessage:
    return WebsocketMessage(message="this is my ae-8900 backend!")


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        await asyncio.sleep(0.1)
        await websocket.send_json({"data": random.random() * 150, "timestamp": datetime.now().timestamp()})
