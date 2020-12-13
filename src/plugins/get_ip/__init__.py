from nonebot import on_command, CommandSession, message
from .data_source import *

__plugin_name__ = 'get_ip'
__plugin_usage__ = r"""
Get other's ip with a trap website.
Usage:
    Use '/gettrap' to generate a trap url (a website can getting IP addr) with a key,
    Then send the trap url to the one you want to get IP,
    After they visit the site, use '/getip' and the key to get the information.
    
Command(s):
 - /gettrap [jump_url]
    Generate a trap url.
    [jump_url]: Optional arg, the url jump to after getting ip.
    
 - /getip [key]
    Get the user's ip from trap.
    Please make sure the trap has been *VISITED*
""".strip()

@on_command('gettrap', aliases=('get_trap', 'generate_trap', 'generate_trap_url'))
async def get_trap(session: CommandSession):
    if session.state['jump_url']:
        ret = await generate_trap_url(session.state['jump_url'])
    else:
        ret = await generate_trap_url()

    if ret:
        await session.send("TrapURL & Key:")
        await session.send(ret[0])
        await session.send(ret[1])
    else:
        await session.send("Failed to get TrapURL.")

@get_trap.args_parser
async def _(session: CommandSession):
    arg = session.current_arg.strip()
    if arg:
        session.state['jump_url'] = arg
    else:
        session.state['jump_url'] = None



@on_command('getip', aliases=('get_ip', 'get_ip_from_trap'))
async def get_trap(session: CommandSession):
    key = session.get('key', prompt="Please input the trap key.")
    ret = await get_ip_from_trap(key)

    if ret:
        await session.send("IP: %s\nApprox.addr: %s" %(ret[0], ret[1]))
    else:
        await session.send("Failed to get IP.")

@get_trap.args_parser
async def _(session: CommandSession):
    arg = session.current_arg

    if session.is_first_run:
        if arg:
            session.state['key'] = arg
        return

    if not arg:
        session.pause('Please input the trap key.')

    session.state[session.current_key] = arg