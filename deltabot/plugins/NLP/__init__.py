from .itpk_api import call_NLP_api
from aiocqhttp.message import escape
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import render_expression

__plugin_name__ = '[I]NLP'
__plugin_usage__ = r"""
[Internal plugin]
Internal plugin for natural language conversation.
Based on ITPK api.
Please DO NOT call the plugin *manually*.
""".strip()

EXPR_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～'
)


@on_command('NLP')
async def NLP(session: CommandSession):
    # 获取可选参数，这里如果没有 message 参数，命令不会被中断，message 变量会是 None
    message = session.state.get('message')

    reply = await call_NLP_api(session, message)
    if reply:
        # 如果调用机器人成功，得到了回复，则转义之后发送给用户
        await session.send(escape(reply))
    else:
        await session.send(render_expression(EXPR_DONT_UNDERSTAND))


@on_natural_language
async def _(session: NLPSession):
    return IntentCommand(60.0, 'NLP', args={'message': session.msg_text})