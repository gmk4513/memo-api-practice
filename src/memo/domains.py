"""메모 도메인 — 메모가 지켜야 할 규칙은 여기에만 있다.
DB 도, HTTP 도 모른다. 순수한 파이썬 객체."""
from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.common.exceptions import InvalidInput, PermissionDenied

TITLE_MAX = 50


@dataclass
class Memo:
    owner: str
    title: str
    body: str = ""
    id: int | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        self.validate_title(self.title)

    @staticmethod
    def validate_title(title: str) -> None:
        if not title.strip():
            raise InvalidInput("제목이 비었습니다")
        if len(title) > TITLE_MAX:
            raise InvalidInput(f"제목은 {TITLE_MAX}자까지입니다")

    def rename(self, title: str) -> None:
        self.validate_title(title)
        self.title = title

    def ensure_owner(self, user: str) -> None:
        if self.owner != user:
            raise PermissionDenied("내 메모가 아닙니다")
