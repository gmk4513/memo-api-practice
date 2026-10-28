# memo-api-practice

[gangmini.com/learn](https://gangmini.com/learn/#arch) 의 **"코드 구조와 설계"** 시리즈를 직접 따라 해 보는 연습 저장소.
한 파일에 HTTP·규칙·SQL 이 다 섞인 78줄짜리 메모 API(`app.py`)를 **레이어드 아키텍처 + 의존성 주입(DI)** 구조로 정리한다.

| 브랜치 / 태그 | 내용 |
|---|---|
| `main` (운영) · 태그 `v0.1.0` | 시작 상태 — 한 파일짜리 `app.py` |
| `dev` (개발) | 여기서 브랜치를 따서 시작한다 |
| `solution` · 태그 `solution-v0.2.0` | 정답 예시 — 커밋 5개로 나눠 정리한 결과 |

## 어디서 하나

**내 컴퓨터의 VS Code 안 터미널**에서 한다. 윈도우는 터미널을 **Git Bash** 로 바꿔 둔다 (명령이 bash 문법이다).
설치할 것: VS Code · Git · Python 3.11 이상. 폴더는 `C:\dev\` 처럼 영어로 된 짧은 경로에 (OneDrive·한글 경로는 피한다).
처음이면 → [실습 환경 준비 — VS Code, 터미널, Git, Python](https://gangmini.com/learn/dev-setup/)

## 시작하기

```bash
git clone https://github.com/gmk4513/memo-api-practice.git
cd memo-api-practice
git switch dev

python -m venv .venv
source .venv/Scripts/activate        # Git Bash 기준. macOS/Linux: source .venv/bin/activate · PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

python smoke.py                      # 지금 상태가 돌아가는지 확인 (단계마다 다시 돌린다)
git switch -c refactor/layered-di    # 내 작업 브랜치
```

그다음은 글을 따라 커밋을 하나씩 쌓는다.

1. [코드 구조 한눈에](https://gangmini.com/learn/arch-overview/) · [패키지와 모듈 나누기](https://gangmini.com/learn/arch-modules/) — 먼저 큰 그림
2. [레이어드 아키텍처 따라 만들기](https://gangmini.com/learn/arch-layers/)
3. [의존성 주입(DI)](https://gangmini.com/learn/arch-di/)
4. [실습: 브랜치 따서 한 파일짜리 API 를 계층 + DI 로 정리하기](https://gangmini.com/learn/arch-refactor-practice/) ← 이 저장소로 하는 글
5. [운영 브랜치와 개발 브랜치](https://gangmini.com/learn/git-main-dev/) — main / dev 를 왜 나누나

## 막히면 정답과 비교

```bash
git log --oneline dev..solution      # 정답의 커밋 5개
git diff dev solution -- src/        # 시작과 정답의 차이
git switch solution && pytest -q     # 정답 테스트 돌려 보기
```

`solution` 에는 글에서 쓴 확인용 스크립트도 있다: `swap_demo.py`(저장소 바꿔 끼우기), `provider_demo.py`(Singleton·Factory), `lifecycle_demo.py`(앱 수명 vs 요청 수명), `demo_requests.py`.

## 쓰는 것

Python 3.11 · FastAPI · pydantic · dependency-injector · pytest · sqlite3(표준 라이브러리)
