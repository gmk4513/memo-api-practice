"""1단계: 라우트에서 SQL 이 빠졌다. 규칙·권한 확인은 아직 여기 있다."""
import json
import sqlite3

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from src.memo.repository import SqliteMemoRepository

app = FastAPI()
repo = SqliteMemoRepository(sqlite3.connect("memo.db", check_same_thread=False))


class MemoIn(BaseModel):
    title: str
    body: str = ""


def _public(m: dict) -> dict:
    return {k: m[k] for k in ("id", "title", "body", "created_at")}


def _mine(memo_id: int, user: str) -> dict:
    m = repo.find_memo(memo_id)
    if m is None:
        raise HTTPException(404, f"메모 {memo_id} 가 없습니다")
    if m["owner"] != user:
        raise HTTPException(403, "내 메모가 아닙니다")
    return m


def _check_title(title: str) -> None:
    if not title.strip():
        raise HTTPException(400, "제목이 비었습니다")
    if len(title) > 50:
        raise HTTPException(400, "제목은 50자까지입니다")


@app.post("/memos", status_code=201)
def create_memo(m: MemoIn, x_user: str = Header()):
    _check_title(m.title)
    memo = repo.create(x_user, m.title, m.body)
    print(json.dumps({"level": "INFO", "msg": "메모를 만들었다", "memo_id": memo["id"]}, ensure_ascii=False))
    return _public(memo)


@app.get("/memos")
def list_memos(x_user: str = Header()):
    return [_public(m) for m in repo.find_memos_by_owner(x_user)]


@app.get("/memos/{memo_id}")
def get_memo(memo_id: int, x_user: str = Header()):
    return _public(_mine(memo_id, x_user))


@app.patch("/memos/{memo_id}")
def rename_memo(memo_id: int, m: MemoIn, x_user: str = Header()):
    _mine(memo_id, x_user)
    _check_title(m.title)
    repo.update_title(memo_id, m.title)
    return _public(repo.find_memo(memo_id))


@app.delete("/memos/{memo_id}", status_code=204)
def delete_memo(memo_id: int, x_user: str = Header()):
    _mine(memo_id, x_user)
    repo.delete(memo_id)


@app.get("/me")
def me(x_user: str = Header()):
    return {"user": x_user, "memo_count": len(repo.find_memos_by_owner(x_user))}
