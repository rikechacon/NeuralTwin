import asyncio
import websockets
import json
import numpy as np
import time
from collections import deque

class FalconPredictor:
    def __init__(self):
        self.window_size = 100
        self.r_history = deque(maxlen=self.window_size)
        self.time_history = deque(maxlen=self.window_size)
        self.CRITICAL_R = 0.45
        self.intervention_cooldown = 0
        self.is_pacing = False

    def predict_collapse(self):
        if len(self.r_history) < self.window_size:
            return None, None

        t_array = np.array(self.time_history)
        r_array = np.array(self.r_history)
        t_relative = t_array - t_array[0]
        
        m, b = np.polyfit(t_relative, r_array, 1)
        
        if m >= 0:
            return m, float('inf')
            
        current_r = r_array[-1]
        time_to_crash = (self.CRITICAL_R - current_r) / m
        
        if time_to_crash > 0 and current_r < 0.75:
            return m, time_to_crash
        return m, float('inf')

    async def monitor_stream(self):
        uri = "ws://localhost:8765"
        print("🦅 Agente Falcon: Conectado. Analizando series temporales de fase...")
        
        async with websockets.connect(uri) as websocket:
            try:
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    
                    self.r_history.append(data["global_sync"])
                    self.time_history.append(data["timestamp"])
                    
                    if time.time() > self.intervention_cooldown:
                        self.is_pacing = False
                        slope, eta = self.predict_collapse()
                        
                        if eta is not None and eta < 5.0 and not self.is_pacing:
                            print(f"\n[ALERTA FALCON] Caída libre detectada (Pendiente: {slope:.3f}).")
                            print(f"⚠️ Colapso topológico proyectado en {eta:.1f} segundos.")
                            print("🤖 Ejecutando intervención autónoma de Lazo Cerrado...")
                            
                            cmd = json.dumps({"command": "pace_node", "target": "M0", "frequency": 40.0})
                            await websocket.send(cmd)
                            
                            self.intervention_cooldown = time.time() + 10.0
                            self.is_pacing = True
                            
            except websockets.exceptions.ConnectionClosed:
                pass

if __name__ == "__main__":
    agent = FalconPredictor()
    asyncio.run(agent.monitor_stream())