import logging
import sys
from types import FrameType
from typing import TYPE_CHECKING, Any, cast

from loguru import logger

from app.core.constants import LogLevelEnum

if TYPE_CHECKING:
    from loguru import Record
else:
    Record = dict[str, Any]


class Formatter:
    @staticmethod
    def json_formatter(record: Record) -> str:
        # Обрезаем `\n` в конце логов, т.к. в json формате переносы не нужны
        return record.get("message", "").strip()

    @staticmethod
    def text_formatter(record: Record) -> str:
        # WARNING !!!
        # Функция должна возвращать строку, которая содержит только шаблоны для форматирования.
        # Если в строку прокидывать значения из record (или еще откуда-либо),
        # то loguru может принять их за f-строки и попытается обработать, что приведет к ошибке.
        # Например, если нужно достать какое-то значение из поля extra, вместо того чтобы прокидывать его в строку
        # формата, нужно прокидывать подстроку вида {extra[тут_ключ]}

        if message := record.get("message", ""):
            record["message"] = Formatter.scrap_sensitive_info(message)

        # Стандартный формат loguru. Задается через env LOGURU_FORMAT
        format_ = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<magenta>{name}</magenta>:<magenta>{function}</magenta>:<magenta>{line}</magenta> - "
            "<level>{message}</level>"
        )

        # Добавляем мета параметры по типу user_id, art_id, которые передаются через logger.bind(...)
        extra = record["extra"]
        if extra:
            formatted = ", ".join(f"{key}" + "={extra[" + str(key) + "]}" for key, value in extra.items())
            format_ += f" - <cyan>{formatted}</cyan>"

        format_ += "\n"

        if record["exception"] is not None:
            format_ += "{exception}\n"

        return format_

    @staticmethod
    def scrap_sensitive_info(message: str) -> str:
        return message


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, Formatter.scrap_sensitive_info(record.getMessage())
        )


def configure_logging(*, level: LogLevelEnum, enable_json_logs: bool) -> None:
    intercept_handler = InterceptHandler()

    formatter = Formatter.json_formatter if enable_json_logs else Formatter.text_formatter

    base_config_handlers = [intercept_handler]

    base_loguru_handler = {
        "level": level.name,
        "serialize": enable_json_logs,
        "format": formatter,
        "colorize": False,
    }
    loguru_handlers = [
        {**base_loguru_handler, "colorize": True, "sink": sys.stdout},
    ]


    logging.basicConfig(handlers=base_config_handlers, level=level.name)
    logger.configure(handlers=loguru_handlers)

