from os import path
import nonebot
import time
import asyncio

import config

nonebot.init(config)
nonebot.load_builtin_plugins()
nonebot.load_plugins(path.join(path.dirname(__file__), 'plugins'), 'plugins')

nonebot.run()