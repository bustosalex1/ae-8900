import asyncio
import random
from datetime import datetime
from fastapi import FastAPI, WebSocket

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "This is my AE 8900 backend!"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        await asyncio.sleep(0.1)
        await websocket.send_json({"data": random.random() * 150, "timestamp": datetime.now().timestamp()})
