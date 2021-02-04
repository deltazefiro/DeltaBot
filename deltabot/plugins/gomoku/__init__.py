"""
五子棋的搜索算法使用cpp编写 (search.cpp) 以保证运行效率
目前仅提供 linux-amd64 的编译版本
首次运行时，程序会通过GithubCDN自动下载其可执行文件

若使用非 linux-amd64 平台 或 下载出现问题
也可以使用此命令本地编译本文件夹下的 search.cpp:
'g++ -O3 -fPIC -shared -o search.so search.cpp'
(需要gcc编译环境)
"""
import re

from nonebot import on_command, CommandSession, MessageSegment, context_id
from nonebot.command.argfilter.controllers import handle_cancellation
from nonebot.command.argfilter.validators import not_empty, match_regex

from .game import GomokuGame
import asyncio

__plugin_name__ = '[E]gomoku(五子棋)'
__plugin_usage__ = r"""
与机器人切磋切磋五子棋 :D
【实用性功能，不稳定！】

Command(s):
 - /gomoku
    开始玩耍五子棋
""".strip()

USER, BOT = 1, 2
ALPHABET = list('ABCDEFGHIJKLMNO')


@on_command('gomoku', aliases=('gomo', '五子棋'))
async def gomoku(session: CommandSession):
    await session.send("游戏开始！\n"
                       "玩家黑棋，机器人白棋\n"
                       "落子格式: 例如'e9'或'E9'\n"
                       "字母在前数字在后，不分大小写")

    g = GomokuGame(context_id(session.ctx, use_hash=True))
    await session.send(MessageSegment.image(g.get_img()))
    await asyncio.sleep(0.5)
    while True:
        inp = await session.aget('input', force_update=True, prompt="请玩家落子(发送'取消'以退出)",
                                 arg_filters=[not_empty(message="输入不能为空！请重新落子"),
                                              handle_cancellation(session),
                                              match_regex(r'[a-oA-O](1[0-5]|[1-9])', fullmatch=True,
                                                          message="无效的输入！落子格式: 例如'e9'或'E9'\n"
                                                                  "字母在前数字在后，不分大小写")])
        x, y = re.match(r'([a-oA-O])(1[0-5]|[1-9])', inp).groups()
        x, y = ALPHABET.index(x.upper()), int(y) - 1
        if not g.set_chess(x, y, USER):
            await session.send(f"位置'{inp}'已存在旗子，请重新输入")
            continue

        sco = -g.estimate()
        g.update_display()
        if sco > 1e6:
            await session.send("恭喜！你赢了" + MessageSegment.image(g.get_img()))
            return

        x, y = g.search()
        g.set_chess(x, y, BOT)
        g.display.draw_chess(x, y, BOT, high_lighted=True)
        sco = -g.estimate()
        if sco < -1e6:
            await session.send("你输啦 ~\(≧▽≦)/~" + MessageSegment.image(g.get_img()))
            return

        await session.send(f"估计分数: {sco}" + MessageSegment.image(g.get_img()))
        await asyncio.sleep(0.8)
