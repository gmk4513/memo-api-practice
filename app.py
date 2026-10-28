"""2단계: 규칙은 도메인(Memo)으로, 흐름은 서비스로. 라우트는 받아서 넘기기만 한다."""
import sqlite3

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from src.common.exceptions import InvalidInput, NotFound, PermissionDenied
from src.memo.repository import SqliteMemoRepository
from src.memo.service import MemoService

app = FastAPI()
service = MemoService(SqliteMemoRepository(sqlite3.connect("memo.db", check_same_thread=False)))
STATUS = {NotFound: 404, PermissionDenied: 403, InvalidInput: 400}


class MemoIn(BaseModel):
    title: str
    body: str = ""


def _public(m) -> dict:
    return {"id": m.id, "title": m.title, "body": m.body, "created_at": m.created_at}


def _call(fn, *args):
    try:
        return fn(*args)
    except tuple(STATUS) as e:
        raise HTTPException(STATUS[type(e)], str(e))


@app.post("/memos", status_code=201)
def create_memo(m: MemoIn, x_user: str = Header()):
    return _public(_call(service.create_memo, x_user, m.title, m.body))


@app.get("/memos")
def list_memos(x_user: str = Header()):
    return [_public(m) for m in service.list_memos(x_user)]


@app.get("/memos/{memo_id}")
def get_memo(memo_id: int, x_user: str = Header()):
    return _public(_call(service.get_memo, x_user, memo_id))


@app.patch("/memos/{memo_id}")
def rename_memo(memo_id: int, m: MemoIn, x_user: str = Header()):
    return _public(_call(service.rename_memo, x_user, memo_id, m.title))


@app.delete("/memos/{memo_id}", status_code=204)
def delete_memo(memo_id: int, x_user: str = Header()):
    _call(service.delete_memo, x_user, memo_id)


@app.get("/me")
def me(x_user: str = Header()):
    return {"user": x_user, "memo_count": service.count_memos(x_user)}
