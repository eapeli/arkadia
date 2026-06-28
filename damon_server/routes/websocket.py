"""WebSocket routes."""
from fastapi import APIRouter, Depends, WebSocket
from pydantic import BaseModel

router = APIRouter()


class WSMessage(BaseModel):
    type: str
    payload: dict


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text(f"echo: {data}")
    except Exception:
        await ws.close()
