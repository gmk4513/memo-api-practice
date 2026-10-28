"""로거 꺼내기. src 는 '무엇을' 남길지만 정한다.
'어떻게'(JSON 한 줄, 사람이 읽는 한 줄 …)는 바깥(webapp, tests)이 정한다."""
import logging


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"memo_api.{name}")
