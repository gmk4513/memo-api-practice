"""user 모듈 — 메모 수가 필요하지만 memo 테이블을 직접 읽지 않고 MemoService 에 묻는다."""
from src.memo.service import MemoService


class ProfileService:
    def __init__(self, memo_service: MemoService) -> None:
        self.memo_service = memo_service

    def profile(self, user: str) -> dict:
        return {"user": user, "memo_count": self.memo_service.count_memos(user)}
