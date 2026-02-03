from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

app = FastAPI()

devices = {}

@app.get("/")
def health():
    return {"status": "WebSocket server running"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    device_id = None

    try:
        # First message = registration
        try:
            data = await ws.receive_json()
            device_id = data.get("device_id")
        except Exception:
            # If malformed JSON or other error during init
            await ws.close()
            return

        if not device_id:
            await ws.close()
            return

        devices[device_id] = ws
        print(f"{device_id} connected")

        while True:
            try:
                msg = await ws.receive_json()
                target = msg.get("to")

                if target and target in devices:
                    target_ws = devices[target]
                    await target_ws.send_json(msg)
                else:
                    print(f"Target {target} not found for message from {device_id}")
            except Exception as e:
                 print(f"Error processing message from {device_id}: {e}")
                 # Decide whether to break or continue. excessive errors might warrant disconnect.
                 # For now, we continue to keep the connection alive.

    except WebSocketDisconnect:
        print(f"{device_id} disconnected")
    except Exception as e:
        print(f"Unexpected error for {device_id}: {e}")
    finally:
        if device_id and device_id in devices:
            devices.pop(device_id, None)
