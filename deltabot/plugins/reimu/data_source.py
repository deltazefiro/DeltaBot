"""Modified from https://github.com/Angel-Hair/XUN_Bot/"""
import asyncio
from typing import Optional

import aiohttp
from loguru import logger
from lxml import etree
from nonebot import CommandSession

from ...utils import get_local_proxy


# MAXINFO_REIMU = 5
#
# async def from_reimu_get_info(key_word: str) -> str or None:
#     repass = ""
#     url = 'https://blog.reimu.net/search/' + key_word
#     url_s = 'https://blog.reimu.net/'
#
#     if key_word == "最近的存档":
#         print("Now starting get the {}".format(url_s))
#         repass = await get_search_result(url_s)
#     else:
#         print("Now starting get the {}".format(url))
#         repass = await get_search_result(url)
#
#     return repass


async def get_search_result(session: CommandSession, key_word: str) -> Optional[list]:
    if key_word in ('latest', 'l'):
        url = 'https://blog.reimu.net/'
    else:
        url = 'https://blog.reimu.net/search/' + key_word

    logger.debug(f"Start getting {url} ...")
    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(url, timeout=10, proxy=get_local_proxy()) as response:

                if response.status != 200:
                    logger.error("Cannot connect to https://blog.reimu.net/, "
                                 "Status: [%s]"%response.status)
                    await session.send("无法连接到搜索服务器")
                    return None

                r = await response.text()
    except asyncio.TimeoutError:
        logger.error("Connect to https://blog.reimu.net/ timeout. Please add '104.28.28.43 blog.reimu.net' in host file to access it.")
        await session.send("请求超时")
        return None

    html = etree.HTML(r)

    fund_l = html.xpath('//h1[@class="page-title"]/text()')
    if fund_l:
        fund = fund_l[0]
        if fund == "未找到":
            logger.debug("No search results are found.")
            await session.send("无搜索结果，试试换个关键词？")
            return None

    headers = html.xpath('//article/header/h2/a/text()')
    urls = html.xpath('//article/header/h2/a/@href')
    logger.debug("Now get {} post from search page".format(len(headers)))

    processed_headers = []
    processed_urls = []
    for i, header in enumerate(headers):
        if  '审核' not in header and header not in ('御所动态', '音乐'):
            processed_headers.append(headers[i])
            processed_urls.append(urls[i])
        else:
            logger.debug("This title {} does not meet the requirements".format(header))

    n_posts = len(processed_headers)
    logger.debug("Get {} post after processing".format(n_posts))

    return list(zip(processed_headers, processed_urls))


    # if n_posts > MAXINFO_REIMU:
    #     processed_headers = processed_headers[:MAXINFO_REIMU]
    #     processed_urls = processed_urls[:MAXINFO_REIMU]
    #
    # for header, url in zip(processed_headers, processed_urls):
    #     time.sleep(0.1)
    #     download_link = await get_download_links(header, url)
    #     if download_link:
    #         if ret:
    #             ret += "\n\n- - - - - - - - \n\n" + download_link
    #         else:
    #             ret = download_link
    #
    # if ret:
    #     ret = info + ret
    # return ret


async def get_download_links(session: CommandSession, url: str) -> Optional[str]:
    ret = ""
    logger.debug("Start sniffing download links form {}".format(url))

    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(url, timeout=10, proxy=get_local_proxy()) as response:

                if response.status != 200:
                    logger.error("Cannot connect to https://blog.reimu.net/"
                                 "Status: [%s]"%response.status)
                    await session.send("无法连接到资源服务器")
                    return None

                r = await response.text()
    except asyncio.TimeoutError:
        logger.error("Connect to https://blog.reimu.net/ timeout. Please add '104.28.28.43 blog.reimu.net' in host file to access it.")
        await session.send("请求超时")
        return None

    html = etree.HTML(r)

    pres = html.xpath('//div[@class="entry-content"]/pre/text()')
    a_texts = html.xpath('//div[@class="entry-content"]/pre//a/text()')
    a_hrefs = html.xpath('//div[@class="entry-content"]/pre//a/@href')

    if pres:
        ret = pres[0].strip()

        if a_hrefs:
            for i, (a_t_s, a_h_s) in enumerate(zip(a_texts, a_hrefs)):
                a = "\n {}  {}  {} ".format(a_t_s, a_h_s, pres[i + 1].strip())
                ret += a
    else:
        logger.debug("No download links are found in {}".format(url))

    return ret