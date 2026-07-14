import React, { useRef, useCallback } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

const dummyData = {
  nodes: [
    { id: '1', name: 'Node 1', group: 1 },
    { id: '2', name: 'Node 2', group: 1 },
    { id: '3', name: 'Node 3', group: 2 },
    { id: '4', name: 'Node 4', group: 2 },
    { id: '5', name: 'Node 5', group: 3 }
  ],
  links: [
    { source: '1', target: '2' },
    { source: '1', target: '3' },
    { source: '2', target: '4' },
    { source: '3', target: '5' }
  ]
};

const NeuralGraph = () => {
  const fgRef = useRef();

  const handleNodeClick = useCallback(node => {
    // Center/zoom on node
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
          graphData={dummyData}
          nodeLabel="name"
          nodeColor={node => {
            switch(node.group) {
              case 1: return '#3b82f6';
              case 2: return '#10b981';
              case 3: return '#8b5cf6';
              default: return '#6b7280';
            }
          }}
          linkColor={() => 'rgba(255, 255, 255, 0.2)'}
          backgroundColor="#09090b" // zinc-950
          onNodeClick={handleNodeClick}
          cooldownTicks={100}
        />
      </div>
    </div>
  );
};

export default NeuralGraph;
