from datetime import datetime

import sys
sys.path.append('../')

from aiocqhttp.exceptions import Error as CQHttpError
import nonebot
import time

@nonebot.scheduler.scheduled_job('interval', minutes=120)
async def heartbeat():
    bot = nonebot.get_bot()
    t_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        await bot.send_private_msg(user_id=2781945273, message="[Heartbeat][%s]DeltaBot is running ..." %t_now)
    except CQHttpError as e:
        nonebot.logger.error(e)
