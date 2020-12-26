import json
import random
import string
import time
from urllib.parse import quote
import hashlib
from typing import Optional
import aiohttp
from loguru import logger

import nonebot
from nonebot import CommandSession
from nonebot.helpers import context_id, render_expression




def get_req_sign(params: dict, app_key) -> str:
    """
    Calculate Tencent AI Open Platform's request sign
    Args:
        params (dict): Request data
        app_key (key): App key of API

    Returns:
        request sign
    """
    sign = ''
    for key,value in sorted(params.items()):
        sign += f'{key}={quote(str(value))}&'
    sign += f'app_key={app_key}'
    sign = hashlib.md5(sign.encode(encoding='UTF-8')).hexdigest().upper()
    return sign


async def call_NLP_api(session: CommandSession, text: str) -> Optional[str]:
    config = nonebot.get_bot().config
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"

    data = {
        'app_id': config.TENCENT_APP_ID,
        'session': context_id(session.ctx, mode='group', use_hash=True),
        'question': str(text),
        'time_stamp': int(time.time()),
        'nonce_str': ''.join(random.choice(string.ascii_lowercase) for _ in range(32))
    }

    data['sign'] = get_req_sign(data, config.TENCENT_APP_KEY)

    try:

        async with aiohttp.ClientSession() as sess:
            async with sess.post(url, data=data) as response:

                logger.debug(f"Send data to api: {data}")

                if response.status != 200:
                    logger.error(f"Cannot connect to {url}, Status: {response.status}")
                    await session.send("对话api调用发生错误 :(")
                    return None

                r = json.loads(await response.text())
                logger.debug(f"Response from API: {r}")

                if not r['ret']:
                    return r['data']['answer']
                elif r['msg'] == 'chat answer not found':
                    logger.debug("Chat answer not found. Render not understanding instead.")
                    return render_expression(config.EXPR_DONT_UNDERSTAND)
                elif r['msg'] == 'app_id not found' or r['msg'] == 'app_key not found':
                    logger.warning("API config invalid / unfilled. Please fill them in config.py to enable NL conversation function.")
                    await session.send("对话api配置错误！请联系管理员")
                    return None
                else:
                    logger.error(f"Error response from API: {r['msg']}")
                    await session.send("对话api调用发生错误 :(")
                    return None

    except (aiohttp.ClientError, json.JSONDecodeError, KeyError) as e:
        logger.error(f"An error occupied when calling api: {e}")
        await session.send("对话api调用发生错误 :(")
        return None