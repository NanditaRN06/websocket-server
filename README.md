# FastAPI WebSocket Device Messaging Server

A lightweight FastAPI WebSocket server that allows real-time messaging between devices using unique device IDs.

> **Live Deployment:** `https://websocket-server-ihw6.onrender.com`

## Features

1. WebSocket-based real-time communication.
2. Device registration using `device_id`.
3. Send messages from one device to another.
4. In-memory device connection tracking.
5. Easily deployable on Render.
6. Built with FastAPI + Uvicorn

## Folder Structure

```
.
├── server.py
├── requirements.txt
└── README.md
```

## How it works !!

1. A device connects to `/ws`.
2. It registers itself by sending:
```bash
{ "device_id": "device-123" }
```
3. The server stores the WebSocket connection in memory.
4. Any device can send a message like:
```bash
{
  "to": "device-456",
  "message": "Hello from device-123"
}
```
5. The server forwards the message to the target device (if connected)

## Run 

1. Install dependencies
```bash
pip install -r requirements.txt
```
2. Start the server
```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```
3. Open in browser:

```bash
http://localhost:8000/
```
Response:
```bash
{ "status": "WebSocket server running" }
```

**Web-Socket Endpoint:**
```bash
ws://localhost:8000/ws
```

## Limitations

1. Device connections are stored in memory.
2. Restarting the server clears all connections.
3. No authentication or persistence (intentional for simplicity)
