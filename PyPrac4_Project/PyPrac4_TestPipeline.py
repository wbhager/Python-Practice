import pytest
import sqlite3
from PyPrac4_ProjectPipeline import CSVLoader

@pytest.fixture
def db_path(tmp_path):
    return tmp_path / "test.db"

def test_load_csv(db_path, tmp_path):
    csv_file = tmp_path / "users.csv"
    csv_file.write_text("id,name,Gender\n1,Alice,F\n2,Bob,M")

    loader = CSVLoader(str(db_path))
    loader.load(str(csv_file), "users")

    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT * FROM users").fetchall()
    assert len(rows) == 2
