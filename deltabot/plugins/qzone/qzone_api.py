import os
import pickle
import threading
from typing import Optional

import aiohttp
from loguru import logger
from nonebot import CommandSession, get_bot

from . import sim_login

config = get_bot().config

get_relative_path = lambda p: os.path.join(os.path.dirname(__file__), p)
_login_thread_lock: Optional[threading.Lock] = None


async def _get_login_token(session: CommandSession, force: bool = False) -> Optional[tuple]:
    """
    Get Qzone login token (cookies & g_tk)
    Args:
        session (CommandSession): Current session
        force (bool): Force to re-login, ignoring saved token
    Returns:
        if saved token exist, return Qzone cookies(str) & g_tk
        Otherwise, return None
    """
    global _login_thread_lock
    if _login_thread_lock is not None and _login_thread_lock.locked():
        await session.send("正在自动获取空间登录令牌，请稍等片刻后再试！")
        return None

    if not force:
        try:
            with open(get_relative_path('./data/cookies.pkl'), 'rb') as f:
                cookies, g_tk = pickle.load(f)
            return cookies, g_tk
        except (FileNotFoundError, ValueError):
            logger.warning("Qzone login token is not exist. Start simulate-login to get it.")
            await session.send("空间登录令牌不存在，开始自动获取，请稍等片刻后再使用此功能！")

    if _login_thread_lock is None:
        _login_thread_lock = threading.Lock()
    t = threading.Thread(target=sim_login.run, args=[_login_thread_lock], daemon=True)
    t.start()
    return None


async def post_emotion(session: CommandSession, content: str) -> Optional[bool]:
    """
    Post a Qzone emotion.
    Args:
        session (CommandSession): Current session
        content (str): Emotion content

    Returns:
        Bool, is successful or not

    """

    uin = config.UIN
    ret = await _get_login_token(session)
    if not ret:
        return False
    cookies, g_tk = ret


    url = "https://user.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_publish_v6" \
          f"?&g_tk={g_tk}"

    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "cookie": cookies
    }

    data = {
        "syn_tweet_verson": "1",
        "paramstr": "1",
        "con": str(content),
        "feedversion": "1",
        "ver": "1",
        "ugc_right": "1",
        "to_sign": "0",
        "hostuin": str(uin),
        "code_version": "1",
        "format": "fs",
        "qzreferrer": f"https://user.qzone.qq.com/{uin}/"
    }


    async with aiohttp.ClientSession() as sess:
        async with sess.post(url, headers=headers, data=data) as response:

            if response.status != 200:
                logger.error("Cannot connect to Qzone, "
                             "Status: [%s]"%response.status)
                await session.send("无法连接到QQ空间，请稍后重试")
                return False

            resp = str(await response.text())
            if not resp:
                logger.error("Got an empty resp from Qzone.")
                await session.send("未知错误，请等待管理员更新")
                return False
            elif '4001' in resp:
                logger.warning("Qzone cookie expired! Start simulate login to get cookie.")
                await session.send("QQ空间cookie已过期! 已开始自动获取，请稍待片刻再使用此功能")
                await _get_login_token(session, force=True)
                return False

            return True
