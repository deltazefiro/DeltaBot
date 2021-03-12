import json
import os
from nonebot import CommandSession, NLPSession
from loguru import logger
from nonebot.command.argfilter.controllers import handle_cancellation
from nonebot.command.argfilter.validators import ensure_true, between_inclusive

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
_global_rules = None


def dump_rules(content: dict):
    global _global_rules
    _global_rules = content
    os.makedirs(get_relative_path('data'), exist_ok=True)
    with open(get_relative_path('data/rules.json'), 'w') as f:
        json.dump(content, f)

def load_rules(force_reload=False):
    global _global_rules

    if force_reload or not _global_rules:
        try:
            with open(get_relative_path('data/rules.json'), 'r') as f:
                _global_rules = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            _global_rules = {}
    return _global_rules


async def add(session: CommandSession, args: str):
    group_id = session.event.group_id
    if not group_id:
        logger.debug("Group only cmd is called in private chat!")
        session.finish("请在群组中使用本命令！")
    group_id = str(group_id)
    rules = load_rules(force_reload=True)

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



async def ls(session: CommandSession):
    group_id = session.event.group_id
    if not group_id:
        logger.debug("Group only cmd is called in private chat!")
        session.finish("请在群组中使用本命令！")
    group_id = str(group_id)
    rules = load_rules(force_reload=True)

    if not group_id in rules:
        logger.debug(f"No trigger words have been set for group {group_id}.")
        session.finish("本群组尚未设置关键词触发规则，请使用 '/keyword add' 命令添加")

    r = rules[group_id]
    logger.debug(f"Group {group_id} Trigger words: {r}")
    msg = f'【群组{group_id}的关键词】\n'
    msg += '\n'.join(f"   » 关键词: '{keyword}', 回复: '{reply if len(reply) <= 10 else reply[:10]+'...'}'" for keyword, reply in r.items())
    await session.send(msg)



async def rm(session: CommandSession, args: str):
    group_id = session.event.group_id
    if not group_id:
        logger.debug("Group only cmd is called in private chat!")
        session.finish("请在群组中使用本命令！")
    group_id = str(group_id)
    rules = load_rules(force_reload=True)

    if not args.split():
        logger.debug(f"Got an empty arg!")
        await session.finish("无效的参数!\n"
                           "使用方法: /keyword rm [触发词]\n"
                           "示例: /keyword rm 笨蛋")
        return

    if not group_id in rules:
        logger.debug(f"No trigger words have been set for group {group_id}.")
        session.finish("本群组尚未设置关键词触发规则，请使用 '/keyword add' 命令添加")

    group_rules = rules[group_id]
    m = [k for k in group_rules.keys() if args in k]
    if m:
        msg = f"匹配 '{args}' 的触发词: \n" + '\n'.join([F' »【{i+1}】{t}' for i, t in enumerate(m)])
        await session.send(msg)

        idx = int(await session.aget('idx', prompt="请输入要删除的触发关键词序号 (输入'取消'可终止命令)",
                                     arg_filters=[handle_cancellation(session),
                                                  ensure_true(str.isdigit, message="无效的序号!请重输 (输入'取消'可终止命令)"),
                                                  int,
                                                  between_inclusive(start=1, end=len(m), message="序号范围错误!请重输 (输入'取消'可终止命令)")]))

        del rules[group_id][m[idx-1]]
        if not rules[group_id]:
            del rules[group_id]
        dump_rules(rules)
        logger.info(f"Removed trigger word '{args}' for group {group_id}.")
        await session.send("删除成功!")
    else:
        logger.debug(f"Trigger word '{args}' not found!")
        await session.send(f"未找到匹配 '{args}' 的触发词! 请使用 '/keyword ls' 查看所有触发词")


async def match(session: NLPSession):
    group_id = str(session.event.group_id)
    try:
        r = load_rules()[group_id]
        for k in r.keys():
            if k in session.msg:
                return k, r[k]

    except KeyError:
        return None