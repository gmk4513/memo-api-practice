"""같은 MemoService 에 저장소만 바꿔 끼우기 (개방-폐쇄)."""
import sqlite3
from src.memo.repository import InMemoryMemoRepository, SqliteMemoRepository
from src.memo.service import MemoService

for repo in [SqliteMemoRepository(sqlite3.connect(":memory:")), InMemoryMemoRepository()]:
    service = MemoService(repository=repo)          # 서비스 코드는 한 글자도 안 바뀐다
    memo = service.create_memo("kim", "장보기")
    print(type(repo).__name__, "->", service.get_memo("kim", memo.id).title, service.count_memos("kim"))
