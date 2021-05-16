import asyncio

import nonebot
from loguru import logger
from nonebot import on_request, RequestSession, helpers, get_bot

__plugin_name__ = '[I]request_process'
__plugin_usage__ = r"""
[Internal plugin]
Approving friend-adding request automatically.
Please DO NOT call the plugin *manually*.
""".strip()

from deltabot import utils


@on_request('friend')
async def approve_friend_adding(session: RequestSession):
    bot = get_bot()
    user_id = session.event.user_id
    user_nickname = await utils.get_stranger_nickname(session, user_id)

    if not bot.config.APPROVE_FRIEND_ADDING:
        logger.info(f"Received {user_nickname}<{user_id}>'s friend adding request.")
        await helpers.send_to_superusers(bot, f"收到 {user_nickname}<{user_id}> 的好友请求")
        return

    await session.approve()
    logger.info(f"Approved {user_nickname}<{user_id}>'s friend adding request.")
    await helpers.send_to_superusers(bot, f"自动通过 {user_nickname}<{user_id}> 的好友请求")
    await asyncio.sleep(3)
    await session.send(get_bot().config.WELCOME_MESSAGE)


@on_request('group.invite')
async def approve_group_inviting(session: RequestSession):
    bot = get_bot()
    logger.debug(session.event)
    user_id = session.event.user_id
    user_nickname = await utils.get_stranger_nickname(session, user_id)
    group_id = session.event.group_id
    group_name = await utils.get_group_name(session, group_id)

    if bot.config.APPROVE_GROUP_INVITE_MODE == 'everyone' or \
            (bot.config.APPROVE_GROUP_INVITE_MODE == 'superuser' and user_id in bot.config.SUPERUSERS):
        try:
            await bot.call_action(action='.handle_quick_operation_async',
                                  context=session.event,
                                  operation={
                                      'approve': True
                                  })
        except nonebot.exceptions.CQHttpError:
            pass

        logger.info(f"Approved group invite request: {group_name}<{group_name}>, from {user_nickname}<{user_id}>")
        await helpers.send_to_superusers(bot, f"自动通过来自 {user_nickname}<{user_id}> 的加群 {group_name}<{group_id}> 邀请")
        return

    logger.info(f"Received group invite request: {group_name}<{group_name}>, from {user_nickname}<{user_id}>")
    await helpers.send_to_superusers(bot, f"收到来自 {user_nickname}<{user_id}> 的加群 {group_name}<{group_id}> 邀请")
    return
