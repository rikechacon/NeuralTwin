# NeuralTwin: Gemelo Digital Cognitivo de Lazo Cerrado 🧠⚡

NeuralTwin es un entorno de simulación biofísica y topológica en tiempo real diseñado para modelar la neurodegeneración (como la enfermedad de Alzheimer) y probar intervenciones de neuroestimulación autónoma mediante sistemas multiagente (IA).

Este proyecto fusiona la neurociencia computacional (dinámica de poblaciones y osciladores acoplados) con arquitecturas web modernas de alta velocidad, permitiendo la observación e intervención de una red neuronal simulada a 60Hz.

## 🔬 Fundamentos Matemáticos

El motor biológico (`BrainTwinEngine`) no simula neuronas individuales, sino la dinámica macroscópica de "Hubs" (nodos de alta conectividad) utilizando modelos de orden reducido:

1. **Dinámica Local (Wilson-Cowan):** Modela la tasa de disparo de poblaciones excitatorias ($E$) e inhibitorias ($I$). La neuromodulación (Dopamina/Noradrenalina) altera la ganancia ($a$) y el umbral ($\theta$) de la función sigmoide:
   $$\tau_e \frac{dE}{dt} = -E + \mathcal{S}(W \cdot E - I + I_{ext}, a, \theta)$$

2. **Dinámica Global (Kuramoto):** Modela la sincronización de fase entre los Hubs a lo largo del conectoma:
   $$\frac{d\theta_i}{dt} = \omega_i + \frac{K}{N} \sum_{j=1}^{N} W_{ij} \sin(\theta_j - \theta_i)$$

3. **Plasticidad Hebbiana y Patología:** Los pesos sinápticos ($W_{ij}$) se ajustan dinámicamente. La cascada patológica degrada la resistencia axial y la excitabilidad a lo largo del tiempo, provocando un colapso en el Parámetro de Orden global ($R$).

## 🏗️ Arquitectura del Sistema

El ecosistema se divide en tres capas interconectadas por WebSockets:

* **El Motor Biofísico (Backend - Python):** Calcula las ecuaciones diferenciales de la red de 5 nodos estandarizados (`A0`, `V0`, `M0`, `Mot0`, `Lim0`) en tiempo real.
* **Monitor de Telemetría (Frontend - React/Vite):** Interfaz gráfica (UI) que renderiza la topología utilizando un motor de físicas 2D. Permite inyectar neurotransmisores al vuelo, iniciar cascadas patológicas y aplicar marcapasos manuales.
* **Agentes Predictivos (IA - Python):** Subsistemas autónomos (ej. `FalconPredictor`) que observan la serie temporal de Sincronía Global ($R$). Utilizan regresiones lineales sobre ventanas de memoria para predecir colapsos inminentes y disparar estimulaciones preventivas a 40Hz (Gamma Entrainment).

## 🚀 Instalación y Ejecución

Asegúrate de tener instalado Python 3.10+ y Node.js.

### 1. Levantar el Motor (Backend)
```bash
pip install numpy websockets
python backend/api/server.py
(Asegúrate de exponer el puerto 8765 de forma pública si usas entornos en la nube como GitHub Codespaces).
```

---
2. Levantar la Interfaz Visual (Frontend)
En una nueva terminal:
```Bash
cd frontend
npm install
npm run dev
Abre la URL proporcionada por Vite (usualmente en el puerto 5173).
```

---
3. Activar la Inteligencia Artificial (Agente Falcon)
En una tercera terminal:
```Bash
python agents/falcon_predictive.py
Prueba el sistema iniciando la patología desde la web y observa cómo el agente Falcon interviene autónomamente cuando detecta una pendiente de caída crítica.
📄 Licencia y Autores
Desarrollado como investigación independiente en la intersección de la neurotecnología y los sistemas multiagente predictivos.

