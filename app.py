"""한 파일짜리 메모 API — 일단 돌아가게만 만든 버전."""
import json
import sqlite3
from datetime import datetime, timezone

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()
db = sqlite3.connect("memo.db", check_same_thread=False)  # 전역 연결
db.execute("CREATE TABLE IF NOT EXISTS memo (id INTEGER PRIMARY KEY AUTOINCREMENT, owner TEXT NOT NULL,"
           " title TEXT NOT NULL, body TEXT NOT NULL, created_at TEXT NOT NULL)")


class MemoIn(BaseModel):
    title: str
    body: str = ""


@app.post("/memos", status_code=201)
def create_memo(m: MemoIn, x_user: str = Header()):
    if not m.title.strip():
        raise HTTPException(400, "제목이 비었습니다")
    if len(m.title) > 50:
        raise HTTPException(400, "제목은 50자까지입니다")
    now = datetime.now(timezone.utc).isoformat()
    cur = db.execute("INSERT INTO memo (owner, title, body, created_at) VALUES (?, ?, ?, ?)",
                     (x_user, m.title, m.body, now))
    db.commit()
    print(json.dumps({"level": "INFO", "msg": "메모를 만들었다", "memo_id": cur.lastrowid}, ensure_ascii=False))
    return {"id": cur.lastrowid, "title": m.title, "body": m.body, "created_at": now}


@app.get("/memos")
def list_memos(x_user: str = Header()):
    rows = db.execute("SELECT id, title, body, created_at FROM memo WHERE owner = ? ORDER BY id", (x_user,)).fetchall()
    return [{"id": r[0], "title": r[1], "body": r[2], "created_at": r[3]} for r in rows]


@app.get("/memos/{memo_id}")
def get_memo(memo_id: int, x_user: str = Header()):
    row = db.execute("SELECT id, owner, title, body, created_at FROM memo WHERE id = ?", (memo_id,)).fetchone()
    if row is None:
        raise HTTPException(404, f"메모 {memo_id} 가 없습니다")
    if row[1] != x_user:
        raise HTTPException(403, "내 메모가 아닙니다")
    return {"id": row[0], "title": row[2], "body": row[3], "created_at": row[4]}


@app.patch("/memos/{memo_id}")
def rename_memo(memo_id: int, m: MemoIn, x_user: str = Header()):
    row = db.execute("SELECT owner FROM memo WHERE id = ?", (memo_id,)).fetchone()
    if row is None:
        raise HTTPException(404, f"메모 {memo_id} 가 없습니다")
    if row[0] != x_user:
        raise HTTPException(403, "내 메모가 아닙니다")
    if not m.title.strip():            # 같은 규칙을 또 쓴다
        raise HTTPException(400, "제목이 비었습니다")
    db.execute("UPDATE memo SET title = ? WHERE id = ?", (m.title, memo_id))
    db.commit()
    return get_memo(memo_id, x_user)


@app.delete("/memos/{memo_id}", status_code=204)
def delete_memo(memo_id: int, x_user: str = Header()):
    row = db.execute("SELECT owner FROM memo WHERE id = ?", (memo_id,)).fetchone()
    if row is None:
        raise HTTPException(404, f"메모 {memo_id} 가 없습니다")
    if row[0] != x_user:
        raise HTTPException(403, "내 메모가 아닙니다")
    db.execute("DELETE FROM memo WHERE id = ?", (memo_id,))
    db.commit()


@app.get("/me")
def me(x_user: str = Header()):
    count = db.execute("SELECT COUNT(*) FROM memo WHERE owner = ?", (x_user,)).fetchone()[0]
    return {"user": x_user, "memo_count": count}
