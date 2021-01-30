import sys
import logging
from loguru import logger
from . import config

class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


for log in [logging.getLogger('nonebot'), logging.getLogger('aiocqhttp')]:
    for handler in log.handlers:
        log.removeHandler(handler)

logging.getLogger("aiocqhttp").addHandler(InterceptHandler())
logging.getLogger("nonebot").addHandler(InterceptHandler())

logger.remove()
logger.add(sys.stdout,
           level= 'DEBUG' if config.DEBUG else 'INFO',
           colorize=True,
           format="<g>{time:YYYY-MM-DD HH:mm:ss}</g> <level>| {level} |</level> <c>{name}</c>:<c>{function}</c> - <level>{message}</level>")

logger.add('logfile.log', rotation='10 MB',
           filter='deltabot',
           level='INFO',
           colorize=False,
           format="<g>{time:YYYY-MM-DD HH:mm:ss}</g> <level>| {level} |</level> <c>{name}</c>:<c>{function}</c> - <level>{message}</level>")