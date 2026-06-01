import React, { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import ConnectomeGraph from './ConnectomeGraph';
import NodeTelemetry from './NodeTelemetry';
import './Dashboard.css';

const DigitalTwinDashboard = () => {
  const [networkData, setNetworkData] = useState({ nodes: [], links: [] });
  const [selectedNodeId, setSelectedNodeId] = useState(null); 
  const [kuramotoR, setKuramotoR] = useState(0);
  
  const wsRef = useRef(null);

  useEffect(() => {
    const ws = new WebSocket('wss://fuzzy-umbrella-69pvjrj6j6wj25jrr-8765.app.github.dev');
    wsRef.current = ws;
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setNetworkData({ nodes: data.nodes, links: data.links });
      setKuramotoR(data.global_sync);
    };

    return () => ws.close();
  }, []); 

  const handleNodeClick = useCallback((node) => {
    setSelectedNodeId(prev => (prev === node.id ? null : node.id));
  }, []);

  const sendCommand = (cmd) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(cmd));
    }
  };

  const selectedNodeData = useMemo(() => {
    return networkData.nodes.find(n => n.id === selectedNodeId) || null;
  }, [networkData.nodes, selectedNodeId]);

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h2>Monitor del Gemelo Cognitivo</h2>
        
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <div style={{ display: 'flex', gap: '5px', backgroundColor: '#1a1a1a', padding: '5px', borderRadius: '5px', border: '1px solid #333' }}>
            <span style={{color: '#888', margin: '0 10px', fontSize: '0.9em'}}>Hubs:</span>
            {['A0', 'V0', 'M0', 'Mot0', 'Lim0'].map(id => (
              <button key={id} onClick={() => setSelectedNodeId(prev => prev === id ? null : id)}
                style={{ padding: '6px 10px', backgroundColor: selectedNodeId === id ? '#4facfe' : '#333', color: 'white', border: 'none', borderRadius: '3px', cursor: 'pointer', fontWeight: 'bold' }}>
                {id}
              </button>
            ))}
          </div>
          <button style={{ padding: '8px 12px', backgroundColor: '#ff4757', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }} onClick={() => sendCommand({ command: 'trigger_degeneration' })}>☣️ Alzheimer</button>
          <button style={{ padding: '8px 12px', backgroundColor: '#1e90ff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }} onClick={() => sendCommand({ command: 'pace_node', target: 'M0', frequency: 40.0 })}>⚡ 40Hz</button>
        </div>

        <div className={`sync-indicator ${kuramotoR > 0.8 ? 'healthy' : 'pathological'}`}>R: {kuramotoR.toFixed(3)}</div>
      </header>

      <main className="dashboard-layout">
        <div className="canvas-section">
          <ConnectomeGraph data={networkData} selectedNode={selectedNodeData} onNodeClick={handleNodeClick} />
        </div>
        
        {selectedNodeData && (
          <aside className="telemetry-section">
            <NodeTelemetry node={selectedNodeData} onSendCommand={sendCommand} />
          </aside>
        )}
      </main>
    </div>
  );
};

export default DigitalTwinDashboard;