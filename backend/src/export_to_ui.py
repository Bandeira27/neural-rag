import sqlite3
import json
import os

def main():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data.db')
    out_path = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'public', 'graph.json')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='nodes'")
    if not cursor.fetchone():
        cursor.execute("CREATE TABLE nodes (id TEXT, label TEXT, group_id INTEGER)")
        cursor.execute("CREATE TABLE edges (source TEXT, target TEXT, label TEXT)")
    else:
        # Check if label column exists
        cursor.execute("PRAGMA table_info(nodes)")
        columns = [info[1] for info in cursor.fetchall()]
        if 'label' not in columns:
            cursor.execute("ALTER TABLE nodes ADD COLUMN label TEXT")
            conn.commit()
            
    # Extraia as tabelas de nós e arestas
    cursor.execute("SELECT id, label, group_id FROM nodes")
    db_nodes = cursor.fetchall()
    
    cursor.execute("SELECT source, target, label FROM edges")
    db_edges = cursor.fetchall()
    
    # Converta tudo num JSON estruturado
    nodes = [{"id": str(n[0]), "label": n[1] if n[1] else str(n[0]), "group": n[2]} for n in db_nodes]
    links = [{"source": str(e[0]), "target": str(e[1]), "label": e[2]} for e in db_edges]
    
    graph_data = {
        "nodes": nodes,
        "links": links
    }
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
    print(f"Extracted {len(nodes)} nodes and {len(links)} edges from SQLite and saved to {out_path}.")
    conn.close()

if __name__ == "__main__":
    main()
