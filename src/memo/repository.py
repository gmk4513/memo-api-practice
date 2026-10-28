"""1단계: SQL 을 한 곳으로 모은다. 아직 dict 를 돌려준다."""
import sqlite3
from datetime import datetime, timezone

COLS = "id, owner, title, body, created_at"


def _row(r):
    return {"id": r[0], "owner": r[1], "title": r[2], "body": r[3], "created_at": r[4]}


class SqliteMemoRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS memo (id INTEGER PRIMARY KEY AUTOINCREMENT, owner TEXT NOT NULL,"
            " title TEXT NOT NULL, body TEXT NOT NULL, created_at TEXT NOT NULL)")

    def find_memo(self, memo_id: int) -> dict | None:
        r = self.conn.execute(f"SELECT {COLS} FROM memo WHERE id = ?", (memo_id,)).fetchone()
        return _row(r) if r else None

    def find_memos_by_owner(self, owner: str) -> list[dict]:
        rows = self.conn.execute(f"SELECT {COLS} FROM memo WHERE owner = ? ORDER BY id", (owner,)).fetchall()
        return [_row(r) for r in rows]

    def create(self, owner: str, title: str, body: str) -> dict:
        now = datetime.now(timezone.utc).isoformat()
        cur = self.conn.execute("INSERT INTO memo (owner, title, body, created_at) VALUES (?, ?, ?, ?)",
                                (owner, title, body, now))
        self.conn.commit()
        return self.find_memo(cur.lastrowid)

    def update_title(self, memo_id: int, title: str) -> None:
        self.conn.execute("UPDATE memo SET title = ? WHERE id = ?", (title, memo_id))
        self.conn.commit()

    def delete(self, memo_id: int) -> None:
        self.conn.execute("DELETE FROM memo WHERE id = ?", (memo_id,))
        self.conn.commit()
