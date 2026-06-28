"""Gateway routes."""
from fastapi import APIRouter, Depends, WebSocket
from pydantic import BaseModel

router = APIRouter()


class GatewayStatus(BaseModel):
    status: str
    connected_platforms: list[str] = []


@router.get("/status", response_model=GatewayStatus)
async def gateway_status():
    return GatewayStatus(status="ok", connected_platforms=[])


@router.websocket("/ws")
async def gateway_ws(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text(f"gateway echo: {data}")
    except Exception:
        await ws.close()
