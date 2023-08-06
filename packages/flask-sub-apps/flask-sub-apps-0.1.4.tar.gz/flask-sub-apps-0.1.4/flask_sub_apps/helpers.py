import logging


def in_quotes(string: str) -> str:
    """Wrap string in double quotes."""
    return f'"{string}"'


def get_logger() -> logging.Logger:
    """Get logger for FlaskSubApps."""
    return logging.getLogger("FlaskSubApps")
