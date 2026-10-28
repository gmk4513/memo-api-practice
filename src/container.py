"""앱 전체 컨테이너 — 모듈 컨테이너를 엮는다. 의존 관계를 한눈에 보는 곳."""
import sqlite3

from dependency_injector import containers, providers

from src.memo.container import MemoContainer
from src.user.container import UserContainer


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(sqlite3.connect, config.db_path, check_same_thread=False)

    memo = providers.Container(MemoContainer, db=db)
    user = providers.Container(UserContainer, memo_service=memo.service)
