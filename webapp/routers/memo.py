"""표현 계층 — HTTP 요청을 받아 서비스에 넘기고, 결과를 응답 모양(DTO)으로 바꾼다.
여기에는 규칙도, SQL 도 없다."""
from datetime import datetime

from fastapi import APIRouter, Depends, Header, Request
from pydantic import BaseModel

from src.memo.domains import Memo
from src.memo.service import MemoService

router = APIRouter(prefix="/memos", tags=["memo"])


# ---- DTO: 바깥과 주고받는 모양. 도메인과 일부러 따로 둔다 ----
class MemoCreateRequest(BaseModel):
    title: str
    body: str = ""


class MemoRenameRequest(BaseModel):
    title: str


class MemoResponse(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime  # owner 는 응답에 내보내지 않는다

    @classmethod
    def from_domain(cls, memo: Memo) -> "MemoResponse":
        return cls(id=memo.id, title=memo.title, body=memo.body, created_at=memo.created_at)


# ---- 서비스 꺼내기: 앱이 켜질 때 한 번 만든 컨테이너에서 ----
def memo_service(request: Request) -> MemoService:
    return request.app.state.container.memo.service()


@router.post("", status_code=201, response_model=MemoResponse)
def create_memo(req: MemoCreateRequest, x_user: str = Header(),
                service: MemoService = Depends(memo_service)):
    return MemoResponse.from_domain(service.create_memo(x_user, req.title, req.body))


@router.get("", response_model=list[MemoResponse])
def list_memos(x_user: str = Header(), service: MemoService = Depends(memo_service)):
    return [MemoResponse.from_domain(m) for m in service.list_memos(x_user)]


@router.get("/{memo_id}", response_model=MemoResponse)
def get_memo(memo_id: int, x_user: str = Header(), service: MemoService = Depends(memo_service)):
    return MemoResponse.from_domain(service.get_memo(x_user, memo_id))


@router.patch("/{memo_id}", response_model=MemoResponse)
def rename_memo(memo_id: int, req: MemoRenameRequest, x_user: str = Header(),
                service: MemoService = Depends(memo_service)):
    return MemoResponse.from_domain(service.rename_memo(x_user, memo_id, req.title))


@router.delete("/{memo_id}", status_code=204)
def delete_memo(memo_id: int, x_user: str = Header(), service: MemoService = Depends(memo_service)):
    service.delete_memo(x_user, memo_id)
