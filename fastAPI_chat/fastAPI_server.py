from fastapi import FastAPI, WebSocket
import asyncio

app = FastAPI()

# Store active WebSocket connections
active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for connection in active_connections:
                # You might want to add additional logic here to handle
                # broadcasting messages only to certain users, etc.
                await connection.send_text(f"Message: {data}")
    except Exception as e:
        active_connections.remove(websocket)

# Run the server with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
