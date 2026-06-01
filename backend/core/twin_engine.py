import numpy as np
import json
import time

class BrainTwinEngine:
    def __init__(self, num_nodes=5, dt=0.01):
        self.N = num_nodes
        self.dt = dt
        self.t = 0.0
        
        self.node_ids = ['A0', 'V0', 'M0', 'Mot0', 'Lim0']
        self.node_types = ['sensory', 'sensory', 'superhub', 'motor', 'limbic']
        
        self.E = np.random.uniform(0, 0.1, self.N)
        self.I = np.random.uniform(0, 0.1, self.N)
        
        self.axial_resistance = np.ones(self.N) * 1.0
        self.sigmoid_gain = np.ones(self.N) * 1.5
        self.threshold = np.ones(self.N) * 0.5
        
        self.theta = np.random.uniform(0, 2*np.pi, self.N)
        self.omega = np.random.uniform(8, 12, self.N)
        
        self.dopamine = np.ones(self.N) * 50.0
        self.noradrenaline = np.ones(self.N) * 20.0
        
        self.W = np.random.uniform(0.1, 0.5, (self.N, self.N))
        np.fill_diagonal(self.W, 0)

        self.disease_stage = 0.0
        self.disease_rate = 0.03  # Acelerado para ver el colapso en ~30s
        self.is_degenerating = False
        
        self.vulnerability = np.array([0.2, 0.2, 1.0, 0.1, 0.9])
        self.max_axial_resistance = 10.0
        self.min_sigmoid_gain = 0.3
        
        self.pacing_active = np.zeros(self.N, dtype=bool)
        self.pacing_freq = 40.0
        self.pacing_amplitude = 0.8

    def process_command(self, cmd_json):
        try:
            data = json.loads(cmd_json)
            if data["command"] == "pace_node":
                target_idx = self.node_ids.index(data["target"])
                self.pacing_active[target_idx] = True
                self.pacing_freq = data.get("frequency", 40.0)
                print(f"Motor: Estimulación iniciada en {data['target']} a {self.pacing_freq}Hz")
                
            elif data["command"] == "set_neuromodulator":
                target_idx = self.node_ids.index(data["target"])
                if "dopamine" in data:
                    self.dopamine[target_idx] = float(data["dopamine"])
                    self.sigmoid_gain[target_idx] = 1.5 + (self.dopamine[target_idx] - 50) * 0.02
                if "noradrenaline" in data:
                    self.noradrenaline[target_idx] = float(data["noradrenaline"])
                    self.threshold[target_idx] = 0.5 - (self.noradrenaline[target_idx] - 20) * 0.005
        except Exception as e:
            pass

    def _sigmoid(self, x, a, theta):
        return 1.0 / (1.0 + np.exp(-a * (x - theta)))

    def _wilson_cowan_step(self):
        tau_e, tau_i = 0.01, 0.02
        global_input = np.dot(self.W, self.E) / self.axial_resistance
        
        external_stim = np.zeros(self.N)
        for i in range(self.N):
            if self.pacing_active[i]:
                external_stim[i] = self.pacing_amplitude * np.sin(2 * np.pi * self.pacing_freq * self.t)

        dE = (-self.E + self._sigmoid(global_input - self.I + external_stim, self.sigmoid_gain, self.threshold)) / tau_e
        dI = (-self.I + self._sigmoid(self.E, self.sigmoid_gain, self.threshold)) / tau_i
        
        self.E += dE * self.dt
        self.I += dI * self.dt

    def _kuramoto_step(self):
        K_global = 2.0
        dTheta = np.zeros(self.N)
        for i in range(self.N):
            phase_interaction = np.sum(self.W[i, :] * np.sin(self.theta - self.theta[i]))
            dTheta[i] = self.omega[i] + (K_global / self.N) * phase_interaction
        self.theta = (self.theta + dTheta * self.dt) % (2 * np.pi)

    def _hebbian_plasticity(self):
        alpha, beta = 0.05, 0.01
        for i in range(self.N):
            for j in range(self.N):
                if i != j:
                    dW = alpha * self.E[i] * self.E[j] - beta * self.W[i, j]
                    self.W[i, j] = np.clip(self.W[i, j] + dW * self.dt, 0, 1.0)

    def trigger_degeneration(self):
        self.is_degenerating = True
        print("Atención: Cascada patológica iniciada. Monitoreando topología.")

    def _pathology_progression(self):
        if not self.is_degenerating or self.disease_stage >= 1.0:
            return
        self.disease_stage += self.disease_rate * self.dt
        damage_axial = (self.max_axial_resistance - 1.0) * self.disease_stage * self.vulnerability
        self.axial_resistance = 1.0 + damage_axial
        damage_gain = (1.5 - self.min_sigmoid_gain) * self.disease_stage * self.vulnerability
        self.sigmoid_gain = np.clip(1.5 - damage_gain, self.min_sigmoid_gain, 1.5)

    def step(self):
        self._wilson_cowan_step()
        self._kuramoto_step()
        self._hebbian_plasticity()
        self._pathology_progression()
        self.t += self.dt
        
    def calculate_order_parameter(self):
        complex_order = np.sum(np.exp(1j * self.theta)) / self.N
        return np.abs(complex_order)

    def get_telemetry_json(self):
        nodes_data = []
        for i in range(self.N):
            nodes_data.append({
                "id": self.node_ids[i], "type": self.node_types[i],
                "phase": self.theta[i] / (2*np.pi), "active": bool(self.E[i] > 0.6),
                "pop_E": float(self.E[i]), "pop_I": float(self.I[i]),
                "axial_resistance": float(self.axial_resistance[i]),
                "sigmoid_gain": float(self.sigmoid_gain[i]),
                "threshold": float(self.threshold[i]),
                "dopamine": int(self.dopamine[i]),
                "noradrenaline": int(self.noradrenaline[i])
            })
            
        links_data = []
        for i in range(self.N):
            for j in range(self.N):
                if self.W[i, j] > 0.05:
                    links_data.append({
                        "source": self.node_ids[i], "target": self.node_ids[j],
                        "weight": float(self.W[i, j]), "type": "excitatory"
                    })
                    
        return json.dumps({
            "timestamp": time.time(),
            "global_sync": float(self.calculate_order_parameter()),
            "nodes": nodes_data, "links": links_data
        })