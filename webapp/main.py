"""앱 조립 — 컨테이너를 '한 번' 만들고, 라우터를 붙이고, 예외를 HTTP 상태 코드로 바꾼다.

    uvicorn webapp.main:app --reload
"""
from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse

from src.common.exceptions import InvalidInput, NotFound, PermissionDenied
from src.container import AppContainer
from webapp.log_format import setup_json_logging
from webapp.routers import memo

STATUS = {NotFound: 404, PermissionDenied: 403, InvalidInput: 400}


def create_app(db_path: str = "memo.db", container: AppContainer | None = None) -> FastAPI:
    setup_json_logging()
    if container is None:
        container = AppContainer()
        container.config.db_path.from_value(db_path)

    app = FastAPI(title="memo-api")
    app.state.container = container  # 앱 수명 = 컨테이너 수명
    app.include_router(memo.router)

    for exc_type, status in STATUS.items():
        def handler(request: Request, exc: Exception, status: int = status) -> JSONResponse:
            return JSONResponse({"detail": str(exc)}, status_code=status)
        app.add_exception_handler(exc_type, handler)

    @app.get("/me")
    def me(request: Request, x_user: str = Header()):
        return request.app.state.container.user.profile_service().profile(x_user)

    return app


app = create_app()
