import json
import os
from nonebot import CommandSession, NLPSession
from loguru import logger

"""
data/keyword.json 格式
=============================
{
    <group_id1>: {
        <trigger1>: <reply1>,
        <trigger2>: <reply2>,
        ...
    },
    
    <group_id2>: {
        ...
    },
    
    ...
}
=============================
"""

get_relative_path = lambda p: os.path.join(os.path.dirname(__file__), p)

def dump_rules(content: dict):
    os.makedirs(get_relative_path('data'), exist_ok=True)
    with open(get_relative_path('data/rules.json'), 'w') as f:
        json.dump(content, f)

def load_rules():
    try:
        with open(get_relative_path('data/rules.json'), 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

async def add(session: CommandSession, args: str):
    group_id = str(session.event.group_id)
    if not group_id:
        session.finish("请在群组中使用本命令！")
    rules = load_rules()

    try:
        trigger, reply = args.strip().split(' ', maxsplit=1)
    except ValueError:
        logger.debug(f"Unable to parse args: {args}")
        await session.finish("无效的参数!\n"
                           "使用方法: /keyword add [触发词] [回复消息]\n"
                           "示例: /keyword add 笨蛋 请文明交流!")
        return

    if not group_id in rules:
        rules[group_id] = {trigger: reply}
    else:
        if trigger in rules[group_id]:
            session.finish(f"关键词 '{trigger}' 已存在!")
        rules[group_id][trigger] = reply

    dump_rules(rules)
    logger.info(f"Keyword added: Group {group_id}, Trigger '{trigger}', Reply '{reply}'")
    await session.send(f"成功添加规则: 触发词 '{trigger}', 回复 '{reply}'")

async def ls(session: CommandSession, args: str):
    group_id = str(session.event.group_id)
    if not group_id:
        session.finish("请在群组中使用本命令！")
    rules = load_rules()

    if not group_id in rules:
        session.finish("本群组尚未设置关键词触发规则，请使用 '/keyword add' 命令添加")

    r = rules[group_id]
    msg = f'群组{group_id}的关键词:\n\n'
    msg += '\n\n'.join(f"   » 关键词: {keyword}, 回复: {reply}" for keyword, reply in r.items())
    await session.send(msg)

async def rm(session: CommandSession, args: str):
    pass

async def match(session: NLPSession):
    group_id = str(session.event.group_id)
    return None