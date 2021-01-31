import itertools
import re

from loguru import logger
from nonebot import CommandSession

from ...utils import get_baidu_ai_token, simple_post


async def check_content(session: CommandSession, text: str):
    logger.debug(f"Start to check content: {text}")
    url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"
    token = await get_baidu_ai_token(session)
    if not token:
        return
    data = {'access_token': token, 'text': text}
    r = await simple_post(session, url, data)
    if not r:
        return
    if 'error_code' in r:
        if r['error_code'] in (100, 110, 111):
            logger.warning("BaiduAI token expired / invalid! Trying to reacquire ...")
            await get_baidu_ai_token(session, force=True)
            return await check_content(session, text)
        elif r['error_code'] == 6:
            logger.error("No permission to access API. "
                         "Please make sure '内容审核-文本' function is enabled for your APP in BaiduAI Console.")
            await session.send('功能未启用！')
        else:
            logger.error(f"Error from API: [Error{r['error_code']}]{r['error_msg']}")
            await session.send('内容审核服务器错误！')
        return

    if r['conclusionType'] == 1:
        logger.debug("No illegal content found.")
        return True

    if r['conclusionType'] == 2 or 3:
        # TODO: 允许审核结果为'疑似'发送，但警告并记录其发送者
        reason = [(re.search(r'存在(.*?)不合规', l['msg']).group(1), list(itertools.chain(*[h['words'] for h in l['hits']])))
                  for l in r['data']]
        logger.warning(f"{session.event['sender']['nickname']}({session.event['user_id']}) "
                       f"tried sending an anonymous post with illegal content: {reason}")
        await session.send("内容违规！原因: 消息内容包含 " + '、'.join([l[0] for l in reason]))
        return

    else:
        logger.error("Server failed to check info.")
        await session.send("内容审核服务器错误！")
        return