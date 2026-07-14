import pytest
from main import parse_llm_json

def test_clean_json():
    clean_json = '{"nodes": [], "edges": []}'
    result = parse_llm_json(clean_json)
    assert result.nodes == []
    assert result.edges == []

def test_dirty_json():
    dirty_json = '''Aqui está o JSON:
```json
{"nodes": [{"id": "1", "label": "A"}], "edges": []}
```
Espero que ajude!'''
    result = parse_llm_json(dirty_json)
    assert len(result.nodes) == 1
    assert result.nodes[0].id == "1"
    assert result.edges == []
