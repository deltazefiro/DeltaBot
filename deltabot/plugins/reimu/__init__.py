from nonebot import on_command, CommandSession
from nonebot.command.argfilter.controllers import handle_cancellation

from .data_source import *

# __plugin_name__ = 'reimu'
__plugin_usage__ = r"""
[ThirdParty plugin]
[Modified from https://github.com/Angel-Hair/XUN_Bot/tree/master/xunbot/plugins/reimu]

Command(s):
 - /reimu [目的地]
    ps: 请尽量提供具体的目的地名称
""".strip()


@on_command('reimu', aliases=('reimu', '上车', '上車', '开车'))
async def reimu(session: CommandSession):
    await session.send("[Hidden function]ReimuSearch\n"
                       "本模块修改自Angel-Hair/XUN_Bot\n\n"
                       "[Note]\n - 大部分资源解压密码为⑨\n - 标准码使用方式请自行Google")
    key_word = await session.aget('key_word', prompt='你想到哪儿下车？')#, arg_filters=[handle_cancellation])
    search_result = await get_search_result(key_word)

    if search_result:
        msg = "Found %d results: \n" %len(search_result)
        for i, r in enumerate(search_result):
            msg += "    【%s】%s\n\n" %(i+1, r[0])
        await session.send(msg)

        idx = int(await session.aget('idx', prompt='Index?(exit if input invalid)'))#, arg_filters=[handle_cancellation]))

        if 0 < idx < len(search_result):
            downlinks = await get_download_links(search_result[idx-1][1])
            if downlinks:
                await session.send("Downlinks:\n\n%s" %downlinks)
            else:
                await session.send("No links are found in the post.Please try another one.")
        else:
            await session.send("Invalid input. Exit...")

    else:
        print("Not found reimu")
        await session.send("Search not found.")


@reimu.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    print(session.current_key, stripped_arg)

    if session.is_first_run:
        if stripped_arg:
            session.state['key_word'] = stripped_arg
        return

    if not stripped_arg:
        if session.current_key == 'key_word':
            await session.pause('没时间等了！快说你要去哪里？')
        else:
            await session.pause('看不懂英语吗?输入编号![Doge]')

    session.state[session.current_key] = stripped_arg


