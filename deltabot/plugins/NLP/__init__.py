from aiocqhttp.message import escape
from nonebot import on_command, CommandSession, get_bot
from nonebot import on_natural_language, NLPSession, IntentCommand
from loguru import logger

from . import itpk_api
from . import tencent_api

__plugin_name__ = '[I]NLP'
__plugin_usage__ = r"""
[Internal plugin]
Internal plugin for natural language conversation.
Based on ITPK api.
Please DO NOT call the plugin *manually*.
""".strip()


@on_command('NLP')
async def NLP(session: CommandSession):
    # 获取可选参数，这里如果没有 message 参数，命令不会被中断，message 变量会是 None
    message = session.state.get('message')

    api = get_bot().config.NLP_API
    if api == 'tencent':
        reply = await tencent_api.call_NLP_api(session, message)
    elif api == 'itpk':
        reply = await itpk_api.call_NLP_api(session, message)
    else:
        logger.warning("无效的 自然语言处理人工智能分支 应用程序接口 类型。请在config.py中配置以启用自然语言处理人工智能分支会话功能。")
        reply = "闲聊对话功能未启用，请使用'/help'查看可用命令"

    if reply:
        # 如果调用机器人成功，得到了回复，则转义之后发送给用户
        await session.send(escape(reply))


@on_natural_language
async def _(session: NLPSession):
    return IntentCommand(60.0, 'NLP', args={'message': session.msg_text})