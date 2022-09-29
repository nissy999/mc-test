from typing import Optional, List
import uuid


class LoggedException(Exception):
    """
    Custom exception indicating an exception has already been thrown and allows correlation between log messages
    """

    # consts for demo
    _LOGGED = 'logged'
    _PREFIX_CORRELATION_ID = 'cid'
    _DELIMITER = ' - '

    def __init__(self,
                 correlation_id: Optional[str] = None,
                 msg: Optional[str] = None,
                 ex: Optional[Exception] = None, *args):
        super().__init__(*args)
        self._msg: Optional[str] = msg if isinstance(msg, str) and msg.strip() else None
        self._ex: Optional[Exception] = ex if ex is not None and  isinstance(ex, Exception) else None
        self._correlation_id: str = correlation_id if correlation_id else str(uuid.uuid4())

    @property
    def correlation_id(self) -> str:
        return self._correlation_id

    @property
    def msg(self) -> Optional[str]:
        return self._msg

    @property
    def ex(self) -> Optional[Exception]:
        return self._ex

    def __str__(self) -> str:
        parts: List[str] = [self.msg] if self.msg else []
        parts.append(f'{self._PREFIX_CORRELATION_ID}:{self.correlation_id}')
        return self._DELIMITER.join(parts)
