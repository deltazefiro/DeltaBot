from nonebot import on_command, CommandSession

from .data_source import from_reimu_get_info

__plugin_name__ = 'reimu'
__plugin_usage__ = r"""
[ThirdParty plugin]
[Modified from https://github.com/Angel-Hair/XUN_Bot/tree/master/xunbot/plugins/reimu]

Usage:
 - reimu [目的地]
    ps: 请尽量提供具体的目的地名称
""".strip()


@on_command('reimu', aliases=('reimu', '上车', '上車'))
async def reimu(session: CommandSession):
    key_word = session.get('key_word', prompt='你想到哪儿下车？')
    reimu_ret = await from_reimu_get_info(key_word)
    if reimu_ret:
        await session.send(reimu_ret)
    else:
        print("Not found reimuInfo")
        await session.send("[ERROR]Not found reimuInfo")


@reimu.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['key_word'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('没时间等了！快说你要去哪里？')

    session.state[session.current_key] = stripped_arg

