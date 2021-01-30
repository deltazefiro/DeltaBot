from nonebot import on_command, CommandSession, message
from .data_source import *

__plugin_name__ = 'get_ip'
__plugin_usage__ = r"""
使用陷阱网站获取他人ip
Trap provided by https://met.red/

Usage:
    使用命令 '/gettrap' 生成一个陷阱网址（同时生成一个key），
    然后将陷阱网址发送给你想获取ip的用户,
    当此用户进入陷阱网址后, 你可以通过 '/getip' 并输入key获取此用户的ip
    
Command(s):
 - /gettrap [jump_url]
    生成陷阱网址
    [jump_url]: <可选参数>陷阱网址跳转到的网址，默认Baidu
    
 - /getip [key]
    获取用户ip
    请确保陷阱网址已*被访问*
""".strip()

@on_command('gettrap', aliases=('get_trap', 'generate_trap', 'generate_trap_url'))
async def get_trap(session: CommandSession):
    if session.state['jump_url']:
        ret = await generate_trap_url(session, session.state['jump_url'])
    else:
        ret = await generate_trap_url(session)

    if ret:
        await session.send("诱骗连接和获取秘钥分别为:")
        await session.send(ret[0])
        await session.send(ret[1])

@get_trap.args_parser
async def _(session: CommandSession):
    arg = session.current_arg.strip()
    if arg:
        session.state['jump_url'] = arg
    else:
        session.state['jump_url'] = None



@on_command('getip', aliases=('get_ip', 'get_ip_from_trap'))
async def get_trap(session: CommandSession):
    key = session.get('key', prompt="请输入陷阱网址的key")
    ret = await get_ip_from_trap(session, key)

    if ret:
        await session.send("IP: %s\n大致位置: %s" %(ret[0], ret[1]))

@get_trap.args_parser
async def _(session: CommandSession):
    arg = session.current_arg

    if session.is_first_run:
        if arg:
            session.state['key'] = arg
        return

    if not arg:
        session.pause('请输入陷阱网址的key')

    session.state[session.current_key] = arg