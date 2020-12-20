from nonebot import on_command, CommandSession, permission
import math

__plugin_name__ = '[A]boom'
__plugin_usage__ = r"""
EXPLOSION is ART!!!
*Required admin permission*
**过度使用可能触发风控**
Command(s):
 - /boom
""".strip()

@on_command('boom', permission=permission.SUPERUSER)
async def boom(session: CommandSession):
    o = "BOOM!BOOM!BOOM!BOOM!"
    b = ""
    for i in range(200):
        m = round((math.sin(i/5)+1)/2*(len(o)-1))
        b = b + o[:m] + '\n'

    for _ in range(1):
        await session.send(b)