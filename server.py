from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

app = FastAPI()

# In-memory registry: {device_id: websocket_connection}
devices = {}

@app.get("/")
async def health_check():
    return {"status": "ok", "active_connections": len(devices)}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    device_id = None
    
    try:
        # 1. Wait for Registration
        # We expect the first message to be the device identification
        data = await ws.receive_json()
        device_id = data.get("device_id")
        
        if not device_id:
            await ws.close(code=4003, reason="Device ID required")
            return
            
        # Register device (Overwrites existing connection if same ID connects again)
        devices[device_id] = ws
        print(f"Device connected: {device_id}")

        # 2. Message Loop
        while True:
            message = await ws.receive_json()
            target_id = message.get("to")
            
            # Relay logic
            if target_id and target_id in devices:
                target_ws = devices[target_id]
                await target_ws.send_json(message)
            elif target_id:
                # Optional: Inform sender that target is offline
                await ws.send_json({
                    "type": "error",
                    "code": "TARGET_OFFLINE",
                    "message": f"Device {target_id} is not connected."
                })
                
    except WebSocketDisconnect:
        print(f"Device disconnected: {device_id}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup on close
        if device_id and device_id in devices:
             # Only remove if it's the specific socket we're handling 
             # (handles race condition where user reconnected quickly)
             if devices[device_id] == ws:
                del devices[device_id]
