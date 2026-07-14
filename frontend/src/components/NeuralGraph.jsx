import React, { useRef, useCallback, useState, useEffect } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

const NeuralGraph = () => {
  const fgRef = useRef();
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });

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
    fgRef.current.centerAt(node.x, node.y, 1000);
    fgRef.current.zoom(8, 2000);
  }, [fgRef]);

  return (
    <div className="w-full h-full bg-zinc-950 flex flex-col">
      <h2 className="text-xl font-bold p-4 text-zinc-100 border-b border-zinc-800">
        Neural RAG - Graph View
      </h2>
      <div className="flex-1 overflow-hidden relative">
        <ForceGraph2D
          ref={fgRef}
          graphData={graphData}
          nodeId="id"
          nodeLabel="name"
          nodeColor={node => {
            switch(node.group) {
              case 1: return '#3b82f6';
              case 2: return '#10b981';
              case 3: return '#8b5cf6';
              default: return '#6b7280';
            }
          }}
          linkColor={() => 'rgba(255, 255, 255, 0.4)'}
          backgroundColor="#09090b"
          onNodeClick={handleNodeClick}
          cooldownTicks={100}
          enableZoomInteraction={true}
          enablePanInteraction={true}
        />
      </div>
    </div>
  );
};

export default NeuralGraph;
