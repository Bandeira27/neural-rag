import sqlite3
import chromadb
from contextlib import contextmanager
import uuid

class StorageException(Exception):
    pass

class Storage:
    def __init__(self, sqlite_path="data.db", chroma_path="./chroma"):
        self.sqlite_path = sqlite_path
        self.chroma_path = chroma_path
        
    @contextmanager
    def get_sqlite_conn(self):
        conn = sqlite3.connect(self.sqlite_path)
        try:
            yield conn
        finally:
            conn.close()
            
    def get_chroma_client(self):
        return chromadb.PersistentClient(path=self.chroma_path)

    def save(self, entity, document_text="", description=""):
        chroma_client = self.get_chroma_client()
        collection = chroma_client.get_or_create_collection(name="documents")
        
        entity_id = str(uuid.uuid4())
        
        with self.get_sqlite_conn() as conn:
            cursor = conn.cursor()
            try:
                # SQLite operation
                cursor.execute("CREATE TABLE IF NOT EXISTS entities (id TEXT PRIMARY KEY, data TEXT, description TEXT)")
                
                # Update schema just in case
                cursor.execute("PRAGMA table_info(entities)")
                columns = [info[1] for info in cursor.fetchall()]
                if 'description' not in columns:
                    cursor.execute("ALTER TABLE entities ADD COLUMN description TEXT")
                    
                cursor.execute("INSERT INTO entities (id, data, description) VALUES (?, ?, ?)", (entity_id, str(entity), description))
                
                # ChromaDB operation
                collection.add(
                    documents=[document_text or str(entity)],
                    ids=[entity_id]
                )
                
                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                try:
                    collection.delete(ids=[entity_id])
                except:
                    pass
                raise StorageException(f"Storage failed: {e}")
