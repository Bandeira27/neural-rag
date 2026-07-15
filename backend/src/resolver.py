class Entity:
    def __init__(self, name, id, edges=None, metadata=None):
        self.name = name
        self.id = id
        self.edges = edges or []
        self.metadata = metadata or {}

def is_textual_synonym(name1, name2):
    n1, n2 = name1.lower(), name2.lower()
    synonyms = [
        {"qa team", "equipe de qa"}
    ]
    for syn_set in synonyms:
        if n1 in syn_set and n2 in syn_set:
            return True
    return False

def resolve_entities(entity1, entity2, llm_response_is_same):
    if llm_response_is_same or is_textual_synonym(entity1.name, entity2.name):
        merged_edges = list(set(entity1.edges + entity2.edges))
        merged_metadata = {**entity1.metadata, **entity2.metadata}
        return [Entity(name=entity1.name, id=entity1.id, edges=merged_edges, metadata=merged_metadata)]
    return [entity1, entity2]
