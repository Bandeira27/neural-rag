import React, { useState, useEffect, useCallback } from 'react';
import {
  ReactFlow,
  Background,
  useNodesState,
  useEdgesState,
  Controls,
  MiniMap
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import dagre from 'dagre';

const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

const nodeWidth = 150;
const nodeHeight = 50;

const getLayoutedElements = (nodes, edges, direction = 'TB') => {
  dagreGraph.setGraph({ rankdir: direction });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  const newNodes = nodes.map((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    const newNode = {
      ...node,
      targetPosition: direction === 'LR' ? 'left' : 'top',
      sourcePosition: direction === 'LR' ? 'right' : 'bottom',
      position: {
        x: nodeWithPosition.x - nodeWidth / 2,
        y: nodeWithPosition.y - nodeHeight / 2,
      },
    };

    return newNode;
  });

  return { nodes: newNodes, edges };
};

const NeuralGraph = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNode, setSelectedNode] = useState(null);

  useEffect(() => {
    fetch('/graph.json')
      .then(res => res.json())
      .then(data => {
        const initialNodes = (data.nodes || []).map(node => ({
          id: node.id,
          data: { label: node.label || node.name, description: node.description },
          position: { x: 0, y: 0 }
        }));
        
        const initialEdges = (data.links || []).map((link, index) => ({
          id: `e${link.source}-${link.target}-${index}`,
          source: link.source,
          target: link.target,
          label: link.label,
          animated: true,
          type: "smoothstep",
        }));

        const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
          initialNodes,
          initialEdges,
          'TB'
        );

        setNodes(layoutedNodes);
        setEdges(layoutedEdges);
      })
      .catch(err => console.error('Error fetching graph data:', err));
  }, [setNodes, setEdges]);

  const handleNodeClick = useCallback((event, node) => {
    setSelectedNode(node.data);
  }, []);

  return (
    <div className="w-full h-full bg-zinc-950 flex flex-col relative">
      <h2 className="text-xl font-bold p-4 text-zinc-100 border-b border-zinc-800 z-10 bg-zinc-950">
        Neural RAG - Graph View
      </h2>
      <div className="flex-1 overflow-hidden relative">
        {selectedNode && (
          <div className="absolute right-4 top-4 bg-zinc-900 border border-zinc-800 text-white rounded-md p-4 z-10 w-80 shadow-lg">
            <div className="flex justify-between items-start mb-2">
              <h3 className="text-lg font-semibold">{selectedNode.label || selectedNode.name}</h3>
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
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={handleNodeClick}
          colorMode="dark"
          fitView
          proOptions={{ hideAttribution: true }}
        >
          <Background variant="dots" />
          <Controls />
          <MiniMap nodeColor="#4f4f4f" maskColor="rgba(0,0,0,0.5)" />
        </ReactFlow>
      </div>
    </div>
  );
};

export default NeuralGraph;
