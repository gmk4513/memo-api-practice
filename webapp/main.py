"""3단계: HTTP 는 webapp 으로. 아직 조립은 손으로 한다(다음 단계에서 컨테이너로)."""
import sqlite3

from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse

from src.common.exceptions import InvalidInput, NotFound, PermissionDenied
from src.memo.repository import SqliteMemoRepository
from src.memo.service import MemoService
from webapp.routers import memo

STATUS = {NotFound: 404, PermissionDenied: 403, InvalidInput: 400}


def create_app(db_path: str = "memo.db") -> FastAPI:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    app = FastAPI(title="memo-api")
    app.state.memo_service = MemoService(SqliteMemoRepository(conn))  # 손으로 조립
    app.include_router(memo.router)

    for exc_type, status in STATUS.items():
        def handler(request: Request, exc: Exception, status: int = status) -> JSONResponse:
            return JSONResponse({"detail": str(exc)}, status_code=status)
        app.add_exception_handler(exc_type, handler)

    @app.get("/me")
    def me(request: Request, x_user: str = Header()):
        return {"user": x_user, "memo_count": request.app.state.memo_service.count_memos(x_user)}

    return app


app = create_app()
