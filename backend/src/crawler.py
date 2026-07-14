import os
import argparse
import sys

def get_target_path(env_var="REPO_PATH", cli_args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default=None)
    
    # Allow passing custom arguments or use sys.argv
    args, _ = parser.parse_known_args(cli_args)
    
    if args.path:
        return args.path
        
    env_path = os.environ.get(env_var)
    if env_path:
        return env_path
        
    raise ValueError("Path must be provided via CLI argument --path or environment variable.")

class Crawler:
    def __init__(self, cli_args=None):
        self.target_path = get_target_path(cli_args=cli_args)
    
    def run(self):
        return f"Crawling {self.target_path}"
