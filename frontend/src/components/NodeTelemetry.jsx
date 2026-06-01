import React from 'react';
import './Telemetry.css';

const NodeTelemetry = ({ node, onSendCommand }) => {
  if (!node) return null;

  const handleSliderChange = (neurotransmitter, value) => {
    if (onSendCommand) {
      onSendCommand({ command: 'set_neuromodulator', target: node.id, [neurotransmitter]: parseInt(value) });
    }
  };

  return (
    <div className="telemetry-panel">
      <h3>Hub: {node.id} ({node.type})</h3><hr />
      <div className="metric-group">
        <h4>Dinámica de Población</h4>
        <div className="metric"><span>Tasa Excitatoria:</span><progress value={node.pop_E} max="1"></progress></div>
        <div className="metric"><span>Freno Inhibitorio:</span><progress value={node.pop_I} max="1" className="inhibitory-bar"></progress></div>
      </div>
      <div className="metric-group">
        <h4>Parámetros Biológicos</h4>
        <ul>
          <li><strong>R. Axial:</strong> {node.axial_resistance.toFixed(2)} MΩ</li>
          <li><strong>Ganancia:</strong> {node.sigmoid_gain.toFixed(2)}</li>
          <li><strong>Umbral:</strong> {node.threshold.toFixed(2)} mV</li>
        </ul>
      </div>
      <div className="metric-group">
        <h4>Bucle Límbico</h4>
        <div className="chemical-levels">
          <div style={{ marginBottom: '10px' }}>
            <label style={{ color: 'gold', fontSize: '0.9em', display: 'block' }}>Dopamina: {node.dopamine}%</label>
            <input type="range" min="0" max="100" value={node.dopamine} onChange={(e) => handleSliderChange('dopamine', e.target.value)} style={{ width: '100%', accentColor: 'gold', cursor: 'pointer' }} />
          </div>
          <div>
            <label style={{ color: 'tomato', fontSize: '0.9em', display: 'block' }}>Noradrenalina: {node.noradrenaline}%</label>
            <input type="range" min="0" max="100" value={node.noradrenaline} onChange={(e) => handleSliderChange('noradrenaline', e.target.value)} style={{ width: '100%', accentColor: 'tomato', cursor: 'pointer' }} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default NodeTelemetry;