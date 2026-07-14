# Neural RAG (Local GraphRAG)

## Sobre o Projeto
O Neural RAG é um projeto de Local GraphRAG (Retrieval-Augmented Generation baseado em grafos). O sistema extrai entidades e relacionamentos de textos de forma local e gera uma visualização interativa em formato de grafo. O grande diferencial é rodar inteiramente no seu próprio ambiente, garantindo privacidade e processamento offline.

## Tech Stack
- **Backend:** Python
- **LLM Local:** Ollama rodando o modelo **Phi-3**
- **Frontend:** React (Vite)
- **Estilização:** Tailwind CSS v3
- **Visualização de Grafo:** react-force-graph

---

## Instruções Passo a Passo

### Pré-requisitos
- [Python 3.10+](https://www.python.org/)
- [Node.js + npm](https://nodejs.org/)
- [Ollama](https://ollama.com/) instalado com o modelo Phi-3 baixado. Para baixar o modelo, execute:
  ```bash
  ollama run phi3
  ```

### 1. Rodando o Backend (Geração do JSON do Grafo)
O backend processa as informações localmente via Ollama (Phi-3) para gerar a estrutura de entidades e links.

1. Abra um terminal na pasta do projeto (`/neural-rag`).
2. Crie e ative um ambiente virtual Python (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Instale as dependências Python:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o script principal de extração para gerar o arquivo JSON contendo o grafo:
   ```bash
   python main.py
   ```
   *(Atenção: o arquivo JSON gerado é utilizado pelo frontend para renderizar o grafo visual. Caso seu script backend tenha outro nome, substitua `main.py` pelo nome correto).*

### 2. Rodando o Frontend (Visualização Interativa)
O frontend consome o JSON gerado pelo backend e exibe a interface com o grafo de conhecimento.

1. Ainda no terminal (ou em uma nova aba, na pasta do frontend caso esteja separada), instale as dependências do Node.js:
   ```bash
   npm install
   ```
2. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```
3. Acesse a aplicação no seu navegador acessando a URL exibida no terminal (geralmente `http://localhost:5173`).
