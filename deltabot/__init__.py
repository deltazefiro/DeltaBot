from os import path
import nonebot

from . import config
from . import logger

def run():
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(path.join(path.dirname(__file__), 'plugins'), 'deltabot.plugins')

    nonebot.run()