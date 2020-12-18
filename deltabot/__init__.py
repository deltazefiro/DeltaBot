from os import path
from . import config
import nonebot
import os

def run():
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(path.join(path.dirname(__file__), 'plugins'), 'deltabot.plugins')

    nonebot.run()