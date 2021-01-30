import json
import random
import string
import time
from urllib.parse import quote_plus
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
        sign += f'{key}={quote_plus(str(value))}&'
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

                logger.debug(f"发送数据到接口: {data}")

                if response.status != 200:
                    logger.error(f"无法连接到 {url}, 状态: {response.status}")
                    await session.send("对话api调用发生错误 :(")
                    return None

                r = json.loads(await response.text())
                logger.debug(f"接口返回为: {r}")

                if not r['ret']:
                    return r['data']['answer']
                elif r['msg'] == 'chat answer not found':
                    logger.debug("没有找到答案，使用不理解的回答")
                    return render_expression(config.EXPR_DONT_UNDERSTAND)
                elif r['msg'] == 'app_id not found' or r['msg'] == 'app_key not found':
                    logger.warning("对话接口错误 / 空缺。请在config.py中填写以启用自然语言处理人工智能分支会话功能")
                    await session.send("对话api配置错误！请联系管理员")
                    return None
                else:
                    logger.error(f"接口返回的错误的信息: {r['msg']}")
                    await session.send("对话api调用发生错误 :(")
                    return None

    except (aiohttp.ClientError, json.JSONDecodeError, KeyError) as e:
        logger.error(f"调用接口时被占用 : {e}")#An error occupied when calling api
        await session.send("对话api调用发生错误 :(")
        return None