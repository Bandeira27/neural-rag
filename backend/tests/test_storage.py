import pytest
from src.storage import StorageMock, StorageException

def test_storage_success():
    storage = StorageMock()
    storage.save({"id": "1", "data": "vec"})
    
    assert len(storage.chroma_data) == 1
    assert len(storage.sqlite_data) == 1

def test_storage_atomic_failure_chroma():
    storage = StorageMock()
    with pytest.raises(StorageException):
        storage.save({"id": "1", "data": "vec"}, fail_chroma=True)
    
    assert len(storage.chroma_data) == 0
    assert len(storage.sqlite_data) == 0

def test_storage_atomic_failure_sqlite():
    storage = StorageMock()
    with pytest.raises(StorageException):
        storage.save({"id": "1", "data": "vec"}, fail_sqlite=True)
        
    assert len(storage.chroma_data) == 0
    assert len(storage.sqlite_data) == 0
