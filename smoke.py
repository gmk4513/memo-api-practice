"""고칠 때마다 돌리는 확인 — 바깥에서 보이는 동작(API)이 그대로인지.
구조를 바꾸는 중이라 앱을 꺼내는 곳이 단계마다 다르다."""
import os

from fastapi.testclient import TestClient

if os.path.exists("memo.db"):
    os.remove("memo.db")
try:
    from webapp.main import create_app
    app = create_app(db_path=":memory:")
except ImportError:
    from app import app

c = TestClient(app)
K, L = {"x-user": "kim"}, {"x-user": "lee"}
checks = [
    ("만들기 201", c.post("/memos", json={"title": "장보기"}, headers=K).status_code == 201),
    ("내 것 읽기 200", c.get("/memos/1", headers=K).status_code == 200),
    ("남의 것 403", c.get("/memos/1", headers=L).status_code == 403),
    ("없는 것 404", c.get("/memos/9", headers=K).status_code == 404),
    ("빈 제목 400", c.post("/memos", json={"title": " "}, headers=K).status_code == 400),
    ("이름 바꾸기", c.patch("/memos/1", json={"title": "마트"}, headers=K).json()["title"] == "마트"),
    ("내 메모 수", c.get("/me", headers=K).json()["memo_count"] == 1),
]
for name, ok in checks:
    print(("ok  " if ok else "FAIL"), name)
print("smoke:", "통과" if all(ok for _, ok in checks) else "실패")
