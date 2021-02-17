from nonebot import on_command, CommandSession, get_loaded_plugins
from nonebot import on_natural_language, NLPSession, IntentCommand
import re
from .._version import __version__

__plugin_name__ = 'usage(使用帮助)'
__plugin_usage__ = r"""
显示使用帮助

Command(s):
 - /help [插件名称]
    查询特定插件的使用帮助，当无参数时，返回功能列表
""".strip()


@on_command('usage', aliases=('help', '使用帮助', '帮助', '使用方法'))
async def usage(session: CommandSession):
    plugins = list(filter(lambda p: p.name, get_loaded_plugins()))

    is_admin = session.event['user_id'] in session.bot.config.SUPERUSERS

    arg = session.current_arg_text.strip().lower()
    if not arg:
        plugins_list = ['    » ' + re.sub(r'\[.*]', '', p.name).replace('(', '  (')
                        for p in plugins
                        if ('[I]' not in p.name) and ('[H]' not in p.name) and
                        ('[A]' not in p.name or is_admin)]

        msg = f'DeltaBot version {__version__}\n'\
               + '\n插件列表:\n'\
               + '\n'.join(plugins_list)

        await session.send(msg +\
                           "\n\n发送 help+空格+插件名称 获取该插件的详细使用帮助\n"
                           "若在群聊中使用请先@本机器人再输入命令\n\n"
                           "在网页上查看更多帮助: https://233a344a455.github.io/DeltaBot/usage.html")
        return

    plugin_usage = [p.usage for p in plugins if arg == re.sub(r'\[.*]|\(.*\)', '', p.name).strip()]
    if plugin_usage:
        for p in plugin_usage:
            await session.send(f"「{arg}」插件使用说明:\n\n" + p)
    else:
        await session.send(f"插件'{arg}'不存在，请确认插件名称是否正确")


@on_natural_language(keywords=['功能', '帮助', '使用', '用法', 'help', 'usage'])
async def _(session: NLPSession):
    return IntentCommand(70.0, 'usage')


@on_command('unknown_command')
async def unknown_command(session: CommandSession):
    await session.send("未知命令，请输入/help查看帮助")


@on_natural_language(keywords='/')
async def _(session: NLPSession):
    return IntentCommand(70.0, 'unknown_command', args={'msg': session.msg_text})
