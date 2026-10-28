"""HTTP 까지 — TestClient 로 진짜 요청을 보낸다. 저장소는 conftest 가 dict 로 바꿔 두었다."""
KIM = {"x-user": "kim"}
LEE = {"x-user": "lee"}


def test_create_then_get(client):
    r = client.post("/memos", json={"title": "장보기", "body": "우유"}, headers=KIM)
    assert r.status_code == 201
    memo_id = r.json()["id"]
    r = client.get(f"/memos/{memo_id}", headers=KIM)
    assert r.json()["title"] == "장보기"
    assert "owner" not in r.json()


def test_status_codes(client):
    memo_id = client.post("/memos", json={"title": "비밀"}, headers=KIM).json()["id"]
    assert client.get(f"/memos/{memo_id}", headers=LEE).status_code == 403
    assert client.get("/memos/999", headers=KIM).status_code == 404
    assert client.post("/memos", json={"title": " "}, headers=KIM).status_code == 400


def test_profile_counts_through_memo_service(client):
    client.post("/memos", json={"title": "a"}, headers=KIM)
    client.post("/memos", json={"title": "b"}, headers=KIM)
    assert client.get("/me", headers=KIM).json() == {"user": "kim", "memo_count": 2}
