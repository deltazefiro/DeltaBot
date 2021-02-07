from nonebot import on_command, CommandSession, permission
import os

__plugin_name__ = '[A]getlog(输出log)'
__plugin_usage__ = r"""
输出log文件的最后10行
【需要管理员权限】

Command(s):
 - /getlog
""".strip()

get_relative_path = lambda p: os.path.join(os.path.dirname(__file__), p)

@on_command('getlog', permission=permission.SUPERUSER)
async def get_log(session: CommandSession):
    try:
        with open(get_relative_path('../../logfile.log'), 'r', encoding='utf8') as f:
            content = f.readlines()
    except EOFError:
        await session.send("未找到log文件")

    try:
        content = content[-10:]
    except IndexError:
        pass

    await session.send('\n'.join(content).replace('deltabot.plugins.', ''))