import logging

import pytest
from dependency_injector import providers
from fastapi.testclient import TestClient

from src.container import AppContainer
from src.memo.repository import InMemoryMemoRepository
from webapp.main import create_app


@pytest.fixture
def container():
    c = AppContainer()
    c.config.db_path.from_value(":memory:")
    # 진짜 DB 대신 dict 저장소로 바꿔 끼운다. 서비스·라우터 코드는 그대로
    c.memo.repository.override(providers.Singleton(InMemoryMemoRepository))
    yield c
    c.memo.repository.reset_override()


@pytest.fixture
def client(container):
    app = create_app(container=container)
    # 테스트에서는 로그를 사람이 읽기 쉬운 한 줄로 (형식은 바깥이 정한다)
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    logging.getLogger("memo_api").handlers[:] = [h]
    return TestClient(app)
