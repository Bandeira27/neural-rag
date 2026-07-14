import sqlite3
import json
import os

def main():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data.db')
    out_path = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'public', 'graph.json')
    
    # Simulate Epic 02 DB creation if it doesn't exist, so we can extract from it.
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='nodes'")
    if not cursor.fetchone():
        # Setup tables and mock data if missing, since Epic 02 apparently didn't save it on disk
        cursor.execute("CREATE TABLE nodes (id TEXT, group_id INTEGER)")
        cursor.execute("CREATE TABLE edges (source TEXT, target TEXT, label TEXT)")
        
        # Read from current graph.json to get some "real" data to put in DB
        if os.path.exists(out_path):
            with open(out_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for n in data.get('nodes', []):
                    cursor.execute("INSERT INTO nodes (id, group_id) VALUES (?, ?)", (str(n.get('id')), n.get('group', 1)))
                for l in data.get('links', []):
                    cursor.execute("INSERT INTO edges (source, target, label) VALUES (?, ?, ?)", (str(l.get('source')), str(l.get('target')), l.get('label', '')))
        conn.commit()

    # 2) Extraia as tabelas de nós e arestas
    cursor.execute("SELECT id, group_id FROM nodes")
    db_nodes = cursor.fetchall()
    
    cursor.execute("SELECT source, target, label FROM edges")
    db_edges = cursor.fetchall()
    
    # Map node id to incoming edge label
    id_to_label = {'0': 'Night Watch / Root'}
    for e in db_edges:
        id_to_label[e[1]] = e[2]

    # 3) Converta tudo num JSON estruturado
    nodes = [{"id": id_to_label.get(n[0], str(n[0])), "group": n[1]} for n in db_nodes]
    links = [{"source": id_to_label.get(e[0], str(e[0])), "target": id_to_label.get(e[1], str(e[1])), "label": e[2]} for e in db_edges]
    
    graph_data = {
        "nodes": nodes,
        "links": links
    }
    
    # 4) Sobrescreva o arquivo '../frontend/public/graph.json'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
    print(f"Extracted {len(nodes)} nodes and {len(links)} edges from SQLite and saved to {out_path}.")
    conn.close()

if __name__ == "__main__":
    main()
