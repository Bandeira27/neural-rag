class StorageException(Exception):
    pass

class StorageMock:
    def __init__(self):
        self.chroma_data = []
        self.sqlite_data = []
        
    def save(self, entity, fail_chroma=False, fail_sqlite=False):
        if fail_chroma:
            raise StorageException("ChromaDB Timeout")
            
        temp_chroma = [entity]
        
        if fail_sqlite:
            # Atomic failure: nothing is saved in self.chroma_data because sqlite failed
            raise StorageException("SQLite Lock")
            
        self.chroma_data.extend(temp_chroma)
        self.sqlite_data.append(entity)
        return True
