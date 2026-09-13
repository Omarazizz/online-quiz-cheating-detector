from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.connection_manager import manager

router = APIRouter()


@router.websocket("/ws/submissions")
async def submissions_websocket(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)