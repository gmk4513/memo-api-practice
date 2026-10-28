"""Factory 와 Singleton, 그리고 override 를 직접 눌러 보기."""
from dependency_injector import containers, providers

from src.container import AppContainer
from src.memo.repository import InMemoryMemoRepository


class Box(containers.DeclarativeContainer):
    factory = providers.Factory(list)      # 부를 때마다 새로
    singleton = providers.Singleton(list)  # 처음 한 번만 만들고 계속 같은 것

box = Box()
print("Factory   같은 객체?", box.factory() is box.factory())
print("Singleton 같은 객체?", box.singleton() is box.singleton())

app = AppContainer()
app.config.db_path.from_value(":memory:")
print("기본 저장소:", type(app.memo.service().repository).__name__)

app2 = AppContainer()
app2.config.db_path.from_value(":memory:")
with app2.memo.repository.override(providers.Singleton(InMemoryMemoRepository)):
    print("override 중:", type(app2.memo.service().repository).__name__)
