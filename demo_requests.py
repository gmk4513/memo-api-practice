"""진짜 요청 몇 개 — 서비스 모드(JSON 로그) 그대로."""
from fastapi.testclient import TestClient
from webapp.main import create_app

client = TestClient(create_app(db_path=":memory:"))
r = client.post("/memos", json={"title": "장보기", "body": "우유, 계란"}, headers={"x-user": "kim"})
print(r.status_code, r.json())
print(client.get("/memos/1", headers={"x-user": "lee"}).status_code, client.get("/memos/1", headers={"x-user": "lee"}).json())
print(client.post("/memos", json={"title": "  "}, headers={"x-user": "kim"}).json())
print(client.get("/me", headers={"x-user": "kim"}).json())
