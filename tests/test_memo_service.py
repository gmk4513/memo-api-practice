"""서비스만 따로 — 컨테이너도 HTTP 도 없이, 가짜 저장소를 손으로 넣어서."""
import pytest

from src.common.exceptions import InvalidInput, NotFound, PermissionDenied
from src.memo.repository import InMemoryMemoRepository
from src.memo.service import MemoService


@pytest.fixture
def service():
    return MemoService(repository=InMemoryMemoRepository())


def test_create_and_list(service):
    service.create_memo("kim", "장보기", "우유")
    assert [m.title for m in service.list_memos("kim")] == ["장보기"]


def test_empty_title_is_rejected(service):
    with pytest.raises(InvalidInput):
        service.create_memo("kim", "   ")


def test_other_user_cannot_read(service):
    memo = service.create_memo("kim", "비밀")
    with pytest.raises(PermissionDenied):
        service.get_memo("lee", memo.id)


def test_rename_keeps_rule(service):
    memo = service.create_memo("kim", "초안")
    with pytest.raises(InvalidInput):
        service.rename_memo("kim", memo.id, "가" * 51)


def test_missing_memo(service):
    with pytest.raises(NotFound):
        service.get_memo("kim", 999)
