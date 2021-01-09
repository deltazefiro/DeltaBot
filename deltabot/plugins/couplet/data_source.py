import asyncio
from typing import Optional
from urllib.parse import quote

import aiohttp
from loguru import logger
from nonebot import CommandSession

from ...utils import get_local_proxy


async def call_api(session: CommandSession, text: str) -> Optional[str]:
    url = f"https://ai-backend.binwang.me/chat/couplet/{quote(text, 'utf-8')}"

    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(url, timeout=10, proxy=get_local_proxy()) as response:

                if response.status != 200:
                    logger.error(f"Cannot connect to {url}, Status: {response.status}")
                    await session.send("无法连接到服务器")
                    return None

                return (await response.json())['output']

    except asyncio.TimeoutError:
        logger.error(f"Cannot connect to {url}, Error: Timeout")
        await session.send("请求超时")
