import os
import pytest
from src.crawler import get_target_path, Crawler

def test_crawler_with_env_var(monkeypatch):
    monkeypatch.setenv("REPO_PATH", "/caminho/para/repositorio")
    path = get_target_path(cli_args=[])
    assert path == "/caminho/para/repositorio"

def test_crawler_with_cli_arg(monkeypatch):
    monkeypatch.setenv("REPO_PATH", "/caminho/ignoravel")
    path = get_target_path(cli_args=["--path=/caminho/para/repositorio2"])
    assert path == "/caminho/para/repositorio2"

def test_crawler_fails_without_path(monkeypatch):
    monkeypatch.delenv("REPO_PATH", raising=False)
    with pytest.raises(ValueError, match="Path must be provided"):
        get_target_path(cli_args=[])
