"""엔티티 — DB 테이블 한 줄을 그대로 옮긴 모양. 도메인과 오가는 변환도 여기서만 한다."""
from dataclasses import dataclass
from datetime import datetime

from src.memo.domains import Memo


@dataclass(frozen=True)
class MemoRow:
    id: int
    owner: str
    title: str
    body: str
    created_at: str  # sqlite 에는 ISO 문자열로 들어간다

    @classmethod
    def from_domain(cls, memo: Memo) -> "MemoRow":
        return cls(memo.id or 0, memo.owner, memo.title, memo.body, memo.created_at.isoformat())

    def to_domain(self) -> Memo:
        return Memo(owner=self.owner, title=self.title, body=self.body,
                    id=self.id, created_at=datetime.fromisoformat(self.created_at))
