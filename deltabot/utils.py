from urllib.request import getproxies
from nonebot import message

def get_local_proxy():
    try:
        return getproxies()['http']
    except KeyError:
        return None

def get_xml_segment(data: str) -> message.MessageSegment:
    return message.MessageSegment(type_='xml', data={'data': str(data)})