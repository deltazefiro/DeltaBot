from typing import Optional


# get_relative_path = lambda p: os.path.join(os.path.dirname(__file__), p)
import nonebot
from loguru import logger
from nonebot.session import BaseSession


def get_local_proxy():
    from urllib.request import getproxies
    try:
        return getproxies()['http']
    except KeyError:
        return None


def get_xml_segment(data: str):
    from nonebot import message
    return message.MessageSegment(type_='xml', data={'data': str(data)})


def get_cardimage_segment(file: str, maxheight: int = 500, maxwidth: int = 500, minheight: int = 40,
                          minwidth: int = 40, source: str = None):
    from nonebot import message
    if source:
        return message.MessageSegment(type_='cardimage',
                                      data={'file': file, 'maxheight': maxheight, 'maxwidth': maxwidth,
                                            'minheight': minheight, 'minwidth': minwidth,
                                            'source': source})
    else:
        return message.MessageSegment(type_='cardimage',
                                      data={'file': file, 'maxheight': maxheight, 'maxwidth': maxwidth,
                                            'minheight': minheight, 'minwidth': minwidth})


def download_file(url: str, download_path: str):
    import requests, sys, os
    with open(download_path + '.dl', 'wb') as f:
        response = requests.get(url, stream=True)
        total = int(response.headers.get('content-length'))

        downloaded = 0

        for data in response.iter_content(chunk_size=1024 * 10):
            downloaded += len(data)
            f.write(data)

            done = int(30 * downloaded / total)
            sys.stdout.write("\rDownloading %.2fM / %.2fM " % (downloaded / 1024 ** 2, total / 1024 ** 2) + \
                             f"[{'█' * done}{'.' * (30 - done)}]")
            sys.stdout.flush()

    sys.stdout.write('\n')
    os.rename(download_path + '.dl', download_path)


async def simple_post(session, url: str, data: dict, timeout: int = 10) -> Optional[dict]:
    """
    A simple post function with exception feedback
    Args:
        session (CommandSession): current session
        url (str): post url
        data (dict): post data
        timeout (int): timeout threshold

    Returns:
        Json response in dict if no exception occurred
        Otherwise, return None and send feedback to user.
    """
    import json
    import aiohttp
    import asyncio
    from loguru import logger

    try:
        logger.debug(f"Start posting {data} to {url} ...")
        async with aiohttp.ClientSession() as client:
            async with client.post(url, data=data, timeout=timeout, proxy=get_local_proxy()) as response:
                if response.status != 200:
                    logger.error(f"Cannot connect to {url}, Status: {response.status}")
                    session.send("无法连接到服务器")
                    return None

                r = json.loads(await response.text())
                logger.debug(f"Response: {r}")
                return r

    except asyncio.TimeoutError:
        logger.error(f"Cannot connect to {url}, Error: Timeout")
        await session.send("请求超时")


_baidu_ai_token = None


async def get_baidu_ai_token(session, force: bool = False) -> Optional[str]:
    """
    Get BaiduAI token.
    Args:
        session (CommandSession): current session
        force (bool): ignore existing token, reacquire a new one

    Returns:
        token in str, None if failed.
    """
    from loguru import logger
    from nonebot import get_bot

    global _baidu_ai_token

    if not force and _baidu_ai_token:
        return _baidu_ai_token

    logger.debug("Start to get BaiduAI token ...")
    config = get_bot().config
    ak, sk = config.BAIDU_API_KEY, config.BAIDU_SECRET_KEY
    if not (ak and sk):
        logger.error(
            "BAIDU_API_KEY / BAIDU_SECRET_KEY unfilled! Please fill them in config to enable illegal-info check.")
        session.send("功能未启用！")
        return
    d = {'grant_type': 'client_credentials', 'client_id': ak, 'client_secret': sk}
    r = await simple_post(session, 'https://aip.baidubce.com/oauth/2.0/token', d)
    if not r:
        return

    if 'error' in r:
        if r['error'] == 'invalid_client':
            logger.error("Invalid BAIDU_API_KEY / BAIDU_SECRET_KEY!")
        else:
            logger.error("Unknown error occurred when getting token.")
        session.send("功能未启用！")
        return

    _baidu_ai_token = r['access_token']
    return _baidu_ai_token


async def get_stranger_nickname(session: BaseSession, user_id: int) -> Optional[str]:
    try:
        ret = await session.bot.call_action(action='get_stranger_info', user_id=user_id)
        return ret['nickname']
    except nonebot.exceptions.CQHttpError:
        return None

async def get_group_name(session: BaseSession, group_id: int) -> Optional[str]:
    try:
        ret = await session.bot.call_action(action='get_group_info', group_id=group_id)
        return ret['group_name']
    except nonebot.exceptions.CQHttpError:
        return ''
