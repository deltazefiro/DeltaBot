import nonebot
import time
from nonebot import on_request, RequestSession, helpers, get_bot

__plugin_name__ = '[I]request_process'
__plugin_usage__ = r"""
[内部插件]
自动批准好友添加请求。
请不要手动调用插件。
""".strip()

@on_request('friend')
async def approve_friend_adding(session: RequestSession):
    await session.approve()
    await helpers.send_to_superusers(nonebot.get_bot(),
                                     "已同意 <%s>的好友请求" %session.event.user_id)
    time.sleep(3)
    await session.send(get_bot().config.WELCOME_MESSAGE)
