from nonebot import on_command, CommandSession, get_loaded_plugins
from nonebot import on_natural_language, NLPSession, IntentCommand
from .._version import __version__
import nonebot

__plugin_name__ = 'usage'
__plugin_usage__ = r"""
显示使用帮助
 - /help [plugin_name]
    查询特定插件的使用帮助
    当无参数时，返回功能列表
""".strip()


@on_command('usage', aliases=('help', '使用帮助', '帮助', '使用方法'))
async def usage(session: CommandSession):
    plugins = list(filter(lambda p: p.name, get_loaded_plugins()))

    arg = session.current_arg_text.strip().lower()
    if not arg:
        plugins_list = ['    - ' + p.name.replace(']', '] ')
                        for p in plugins
                        if ('[I]' not in p.name) and ('[H]' not in p.name)]
        await session.send(__plugin_usage__)
        await session.send('DeltaBot v%s'%__version__
                           + '\n插件列表:\n'
                           + '\n'.join(plugins_list))
        return

    plugin_usage = [p.usage for p in plugins if p.name in (arg, f'[I]{arg}', f'[A]{arg}')]
    if plugin_usage:
        for p in plugin_usage:
            await session.send(p)
    else:
        await session.send("功能不存在")

@on_natural_language(keywords=['功能', '帮助', '使用', '用法', 'help', 'usage'])
async def _(session: NLPSession):
    return IntentCommand(70.0, 'usage')


@on_command('unknown_command')
async def unknown_command(session: CommandSession):
    await session.send("未知命令，请输入/help查看帮助")

@on_natural_language(keywords='/')
async def _(session: NLPSession):
    return IntentCommand(70.0, 'unknown_command', args={'msg': session.msg_text})