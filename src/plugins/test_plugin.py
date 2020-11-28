from nonebot import on_command, CommandSession
import nonebot
import time
import random
import asyncio


@on_command('num2word', aliases=('n2w', 'numtoword'))
async def num2word(session: CommandSession):
    num = int(session.get('num', prompt="Please input an integer between 0 and 10."))
    word_list = "零一二三四五六七八九十"
    await session.send(word_list[num])

@num2word.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['num'] = stripped_arg
        return

    if not stripped_arg:
        # 发送了空白字符，则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('Input invalid. Please input again.')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg