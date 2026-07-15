import React, { useRef, useCallback, useState, useEffect, useMemo } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

const NeuralGraph = () => {
  const fgRef = useRef();
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [selectedNode, setSelectedNode] = useState(null);

  useEffect(() => {
    fetch('/graph.json')
      .then(res => res.json())
      .then(data => {
        const nodes = data.nodes || [];
        const links = (data.links || []).map(link => ({
          ...link,
          source: typeof link.source === 'object' ? link.source.id : link.source,
          target: typeof link.target === 'object' ? link.target.id : link.target
        }));
        setGraphData({ nodes, links });
      })
      .catch(err => console.error('Error fetching graph data:', err));
  }, []);

  useEffect(() => {
    if (fgRef.current) {
      // Adjust d3 physics
      fgRef.current.d3Force('charge').strength(-300).distanceMax(500);
      fgRef.current.d3Force('link').distance(50);
      fgRef.current.d3Force('center').strength(1);
      
      // Center graph after loading
      setTimeout(() => {
        if (fgRef.current) fgRef.current.zoomToFit(400, 50);
      }, 500);
    }
  }, [graphData]);

  const handleNodeClick = useCallback(node => {
    setSelectedNode(node);
    if (fgRef.current) {
      fgRef.current.centerAt(node.x, node.y, 1000);
      fgRef.current.zoom(2, 1000);
    }
  }, []);

  const forceGraphComponent = useMemo(() => (
    <ForceGraph2D
      ref={fgRef}
      graphData={graphData}
      nodeId="id"
      nodeLabel="name"
      d3VelocityDecay={0.1}
      onNodeDragEnd={node => {
        delete node.fx;
        delete node.fy;
        fgRef.current?.d3ReheatSimulation();
      }}
      nodeCanvasObject={(node, ctx, _globalScale) => {
        const label = node.label || '';
        const fontSize = 3;
        ctx.font = `${fontSize}px Sans-Serif`;
        
        // Draw circle
        const r = 4;
        ctx.beginPath();
        ctx.arc(node.x, node.y, r, 0, 2 * Math.PI, false);
        let color = '#6b7280';
        switch(node.group) {
          case 1: color = '#3b82f6'; break;
          case 2: color = '#10b981'; break;
          case 3: color = '#8b5cf6'; break;
        }
        ctx.fillStyle = color;
        ctx.fill();

        // Draw text
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.fillText(label, node.x, node.y + r + fontSize);
      }}
      linkColor={() => 'rgba(255, 255, 255, 0.4)'}
      linkDirectionalArrowLength={3.5}
      backgroundColor="#09090b"
      onNodeClick={handleNodeClick}
      cooldownTicks={100}
      enableZoomInteraction={true}
      enablePanInteraction={true}
      minZoom={0.5}
      maxZoom={5}
    />
  ), [graphData, handleNodeClick]);

  return (
    <div className="w-full h-full bg-zinc-950 flex flex-col">
      <h2 className="text-xl font-bold p-4 text-zinc-100 border-b border-zinc-800">
        Neural RAG - Graph View
      </h2>
      <div className="flex-1 overflow-hidden relative">
        {selectedNode && (
          <div className="absolute right-4 top-4 bg-zinc-900 border border-zinc-800 text-white rounded-md p-4 z-10 w-80 shadow-lg">
            <div className="flex justify-between items-start mb-2">
              <h3 className="text-lg font-semibold">{selectedNode.name || selectedNode.label}</h3>
              <button 
                onClick={() => setSelectedNode(null)}
                className="text-zinc-400 hover:text-white"
              >
                ✕
              </button>
            </div>
            <p className="text-sm text-zinc-300">
              {selectedNode.description || 'Descrição não disponível.'}
            </p>
          </div>
        )}
        {forceGraphComponent}
      </div>
    </div>
  );
};

export default NeuralGraph;
