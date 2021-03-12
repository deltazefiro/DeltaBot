from loguru import logger
from nonebot import NLPSession, on_natural_language, IntentCommand
from nonebot import on_command, CommandSession
from nonebot import permission as perm

from .database import add, ls, rm, match

__plugin_name__ = 'keyword(关键词触发)'
__plugin_usage__ = r"""
设置特定关键词，触发机器人自动回复指定信息
【以下命令仅在群组中可用】
【需要机器人管理员(SuperUser)/群组管理员(GroupAdmin)权限】

Command(s):
 - /keyword add [触发词] [回复内容]
    添加触发词
    
 - /keyword ls
    列出设置的触发词
 
 - /keyword rm [触发词]
    删除特定的触发词
    
Example:
    如需检测到群信息中包含 '笨蛋' 自动回复 '请文明交流'，则使用 '/keyword add 笨蛋 请文明交流' 添加该触发词
    如要删除上述触发词，可输入 '/keyword rm 笨' 然后选择对应序号删除
""".strip()

@on_natural_language(keywords=None, permission=perm.GROUP, only_to_me=False)
async def _(session: NLPSession):
    ret = await match(session)
    if ret:
        return IntentCommand(70.0, 'match_keyword', args={'trigger': ret[0], 'rep': ret[1]})

@on_command('match_keyword')
async def match_keyword(session: CommandSession):
    await session.send(f"【关键词触发: {session.state['trigger']}】\n {session.state['rep']}")



@on_command('keyword', permission=perm.SUPERUSER | perm.GROUP_ADMIN)
async def manage_keyword(session: CommandSession):
    spl = session.get('args').split(maxsplit=1)
    try:
        sub_cmd, args = spl
    except ValueError:
        sub_cmd, args = spl[0], ''

    if sub_cmd == 'add':
        await add(session, args)
    elif sub_cmd == 'ls':
        await ls(session)
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
