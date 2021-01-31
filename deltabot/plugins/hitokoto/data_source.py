import asyncio

import aiohttp
from loguru import logger
from nonebot import CommandSession, get_bot

from ...utils import get_local_proxy


async def get_hitokoto(session: CommandSession):
    category = get_bot().config.HITOKOTO_CATEGORY
    url = f"https://v1.hitokoto.cn/?c={'&c='.join(category)}"

    try:
        logger.debug(f"Start getting {url} ...")
        async with aiohttp.ClientSession() as client:
            async with client.get(url, timeout=10, proxy=get_local_proxy()) as response:

                if response.status != 200:
                    logger.error(f"Cannot connect to {url}, Status: {response.status}")
                    await session.send("无法连接到服务器")
                    return None

                r = await response.json()
                logger.debug(f"Response: {r}")
                if r.get('hitokoto'):
                    return r['hitokoto'], r['from_who'], r['from']
                else:
                    logger.error(f"No result found in the category. Please make sure category is valid.")
                    await session.send("插件配置错误")

    except asyncio.TimeoutError:
        logger.error(f"Cannot connect to {url}, Error: Timeout")
        await session.send("请求超时")
