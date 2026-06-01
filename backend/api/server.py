import asyncio
import websockets
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.twin_engine import BrainTwinEngine

engine = BrainTwinEngine()
connected_clients = set()

async def broadcast_telemetry():
    print("Motor biofísico iniciado. Transmitiendo telemetría a 60Hz...")
    while True:
        engine.step()
        if connected_clients:
            payload = engine.get_telemetry_json()
            websockets.broadcast(connected_clients, payload)
        await asyncio.sleep(1/60)

async def handle_client(websocket, path=None):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                if data.get("command") == "trigger_degeneration":
                    engine.trigger_degeneration()
                else:
                    engine.process_command(message)
            except:
                pass
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)

async def main():
    server = await websockets.serve(handle_client, "0.0.0.0", 8765)
    print("Servidor de Gemelo Digital ejecutándose en el puerto 8765")
    await broadcast_telemetry()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor apagado por el usuario.")