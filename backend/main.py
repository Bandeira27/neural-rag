import json
import re
from pydantic import BaseModel
from typing import List, Optional

class Node(BaseModel):
    id: str
    label: str

class Edge(BaseModel):
    source: str
    target: str

class GraphData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

def parse_llm_json(text: str) -> GraphData:
    match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        # Tenta achar o primeiro objeto json puro
        match = re.search(r'(\{.*?\})', text, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            json_str = text
            
    data = json.loads(json_str)
    return GraphData(**data)
