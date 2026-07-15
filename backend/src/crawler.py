import os
import argparse
import sys

def get_target_path(env_var="REPO_PATH", cli_args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default=None)
    
    args, _ = parser.parse_known_args(cli_args)
    
    if args.path:
        return os.path.abspath(args.path)
        
    env_path = os.environ.get(env_var)
    if env_path:
        return os.path.abspath(env_path)
        
    raise ValueError("Path must be provided via CLI argument --path or environment variable.")

class Crawler:
    def __init__(self, cli_args=None):
        self.target_path = get_target_path(cli_args=cli_args)
        self.base_scope = os.path.abspath('/home/bandeira')
        if os.path.commonpath([self.base_scope, self.target_path]) != self.base_scope:
             raise ValueError("Directory Traversal Attempted: Target path outside allowed scope.")
    
    def run(self):
        valid_exts = ('.md', '.tsx', '.ts', 'package.json')
        for root, dirs, files in os.walk(self.target_path):
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'venv', '__pycache__']]
            for file in files:
                if not file.endswith(valid_exts):
                    continue
                file_path = os.path.abspath(os.path.join(root, file))
                
                # Para evitar estourar tokens da Groq, fazemos chunking simples para código fonte
                if file.endswith(('.tsx', '.ts')):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    # Chunk de 100 linhas (ajuste se necessário)
                    chunk_size = 100
                    for i in range(0, len(lines), chunk_size):
                        chunk = "".join(lines[i:i + chunk_size])
                        yield file_path, chunk
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        yield file_path, f.read()
