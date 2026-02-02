from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

clients = set()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    print("Client connected")

    try:
        while True:
            msg = await ws.receive_text()
            print("Received:", msg)

            for client in clients:
                if client != ws:
                    await client.send_text(msg)

    except WebSocketDisconnect:
        clients.remove(ws)
        print("Client disconnected")
