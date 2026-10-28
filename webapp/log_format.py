"""서비스로 돌 때의 로그 '형식' — JSON 한 줄. 로그 수집기가 필드별로 읽기 쉽다."""
import json
import logging

_STD = set(vars(logging.makeLogRecord({})))  # 기본 필드 이름들 — 이 밖의 것이 extra


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        data = {"level": record.levelname, "logger": record.name, "msg": record.getMessage()}
        data.update({k: v for k, v in vars(record).items() if k not in _STD})
        return json.dumps(data, ensure_ascii=False)


def setup_json_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger("memo_api")
    root.handlers[:] = [handler]
    root.setLevel(logging.INFO)
    root.propagate = False
