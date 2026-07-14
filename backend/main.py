import urllib.request
import urllib.parse
import json
import os

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    agents_path = os.path.join(base_dir, '../AGENTS.md')
    out_path = os.path.join(base_dir, '../frontend/public/graph.json')

    # Read AGENTS.md
    try:
        with open(agents_path, 'r', encoding='utf-8') as f:
            agents_content = f.read()
    except FileNotFoundError:
        print(f"Error: {agents_path} not found.")
        return

    # Prepare request
    url = 'http://127.0.0.1:11434/api/generate'
    prompt = f"Você é um extrator de grafos. Leia o texto e extraia nós e conexões. REGRAS: 1. Retorne APENAS um JSON válido. 2. A chave 'nodes' é uma lista de objetos com 'id' (snake_case) e 'label' (Português, max 3 palavras). 3. A chave 'links' é uma lista com 'source' (id), 'target' (id) e 'label' (Português). EXEMPLO ESPERADO: {{\"nodes\": [{{\"id\": \"tech_lead\", \"label\": \"Líder Técnico\"}}, {{\"id\": \"devops\", \"label\": \"Operações\"}}], \"links\": [{{\"source\": \"tech_lead\", \"target\": \"devops\", \"label\": \"delega para\"}}]}} TEXTO: {agents_content}"

    data = {
        "model": "phi3",
        "prompt": prompt,
        "format": "json",
        "stream": False
    }

    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})

    try:
        print("Sending request to Ollama...")
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            # Ollama response puts the actual text in 'response' key
            response_text = result.get('response', '')
            
            # Parse the response text as JSON
            try:
                graph_data = json.loads(response_text)
            except json.JSONDecodeError:
                print("Error: Could not parse response as JSON.")
                print("Raw response:", response_text)
                return
            
            # Validate
            if 'nodes' in graph_data and 'links' in graph_data:
                # Ensure output directory exists
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                
                with open(out_path, 'w', encoding='utf-8') as f:
                    json.dump(graph_data, f, indent=2)
                print("Successfully saved to graph.json")
            else:
                print("Error: Response JSON missing 'nodes' or 'links'.")
                print("Parsed JSON:", graph_data)
                
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    main()
