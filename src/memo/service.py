"""메모 서비스 — 유스케이스(사용자가 하려는 일) 하나가 메서드 하나.
저장소를 직접 만들지 않고 받는다(생성자 주입)."""
from src.common.logger import get_logger
from src.memo.domains import Memo
from src.memo.repository import MemoRepository

log = get_logger("memo")


class MemoService:
    def __init__(self, repository: MemoRepository) -> None:
        self.repository = repository

    def create_memo(self, user: str, title: str, body: str = "") -> Memo:
        memo = self.repository.create(Memo(owner=user, title=title, body=body))
        log.info("메모를 만들었다", extra={"memo_id": memo.id, "user": user})
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
        """다른 모듈이 메모 수를 알고 싶을 때 여는 문. 테이블을 직접 읽게 하지 않는다."""
        return len(self.repository.find_memos_by_owner(user))
