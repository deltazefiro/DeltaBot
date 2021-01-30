import json
import string
import random
import aiohttp
from typing import Optional
from nonebot import CommandSession

from loguru import logger


async def generate_trap_url(session: CommandSession, jump_url: str = 'www.baidu.com') -> (Optional[str], Optional[str]):
    """Generate a trap url for stealing the user's ip
    Trap url provided by https://met.red/

    Args:
        session (CommandSession): Current session
        jump_url (str): The url jump to after getting ip

    Returns:
        trap_url & key

    """
    url = "https://met.red/api/h/location/saveMyUrl"
    letters = string.ascii_lowercase
    key = ''.join(random.choice(letters) for _ in range(10))
    data = {'key': key, 'jumpUrl': jump_url, 'token': ''}

    async with aiohttp.ClientSession() as sess:
        async with sess.post(url, data=data) as response:

            if response.status != 200:
                logger.error("无法连接到 'https://met.red/api/h/location/saveMyUrl', "
                             "错误状态: [%s]"%response.status)
                await session.send("无法连接到陷阱api")
                return None

            r = json.loads(await response.text())

            try:
                if r['code'] == 0:
                    logger.info("生成陷阱URL成功: %s" %([r['url'], key]))
                    return r['url'], key
                elif r['code'] == 1 and r['msg'] == 'key已被使用':
                    logger.warning("秘钥已被使用，请重新申请秘钥")
                else:
                    logger.error("未知的错误: %s" %r)
                    await session.send("陷阱api返回未知错误")
            except (KeyError, IndexError):
                logger.error("未知的错误: %s" %r)
                await session.send("陷阱api返回未知错误")
                return None

    # Regenerate key and retry
    return generate_trap_url(session, jump_url)


async def get_ip_from_trap(session: CommandSession, key: str) -> (Optional[str], Optional[str]):
    """Get the user's ip from trap api.
    Trap url provided by https://met.red/

    Args:
        session (CommandSession): Current session
        key (str): trap key

    Returns:
        User's ip & address
    """
    url = "https://met.red/api/h/location/getKeyIpList"
    data = {'key': key}

    async with aiohttp.ClientSession() as sess:
        async with sess.post(url, data=data) as response:

            if response.status != 200:
                logger.error("无法连接到  'https://met.red/api/h/location/getKeyIpList', "
                             "错误状态: [%s]"%response.status)
                await session.send("无法连接到陷阱api")
                return None

            r = json.loads(await response.text())

            try:
                if r['code'] == 0:
                    if r['data']:
                        d = r['data'][0]
                        logger.info("成功读取到网际协议地址 %s" % ([d['ip'], d['address']]))
                        return d['ip'], d['address']
                    else:
                        logger.warning(f"陷阱 '{key}' 还没有被访问")
                        await session.send("陷阱网站还没被访问！请等访问后再试")
                        return None
                elif r['code'] == 1 and r['msg'] == 'key不存在,请去创建':
                    logger.warning(f"秘钥 '{key}' 不存在.")
                    await session.send("Key不存在！请先创建")
                else:
                    logger.error("陷阱接口返回未知错误: %s" %r)
                    await session.send("陷阱api返回未知错误")
            except (KeyError, IndexError):
                logger.error("陷阱接口范围未知错误: %s" %r)
                await session.send("陷阱api返回未知错误")
                return None
