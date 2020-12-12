from nonebot import on_command, CommandSession, command
import sys
import nonebot
import time
import asyncio

async def __get_formatted_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())



@nonebot.on_websocket_connect
async def on_setup(event):
    await asyncio.sleep(1)
    await nonebot.helpers.send_to_superusers(nonebot.get_bot(), "DeltaBot has been started. %s"
                                             %(await __get_formatted_time()))
    # logger.log("DeltaBot has been started.")



@on_command('kill', privileged=True)
async def kill(session: CommandSession):
    await session.send("*DeltaBot*掉出了这个世界")
    command.kill_current_session(session.event)



@on_command('ping', aliases=('test', 'Test'))
async def ping(session: CommandSession):
    await session.send("Pong! %s" %(await __get_formatted_time()))



@on_command('log')
async def log(session: CommandSession):
    msg = session.get('msg', prompt="Please enter a log message.")
    # logger.log(msg)
    await session.send("Send msg to log successfully.")

@log.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.state['msg'] = stripped_arg
