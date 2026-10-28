"""메모 저장소 — memo 테이블을 만지는 곳은 이 파일 하나뿐이다 (데이터 주권).

이름 규칙
  get_xxx            반드시 돌려준다. 없으면 NotFound
  find_xxx           없을 수 있다. Optional 또는 list
  <동작>_by_<조건>   by 뒤가 WHERE 절
"""
import sqlite3
from abc import ABC, abstractmethod

from src.common.exceptions import NotFound
from src.memo.domains import Memo
from src.memo.entities import MemoRow


class MemoRepository(ABC):
    @abstractmethod
    def find_memo(self, memo_id: int) -> Memo | None: ...

    @abstractmethod
    def find_memos_by_owner(self, owner: str) -> list[Memo]: ...

    @abstractmethod
    def create(self, memo: Memo) -> Memo: ...

    @abstractmethod
    def update(self, memo: Memo) -> Memo: ...

    @abstractmethod
    def delete(self, memo_id: int) -> None: ...

    def get_memo(self, memo_id: int) -> Memo:
        memo = self.find_memo(memo_id)
        if memo is None:
            raise NotFound(f"메모 {memo_id} 가 없습니다")
        return memo


class SqliteMemoRepository(MemoRepository):
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS memo ("
            " id INTEGER PRIMARY KEY AUTOINCREMENT, owner TEXT NOT NULL,"
            " title TEXT NOT NULL, body TEXT NOT NULL, created_at TEXT NOT NULL)"
        )

    def find_memo(self, memo_id: int) -> Memo | None:
        row = self.conn.execute(
            "SELECT id, owner, title, body, created_at FROM memo WHERE id = ?", (memo_id,)
        ).fetchone()
        return MemoRow(*row).to_domain() if row else None

    def find_memos_by_owner(self, owner: str) -> list[Memo]:
        rows = self.conn.execute(
            "SELECT id, owner, title, body, created_at FROM memo WHERE owner = ? ORDER BY id",
            (owner,),
        ).fetchall()
        return [MemoRow(*r).to_domain() for r in rows]

    def create(self, memo: Memo) -> Memo:
        row = MemoRow.from_domain(memo)
        cur = self.conn.execute(
            "INSERT INTO memo (owner, title, body, created_at) VALUES (?, ?, ?, ?)",
            (row.owner, row.title, row.body, row.created_at),
        )
        self.conn.commit()
        memo.id = cur.lastrowid
        return memo

    def update(self, memo: Memo) -> Memo:
        row = MemoRow.from_domain(memo)
        self.conn.execute("UPDATE memo SET title = ?, body = ? WHERE id = ?", (row.title, row.body, row.id))
        self.conn.commit()
        return memo

    def delete(self, memo_id: int) -> None:
        self.conn.execute("DELETE FROM memo WHERE id = ?", (memo_id,))
        self.conn.commit()


class InMemoryMemoRepository(MemoRepository):
    """DB 없이 dict 에 담는 저장소. 테스트와 빠른 실험용."""

    def __init__(self) -> None:
        self.rows: dict[int, Memo] = {}
        self.next_id = 1

    def find_memo(self, memo_id: int) -> Memo | None:
        return self.rows.get(memo_id)

    def find_memos_by_owner(self, owner: str) -> list[Memo]:
        return [m for m in self.rows.values() if m.owner == owner]

    def create(self, memo: Memo) -> Memo:
        memo.id, self.next_id = self.next_id, self.next_id + 1
        self.rows[memo.id] = memo
        return memo

    def update(self, memo: Memo) -> Memo:
        self.rows[memo.id] = memo
        return memo

    def delete(self, memo_id: int) -> None:
        self.rows.pop(memo_id, None)
