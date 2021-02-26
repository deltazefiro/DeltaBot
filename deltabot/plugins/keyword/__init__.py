from loguru import logger
from nonebot import NLPSession, on_natural_language, IntentCommand
from nonebot import on_command, CommandSession
from nonebot import permission as perm

from .database import add, ls, rm, match

__plugin_name__ = 'keyword(关键词触发器)'
__plugin_usage__ = r"""
Usage...
""".strip()

@on_natural_language(keywords=None, permission=perm.GROUP)
async def _(session: NLPSession):
    ret = await match(session)
    if ret:
        return IntentCommand(70.0, 'match_keyword', args={'trigger': ret[0], 'rep': ret[1]})

@on_command('match_keyword')
async def match_keyword(session: CommandSession):
    await session.send(f"【关键词触发: {session.state['trigger']}】\n\n {session.state['rep']}")



@on_command('keyword')
async def manage_keyword(session: CommandSession):
    spl = session.get('args').split(maxsplit=1)
    try:
        sub_cmd, args = spl
    except ValueError:
        sub_cmd, args = spl[0], ''

    if sub_cmd == 'add':
        await add(session, args)
    elif sub_cmd == 'ls':
        await ls(session, args)
    elif sub_cmd == 'rm':
        await rm(session, args)
    else:
        logger.debug(f"Subcmd not found: {args}")
        await session.finish(f"无效的命令: '{sub_cmd}'，请使用 '/help keyword' 获取帮助")


@manage_keyword.args_parser
async def _(session: CommandSession):
    arg = session.current_arg.strip()
    if arg:
        session.state['args'] = arg
    else:
        await session.finish(__plugin_usage__)
