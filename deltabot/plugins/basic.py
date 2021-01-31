from nonebot import on_command, CommandSession, command, permission
import nonebot
import time
import asyncio
from loguru import logger
from .._version import __version__

__plugin_name__ = 'basic(基础控制)'
__plugin_usage__ = r"""
机器人基础控制插件

Command(s):
  - /ping
    测试机器人存活性
  - /kill
    终止当前命令任务，用于处理卡死
  - /log
    发送信息到控制台
    【需要管理员权限】
  - /version
    获取机器人版本信息
""".strip()

async def __get_formatted_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

@nonebot.on_websocket_connect
async def on_setup(event):
    await asyncio.sleep(1)
    bot = nonebot.get_bot()
    await nonebot.helpers.send_to_superusers(nonebot.get_bot(), "DeltaBot has been started. Version: %s\n%s"
                                             %(__version__, await __get_formatted_time()))
    logger.info("DeltaBot has been started. Version: %s" %__version__)



@on_command('kill', privileged=True)
async def kill(session: CommandSession):
    await session.send("*DeltaBot*掉出了这个世界")
    command.kill_current_session(session.event)



@on_command('version', aliases=('ver'))
async def kill(session: CommandSession):
    bot = nonebot.get_bot()
    await session.send("DeltaBot Version: %s" %__version__)



@on_command('ping')
async def ping(session: CommandSession):
    await session.send("Pong! %s" %(await __get_formatted_time()))



@on_command('log', permission=permission.SUPERUSER)
async def log(session: CommandSession):
    msg = session.get('msg', prompt="Please enter a log message.")
    logger.warning(f"User log received:\n\n\n{msg}\n\n")
    await session.send("Send msg to log successfully.")

@log.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.state['msg'] = stripped_arg
