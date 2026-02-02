from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

devices = {}

@app.get("/")
def health():
    return {"status": "WebSocket server running"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    try:
        # First message = registration
        data = await ws.receive_json()
        device_id = data["device_id"]
        devices[device_id] = ws
        print(f"{device_id} connected")

        while True:
            msg = await ws.receive_json()
            target = msg["to"]

            if target in devices:
                await devices[target].send_json(msg)

    except WebSocketDisconnect:
        devices.pop(device_id, None)
        print(f"{device_id} disconnected")
