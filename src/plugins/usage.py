from nonebot import on_command, CommandSession, get_loaded_plugins
from nonebot import on_natural_language, NLPSession, IntentCommand

__plugin_name__ = 'usage'
__plugin_usage__ = r"""
显示使用帮助
 - help [plugin_name]
    查询特定插件的使用帮助
    当无参数时，返回功能列表
""".strip()


@on_command('usage', aliases=('help', '使用帮助', '帮助', '使用方法'))
async def usage(session: CommandSession):
    plugins = list(filter(lambda p: p.name, get_loaded_plugins()))

    arg = session.current_arg_text.strip().lower()
    if not arg:
        await session.send(__plugin_usage__)
        await session.send('我现在支持的功能有：\n\n' + '\n'.join(p.name for p in plugins))
        return

    check = set(filter(lambda p: p.name.lower() == arg, plugins))
    if check:
        for p in check:
            await session.send(p.usage)
    else:
        await session.send("功能不存在")

@on_command('unknown_command')
async def unknown_command(session: CommandSession):
    await session.send("未知命令，请输入/help查看帮助")

@on_natural_language
async def _(session: NLPSession):
    return IntentCommand(60.0, 'unknown_command', args={'msg': session.msg_text})