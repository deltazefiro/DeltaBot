from nonebot import on_command
from nonebot.command.argfilter.controllers import handle_cancellation
from nonebot.command.argfilter.validators import between_inclusive, ensure_true

from .data_source import *

"""
Notes:
    若网站访问超时
    请在hosts文件中加入"104.28.28.43 blog.reimu.net"来防止DNS污染
"""

__plugin_name__ = '[H]reimu'
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
                       "[Note]\n - 大部分资源解压密码为⑨\n - 标准码使用方式请自行Google\n - 小心社会性死亡[Doge]")
    key_word = await session.aget('key_word', prompt='你想到哪儿下车？', arg_filters=[handle_cancellation(session)])
    await session.send("正在搜索，请稍后......")
    search_result = await get_search_result(session, key_word)

    if search_result:
        msg = "找到 %d 结果: \n" %len(search_result)
        for i, r in enumerate(search_result):
            msg += "    【%s】%s\n\n" %(i+1, r[0])
        await session.send(msg)

        idx = int(await session.aget('idx', prompt='序号?',
                                     arg_filters=[handle_cancellation(session),
                                                  ensure_true(str.isdigit, message="无效的序号，请重新输入！(输入'取消'可终止)"),
                                                  int,
                                                  between_inclusive(start=1, end=len(search_result), message="序号范围错误！请重新输入~(输入'取消'可终止)")]))

        downlinks = await get_download_links(session, search_result[idx-1][1])
        if downlinks:
            await session.send("下载链接:\n\n%s" %downlinks)
        else:
            await session.send("在本贴中未找到下载链接")


@reimu.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['key_word'] = stripped_arg
        return

    if not stripped_arg:
        if session.current_key == 'key_word':
            await session.pause('没时间等了！快说你要去哪里？')
        else:
            await session.pause('请输入编号!')

    session.state[session.current_key] = stripped_arg


