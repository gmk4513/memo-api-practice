from dependency_injector import containers, providers

from src.memo.service import MemoService
from src.user.service import ProfileService


class UserContainer(containers.DeclarativeContainer):
    memo_service = providers.Dependency(instance_of=MemoService)

    profile_service = providers.Singleton(ProfileService, memo_service=memo_service)
