import React, { useState, useEffect, useRef, useMemo } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

const ConnectomeGraph = ({ data, selectedNode, onNodeClick }) => {
  const containerRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });

  // Esta lógica asegura que el grafo se ajuste al tamaño exacto de su contenedor
  useEffect(() => {
    if (containerRef.current) {
      setDimensions({
        width: containerRef.current.clientWidth,
        height: containerRef.current.clientHeight
      });
    }
    
    // Opcional: Escuchar cambios de tamaño de ventana para redibujar
    const handleResize = () => {
        if (containerRef.current) {
            setDimensions({
                width: containerRef.current.clientWidth,
                height: containerRef.current.clientHeight
            });
        }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Lógica para resaltar el nodo seleccionado y sus conexiones
  const { highlightedNodes, highlightedLinks } = useMemo(() => {
    const nodes = new Set();
    const links = new Set();

    if (selectedNode) {
      nodes.add(selectedNode.id);
      // Buscar conexiones directas
      data.links.forEach(link => {
        const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
        const targetId = typeof link.target === 'object' ? link.target.id : link.target;
        
        if (sourceId === selectedNode.id || targetId === selectedNode.id) {
          links.add(link);
          nodes.add(sourceId);
          nodes.add(targetId);
        }
      });
    }
    return { highlightedNodes: nodes, highlightedLinks: links };
  }, [data, selectedNode]);

  return (
    <div ref={containerRef} style={{ width: '100%', height: '100%', overflow: 'hidden' }}>
      <ForceGraph2D
        width={dimensions.width}
        height={dimensions.height}
        graphData={data}
        nodeRelSize={8}
        // Estilo de los nodos
        nodeColor={node => {
          if (selectedNode && !highlightedNodes.has(node.id)) return 'rgba(50, 50, 50, 0.1)'; 
          return node.active ? `rgba(0, 255, 150, ${node.phase || 0.5})` : '#333';
        }}
        nodeVal={node => 10}
        // Estilo de las conexiones
        linkWidth={link => Math.abs(link.weight) * 3}
        linkColor={link => {
          if (selectedNode && !highlightedLinks.has(link)) return 'rgba(50, 50, 50, 0.05)';
          return link.weight > 0.5 ? 'rgba(0, 200, 100, 0.6)' : 'rgba(255, 50, 50, 0.4)';
        }}
        linkDirectionalParticles={4}
        linkDirectionalParticleWidth={link => (link.weight > 0.5 ? 2 : 0)}
        onNodeClick={onNodeClick}
        backgroundColor="#050505"
        nodeCanvasObject={(node, ctx, globalScale) => {
          // Dibujo personalizado para que resalten más
          ctx.beginPath();
          ctx.arc(node.x, node.y, 8, 0, 2 * Math.PI, false);
          ctx.fillStyle = (selectedNode && highlightedNodes.has(node.id)) ? '#4facfe' : '#333';
          ctx.fill();
        }}
      />
    </div>
  );
};

export default ConnectomeGraph;