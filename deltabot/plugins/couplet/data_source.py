import asyncio
from typing import Optional
from urllib.parse import quote

import aiohttp
from loguru import logger
from nonebot import CommandSession

from ...utils import get_local_proxy


async def call_api(session: CommandSession, text: str) -> Optional[str]:
    url = f"https://ai-backend.binwang.me/chat/couplet/{quote(text, 'utf-8')}"
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

    logger.debug(f"Start getting {url} ...")
    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(url, timeout=20, proxy=get_local_proxy(), headers=headers) as response:

                if response.status != 200:
                    logger.error(f"Cannot connect to {url}, Status: {response.status}")
                    await session.send("无法连接到服务器")
                    return None

                r = await response.json()
                logger.debug(f"Response: {r}")
                return r['output']

    except asyncio.TimeoutError:
        logger.error(f"Cannot connect to {url}, Error: Timeout")
        await session.send("请求超时")
