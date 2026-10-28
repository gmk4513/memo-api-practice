"""2단계 서비스 — 로그 '형식'(JSON)이 아직 비즈니스 코드 안에 있다. 4단계에서 뺀다."""
import json

from src.memo.domains import Memo
from src.memo.repository import MemoRepository


class MemoService:
    def __init__(self, repository: MemoRepository) -> None:
        self.repository = repository

    def create_memo(self, user: str, title: str, body: str = "") -> Memo:
        memo = self.repository.create(Memo(owner=user, title=title, body=body))
        print(json.dumps({"level": "INFO", "msg": "메모를 만들었다", "memo_id": memo.id}, ensure_ascii=False))
        return memo

    def get_memo(self, user: str, memo_id: int) -> Memo:
        memo = self.repository.get_memo(memo_id)
        memo.ensure_owner(user)
        return memo

    def list_memos(self, user: str) -> list[Memo]:
        return self.repository.find_memos_by_owner(user)

    def rename_memo(self, user: str, memo_id: int, title: str) -> Memo:
        memo = self.get_memo(user, memo_id)
        memo.rename(title)
        return self.repository.update(memo)

    def delete_memo(self, user: str, memo_id: int) -> None:
        self.get_memo(user, memo_id)
        self.repository.delete(memo_id)

    def count_memos(self, user: str) -> int:
        return len(self.repository.find_memos_by_owner(user))
