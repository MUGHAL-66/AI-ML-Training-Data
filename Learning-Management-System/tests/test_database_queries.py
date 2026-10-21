"""Query tests run without MySQL by replacing the centralized cursor context."""
from contextlib import contextmanager
import db

class FakeCursor:
    def __init__(self): self.sql=None; self.params=None
    def execute(self,sql,params): self.sql=sql;self.params=params
    def fetchall(self): return [{"id":1}]
    def fetchone(self): return {"n":1}
    def close(self): pass
    @property
    def lastrowid(self): return 7

def test_query_binds_values(monkeypatch):
    fake=FakeCursor()
    @contextmanager
    def fake_context(**kwargs): yield fake
    monkeypatch.setattr(db,"cursor",fake_context)
    assert db.query("SELECT * FROM students WHERE email=%s",("a@b.edu",)) == [{"id":1}]
    assert fake.params == ("a@b.edu",)
    assert "%s" in fake.sql

def test_execute_returns_insert_id(monkeypatch):
    fake=FakeCursor()
    @contextmanager
    def fake_context(**kwargs): yield fake
    monkeypatch.setattr(db,"cursor",fake_context)
    assert db.execute("INSERT INTO students(full_name) VALUES(%s)",("A",)) == 7

def test_transaction_commits_and_rolls_back(monkeypatch):
    class FakeConnection:
        committed=False; rolled_back=False
        def cursor(self,**kwargs): return FakeCursor()
        def commit(self): self.committed=True
        def rollback(self): self.rolled_back=True
        def is_connected(self): return True
        def close(self): pass
    conn=FakeConnection();monkeypatch.setattr(db,"connect",lambda:conn)
    with db.cursor(commit=True): pass
    assert conn.committed
    conn.committed=False
    try:
        with db.cursor(commit=True): raise ValueError("fail")
    except ValueError: pass
    assert conn.rolled_back
