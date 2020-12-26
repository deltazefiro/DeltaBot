import aiohttp
from nonebot import get_bot, CommandSession
from typing import Optional

from loguru import logger

def _get_g_tk(cookie: str) -> int:
    cookie = dict(map(lambda s: s.partition('=')[::2], cookie.split('; ')))
    h = 5381
    s = cookie.get('p_skey', None) or cookie.get('skey', None) or ''
    for c in s:
        h += (h << 5) + ord(c)

    return h & 0x7fffffff


async def post_emotion(session: CommandSession, content: str) -> Optional[bool]:
    """
    Post a Qzone emotion.
    Args:
        session (CommandSession): Current session
        content (str): Emotion content

    Returns:
        Bool, is successful or not

    """
    config = get_bot().config
    uin = config.UIN
    cookie = config.QZONE_COOKIE

    if not (cookie and uin):
        logger.waring("Qzone cookie / uin is empty. Please fill them in config.py to enable qzone function.")
        await session.send("插件未启用，请联系管理员")
        return False

    url = "https://user.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_publish_v6" \
          f"?&g_tk={_get_g_tk(cookie)}"

    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "cookie": cookie
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

    # logger.warn(f"\n\n{url}\n{headers}\n{data}\n")

    async with aiohttp.ClientSession() as sess:
        async with sess.post(url, headers=headers, data=data) as response:

            if response.status != 200:
                logger.error("Cannot connect to Qzone, "
                             "Status: [%s]"%response.status)
                await session.send("无法连接到QQ空间，请稍后重试")
                return False

            resp = str(await response.text())
            if not resp:
                logger.error("Got an empty resp from Qzone. Please make sure uid&cookie is invalid.")
                await session.send("未知错误，请等待管理员更新")
                return False
            elif '4001' in resp:
                logger.error("Qzone cookie expired! Please update it.")
                await session.send("QQ空间cookie已过期，请等待管理员更新")
                return False

            return True
