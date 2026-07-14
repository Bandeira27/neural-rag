from src.resolver import Entity, resolve_entities

def test_resolve_entities_merge_synonyms():
    e1 = Entity(name="Autenticação", id="1", edges=["a"], metadata={"type": "auth"})
    e2 = Entity(name="Login", id="2", edges=["b"], metadata={"author": "dev"})
    
    result = resolve_entities(e1, e2, llm_response_is_same=True)
    
    assert len(result) == 1
    merged = result[0]
    assert set(merged.edges) == {"a", "b"}
    assert merged.metadata == {"type": "auth", "author": "dev"}

def test_resolve_entities_distinct():
    e1 = Entity(name="User", id="1", edges=[])
    e2 = Entity(name="Product", id="2", edges=[])
    
    result = resolve_entities(e1, e2, llm_response_is_same=False)
    
    assert len(result) == 2
    assert result[0].id == "1"
    assert result[1].id == "2"
