from nonebot import on_command, CommandSession
from .data_source import get_hitokoto

__plugin_name__ = 'hitokoto'
__plugin_usage__ = r"""
获取「一言」(每日一句)
数据来源 hitokoto.cn
Command(s):
 - /hitokoto
""".strip()

@on_command('hitokoto', aliases=('每日一句'))
async def hitokoto(session: CommandSession):
    ret = await get_hitokoto(session)
    if ret:
        await session.send(f"『{ret[0]}』\n" +
                           f"——{ret[1] if ret[1] else ''}「{ret[2]}」".rjust(12, '　'))
                            # 使用'&#12288'字符进行右对齐，防止QQ将普通空格渲染过小