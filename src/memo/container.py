"""memo 모듈 안에서 누가 누구를 쓰는지 — 이 파일이 지도다."""
import sqlite3

from dependency_injector import containers, providers

from src.memo.repository import SqliteMemoRepository
from src.memo.service import MemoService


class MemoContainer(containers.DeclarativeContainer):
    db = providers.Dependency(instance_of=sqlite3.Connection)  # 바깥(AppContainer)이 넣어 준다

    repository = providers.Singleton(SqliteMemoRepository, conn=db)
    service = providers.Singleton(MemoService, repository=repository)
