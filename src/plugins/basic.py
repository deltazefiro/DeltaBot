from nonebot import on_command, CommandSession, command
import sys
import nonebot
import time
import asyncio
from logger import logger

async def __get_formatted_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())



@nonebot.on_websocket_connect
async def on_setup(event):
    await asyncio.sleep(1)
    bot = nonebot.get_bot()
    await nonebot.helpers.send_to_superusers(nonebot.get_bot(), "DeltaBot has been started. Version: %s\n%s"
                                             %(bot.config.VERSION, await __get_formatted_time()))
    logger.info("DeltaBot has been started. Version: %s" %bot.config.VERSION)



@on_command('kill', privileged=True)
async def kill(session: CommandSession):
    await session.send("*DeltaBot*掉出了这个世界")
    command.kill_current_session(session.event)



@on_command('version', aliases=('ver'))
async def kill(session: CommandSession):
    bot = nonebot.get_bot()
    await session.send("DeltaBot Version: %s" %bot.config.VERSION)



@on_command('ping', aliases=('test', 'Test'))
async def ping(session: CommandSession):
    await session.send("Pong! %s" %(await __get_formatted_time()))



@on_command('log')
async def log(session: CommandSession):
    msg = session.get('msg', prompt="Please enter a log message.")
    logger.warn(msg)
    await session.send("Send msg to log successfully.")

@log.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.state['msg'] = stripped_arg
