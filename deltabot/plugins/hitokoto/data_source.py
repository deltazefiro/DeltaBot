import asyncio

import aiohttp
from loguru import logger
from nonebot import CommandSession, get_bot

from ...utils import get_local_proxy


async def get_hitokoto(session: CommandSession):
    category = get_bot().config.HITOKOTO_CATEGORY
    url = f"https://v1.hitokoto.cn/?c={'&c='.join(category)}"

    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(url, timeout=10, proxy=get_local_proxy()) as response:

                if response.status != 200:
                    logger.error(f"无法连接到  {url}, 错误状态: {response.status}")
                    await session.send("无法连接到服务器")
                    return None

                r = await response.json()
                if r.get('hitokoto'):
                    return r['hitokoto'], r['from_who'], r['from']
                else:
                    logger.error(f"在类中没有发现结果 请确认类是有效的")
                    await session.send("插件配置错误")

    except asyncio.TimeoutError:
        logger.error(f"无法连接到  {url}, 错误: 超时")
        await session.send("请求超时")
