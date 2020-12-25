import nonebot
import time
from nonebot import on_request, RequestSession, helpers, get_bot

__plugin_name__ = '[I]request_process'
__plugin_usage__ = r"""
[Internal plugin]
Approving friend-adding request automatically.
Please DO NOT call the plugin *manually*.
""".strip()

@on_request('friend')
async def approve_friend_adding(session: RequestSession):
    await session.approve()
    await helpers.send_to_superusers(nonebot.get_bot(),
                                     "Approved user <%s>'s friend-adding request." %session.event.user_id)
    time.sleep(3)
    await session.send(get_bot().config.WELCOME_MESSAGE)
