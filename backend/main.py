import urllib.request
import urllib.parse
import urllib.error
import json
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not set.")
        return

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
    url = 'https://api.groq.com/openai/v1/chat/completions'
    prompt = f"Você é um extrator de grafos. Leia o texto e extraia nós e conexões. REGRAS: 1. Retorne APENAS um JSON válido. 2. A chave 'nodes' é uma lista de objetos com 'id' (snake_case) e 'label' (Português, max 3 palavras). 3. A chave 'links' é uma lista com 'source' (id), 'target' (id) e 'label' (Português). EXEMPLO ESPERADO: {{\"nodes\": [{{\"id\": \"tech_lead\", \"label\": \"Líder Técnico\"}}, {{\"id\": \"devops\", \"label\": \"Operações\"}}], \"links\": [{{\"source\": \"tech_lead\", \"target\": \"devops\", \"label\": \"delega para\"}}]}} TEXTO: {agents_content}"

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'Mozilla/5.0 (compatible; neural-rag/1.0)'
    }

    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)

    try:
        print("Sending request to OpenRouter...")
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            # Extract response text from OpenRouter format
            response_text = result['choices'][0]['message']['content']
            
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
                
    except urllib.error.HTTPError as e:
        print(f"Request failed with status {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    main()
