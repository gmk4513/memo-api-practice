"""앱 전체가 같이 쓰는 예외. HTTP 를 모른다 — 몇 번 상태 코드로 바꿀지는 webapp 이 정한다."""


class AppError(Exception):
    """이 앱에서 일부러 던지는 오류의 부모."""


class NotFound(AppError):
    pass


class PermissionDenied(AppError):
    pass


class InvalidInput(AppError):
    pass
