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
        for root, dirs, files in os.walk(self.target_path):
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'venv']]
            for file in files:
                if not file.endswith('.md'):
                    continue
                file_path = os.path.abspath(os.path.join(root, file))
                yield file_path
