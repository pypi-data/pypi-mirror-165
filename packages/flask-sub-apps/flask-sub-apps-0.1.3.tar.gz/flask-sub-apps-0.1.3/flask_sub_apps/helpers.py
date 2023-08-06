import logging
from functools import reduce
from typing import Iterable, Any, List


def in_quotes(string: str) -> str:
    """Wrap string in double quotes."""
    return f'"{string}"'


def merge_lists(lists: Iterable[List[Any]]) -> List[Any]:
    """Merge an iterable of lists into a single list."""
    return reduce(lambda acc, arr: acc + arr, lists, [])


def get_logger() -> logging.Logger:
    """Get logger for FlaskSubApps."""
    return logging.getLogger("FlaskSubApps")
