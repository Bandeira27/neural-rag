import React, { useEffect } from 'react';
import NeuralGraph from './components/NeuralGraph';
import './index.css';

function App() {
  useEffect(() => {
    // Force strict dark mode
    document.documentElement.classList.add('dark');
  }, []);

  return (
    <div className="w-screen h-screen dark bg-zinc-950 text-zinc-50 overflow-hidden flex flex-col">
      <main className="flex-1 w-full h-full relative">
        <NeuralGraph />
      </main>
    </div>
  );
}

export default App;
