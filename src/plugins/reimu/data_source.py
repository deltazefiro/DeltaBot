"""Modified from https://github.com/Angel-Hair/XUN_Bot/"""

import requests
from lxml import etree
import time

MAXINFO_REIMU = 5

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


async def get_search_result(key_word: str) -> list or None:
    html_data = requests.get('https://blog.reimu.net/search/' + key_word)
    html = etree.HTML(html_data.text)

    fund_l = html.xpath('//h1[@class="page-title"]/text()')
    if fund_l:
        fund = fund_l[0]
        if fund == "未找到":
            return None

    headers = html.xpath('//article/header/h2/a/text()')
    urls = html.xpath('//article/header/h2/a/@href')
    print("Now get {} post from search page".format(len(headers)))

    processed_headers = []
    processed_urls = []
    for i, header in enumerate(headers):
        if check_not_excluded(header) and header != "审核结果存档":
            processed_headers.append(headers[i])
            processed_urls.append(urls[i])
        else:
            print("This title {} does not meet the requirements".format(header))

    n_posts = len(processed_headers)
    print("Get {} post after processing".format(n_posts))

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


async def get_download_links(url) -> str:
    ret = ""

    print("Now starting get the {}".format(url))
    html_data = requests.get(url)
    html = etree.HTML(html_data.text)

    pres = html.xpath('//div[@class="entry-content"]/pre/text()')
    a_texts = html.xpath('//div[@class="entry-content"]/pre//a/text()')
    a_hrefs = html.xpath('//div[@class="entry-content"]/pre//a/@href')

    if pres:
        # while "" in pres:
        #     pres.remove("")

        ret = pres[0].strip()

        if a_hrefs:
            for i, (a_t_s, a_h_s) in enumerate(zip(a_texts, a_hrefs)):
                a = "\n {}  {}  {} ".format(a_t_s, a_h_s, pres[i + 1].strip())
                ret += a
    else:
        print("Failed to get download link from {}".format(url))

    return ret


def check_not_excluded(header: str) -> bool:
    exclude = ['音乐', '御所动态']
    for ex in exclude:
        if ex in header:
            return False
    return True
