from nonebot import on_command, CommandSession
from .data_source import *

from aiocqhttp.message import escape

from ...utils import get_xml_segment

__plugin_name__ = 'getip'
__plugin_usage__ = r"""
使用音乐卡片陷阱获取他人ip
陷阱后端由https://met.red/提供
【目前陷阱音乐使用的歌曲暂时硬编码为「逍遥游 by littlealone100」，暂不支持自定义歌曲】
Usage:
    1. 使用命令 '/gettrap' 生成一个含有陷阱的音乐卡片（同时生成一个key）
    2. 将陷阱音乐卡片【转发】给你想获取ip的用户
    3. 当此用户进入听过此音乐后, 你可以通过 '/getip' 并输入key获取此用户的ip
    
Command(s):
 - /gettrap
    生成陷阱音乐卡片
    
 - /getip [key]
    获取用户ip
    请确保陷阱网址【已被访问】
""".strip()


TRAP_XML_CODE = """
<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<msg serviceID="2" templateID="1" action="web" brief="&amp;#91;分享&amp;#93; 逍遥游" sourceMsgId="0"
    url="[trap_url]" flag="0" adverSign="0" multiMsgFlag="0">
    <item layout="2"><audio cover="http://p2.music.126.net/KSACgVt3XlsL3nR815OGQw==/109951164820754474.jpg"
            src="" />
        <title>逍遥游</title>
        <summary>littlealone100</summary>
    </item>
    <source name="网易云音乐" icon="https://i.gtimg.cn/open/app_icon/00/49/50/85/100495085_100_m.png?date=20210109"
        url="http://web.p.qq.com/qqmpmobile/aio/app.html?id=100495085" action="app"
        a_actionData="com.netease.cloudmusic" i_actionData="tencent100495085://" appid="100495085" />
</msg>
""".strip()


@on_command('gettrap', aliases=('get_trap', 'generate_trap', 'generate_trap_url'))
async def get_trap(session: CommandSession):
    ret = await generate_trap_url(session, 'music.163.com/song/532522915')
    if ret:
        await session.send("请保存好key，并将音乐卡片转发给想获取ip的用户【请勿自己点击】，待用户点开音乐后使用'/getip'查询结果")
        await session.send(f"查询key: {ret[1]}")
        await session.send(get_xml_segment(escape(TRAP_XML_CODE.replace('[trap_url]', ret[0]))))



@on_command('getip', aliases=('get_ip', 'get_ip_from_trap'))
async def get_trap(session: CommandSession):
    key = session.get('key', prompt="请输入陷阱网址的key")
    ret = await get_ip_from_trap(session, key)

    if ret:
        await session.send("IP: %s\n大致位置: %s" %(ret[0], ret[1] if ret[1] else '未知'))

@get_trap.args_parser
async def _(session: CommandSession):
    arg = session.current_arg

    if session.is_first_run:
        if arg:
            session.state['key'] = arg
        return

    if not arg:
        session.pause('请输入陷阱网址的key')

    session.state[session.current_key] = arg