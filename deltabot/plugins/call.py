# Modified from https://github.com/Angel-Hair/XUN_Bot/blob/master/xunbot/plugins/call_admin

import time

import nonebot
from nonebot import on_command, CommandSession, helpers
from ..logger import logger

__plugin_name__ = 'call_admin'
__plugin_usage__ = r"""
Send message to admin.
Command(s):
 - /calladmin [msg]
""".strip()


@on_command('calladmin', aliases=('call_admin', '致电管理员'))
async def call_admin(session: CommandSession):

    user_id = session.event['user_id']

    info = session.get('info', prompt='Please input the msg.')
    logger.info("Get Information: {} from ID: {}".format(info, user_id))

    sender_info = "\n\n——@{}({}) | {}".format(session.event['sender']['nickname'], user_id,
                                            time.strftime("%Y-%m-%d", time.localtime(session.event['time'])))

    await helpers.send_to_superusers(nonebot.get_bot(), message=("Message received:\n\n   " + info + sender_info))
    await session.send("Send message successfully :)")
    logger.info("Send message to admin successfully")



@call_admin.args_parser
async def _(session: CommandSession):
    arg = session.current_arg

    if session.is_first_run:
        if arg:
            session.state['info'] = arg
        return

    if not arg:
        session.pause('Please input the message.')

    session.state[session.current_key] = arg