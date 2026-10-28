"""FastAPI Depends(요청마다) vs 컨테이너 Singleton(앱에 한 번) — 몇 번 만들어지나 세어 보기."""
from dependency_injector import containers, providers
from fastapi import Depends, FastAPI, Request
from fastapi.testclient import TestClient


class HeavyClient:
    """연결·모델 로딩처럼 만들기 비싼 것이라고 치자."""
    made = 0

    def __init__(self) -> None:
        HeavyClient.made += 1
        print(f"  HeavyClient 생성 #{HeavyClient.made}")


class Container(containers.DeclarativeContainer):
    heavy = providers.Singleton(HeavyClient)


def per_request() -> HeavyClient:   # FastAPI 의존성: 요청이 올 때마다 불린다
    return HeavyClient()


app = FastAPI()
app.state.container = Container()   # 앱이 켜질 때 한 번


@app.get("/a")
def a(heavy: HeavyClient = Depends(per_request)):
    return {"id": id(heavy)}


@app.get("/b")
def b(request: Request):
    heavy = request.app.state.container.heavy()
    return {"id": id(heavy)}


client = TestClient(app)
print("[Depends] 요청 3번")
ids = {client.get("/a").json()["id"] for _ in range(3)}
print("  서로 다른 객체 수:", len(ids))
HeavyClient.made = 0
print("[컨테이너 Singleton] 요청 3번")
ids = {client.get("/b").json()["id"] for _ in range(3)}
print("  서로 다른 객체 수:", len(ids))
