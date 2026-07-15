import urllib.request
import urllib.parse
import urllib.error
import json
import os
import sys
import time
import sqlite3
import re
from dotenv import load_dotenv

# Ensure we can import from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.crawler import Crawler

def main():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not set.")
        return

    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(base_dir, '../frontend/public/graph.json')
    db_path = os.path.join(base_dir, 'data.db')

    # Setup DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS nodes (id TEXT, label TEXT, group_id INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS edges (source TEXT, target TEXT, label TEXT)")
    cursor.execute("DELETE FROM nodes")
    cursor.execute("DELETE FROM edges")
    conn.commit()

    # Crawler integration
    try:
        crawler = Crawler(cli_args=sys.argv[1:])
    except ValueError as e:
        # Fallback to just AGENTS.md if no --path is given and we want to keep old behavior
        crawler = None

    url = 'https://api.groq.com/openai/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'Mozilla/5.0 (compatible; neural-rag/1.0)'
    }

    files_to_process = []
    if crawler:
        for f in crawler.run():
            files_to_process.append(f)
    else:
        agents_path = os.path.join(base_dir, '../AGENTS.md')
        if os.path.exists(agents_path):
            files_to_process.append(agents_path)
        else:
            print(f"Error: {agents_path} not found.")
            return

    print(f"Found {len(files_to_process)} files to process.")

    all_nodes = []
    all_links = []

    for idx, file_path in enumerate(files_to_process):
        print(f"Processing ({idx+1}/{len(files_to_process)}): {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # skip empty
        if not content.strip():
            continue

        prompt = f"Você é um extrator de grafos. Leia o texto e extraia nós e conexões. REGRAS: 1. Retorne APENAS um JSON válido. 2. A chave 'nodes' é uma lista de objetos com 'id' (snake_case) e 'label' (Português, max 3 palavras). 3. A chave 'links' é uma lista com 'source' (id), 'target' (id) e 'label' (Português). EXEMPLO ESPERADO: {{\"nodes\": [{{\"id\": \"tech_lead\", \"label\": \"Líder Técnico\"}}, {{\"id\": \"devops\", \"label\": \"Operações\"}}], \"links\": [{{\"source\": \"tech_lead\", \"target\": \"devops\", \"label\": \"delega para\"}}]}} TEXTO: {content}"
        
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                response_text = result['choices'][0]['message']['content']
                
                if response_text.startswith("```json"):
                    response_text = response_text.split("```json")[1].split("```")[0].strip()
                elif response_text.startswith("```"):
                    response_text = response_text.split("```")[1].split("```")[0].strip()
                else:
                    match = re.search(r'```(?:json)?\n(.*?)\n```', response_text, re.DOTALL)
                    if match:
                        response_text = match.group(1).strip()
                
                try:
                    graph_data = json.loads(response_text)
                    if 'nodes' in graph_data and 'links' in graph_data:
                        for node in graph_data['nodes']:
                            cursor.execute("INSERT INTO nodes (id, label, group_id) VALUES (?, ?, ?)", (node['id'], node.get('label', ''), 1))
                            all_nodes.append(node)
                        for link in graph_data['links']:
                            cursor.execute("INSERT INTO edges (source, target, label) VALUES (?, ?, ?)", (link['source'], link['target'], link.get('label', '')))
                            all_links.append(link)
                        conn.commit()
                        print("  -> Success")
                        time.sleep(3)
                    else:
                        print("  -> Missing nodes or links in JSON")
                except json.JSONDecodeError:
                    print("  -> JSON Decode Error")
                    
        except urllib.error.HTTPError as e:
            print(f"  -> Request failed with status {e.code}: {e.read().decode('utf-8')}")
            # wait a bit on error too, in case of rate limit
            time.sleep(5)
        except Exception as e:
            print(f"  -> Request failed: {e}")
            time.sleep(5)

    conn.close()

    # Save aggregated JSON
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({"nodes": all_nodes, "links": all_links}, f, indent=2)
    print("Aggregation complete.")

if __name__ == "__main__":
    main()
