from nonebot import on_command, CommandSession, message, permission
from .qzone_api import *

__plugin_name__ = 'qzone'
__plugin_usage__ = r"""
将消息发送到机器人的空间动态
Command(s):
    - /announce [内容]
      在空间发布公告，需管理员权限
      *Required admin permission*
      
    - /anonymous [内容]
      在空间发布匿名内容【匿名墙】
      **禁止发布敏感内容！**
""".strip()


@on_command('announce', aliases=('qzone_announce', 'notice'), permission=permission.SUPERUSER)
async def announce(session: CommandSession):
    content = "【公告】\n" + session.get('content', prompt="请输入发送的内容")
    ret = await post_emotion(session, content)
    if ret:
        await session.send("发送成功！")

@announce.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['content'] = stripped_arg
        return

    if not stripped_arg:
        await session.pause("请输入发送的内容")
    session.state[session.current_key] = stripped_arg


@on_command('anonymous', aliases=('anony', 'anonymous_board'))
async def anonymous_board(session: CommandSession):
    content = "【匿名内容】" \
              "\n\n=============================\n" + \
              session.get('content', prompt="请输入发送的内容") + \
              "\n\n=============================\n" \
              "本动态由匿名用户发布，管理员对本动态不负任何责任\n" \
              "如果其中包含敏感内容，请及时联系管理员"
    ret = await post_emotion(session, content)
    if ret:
        await session.send("发送成功！")

@anonymous_board.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['content'] = stripped_arg
        return

    if not stripped_arg:
        await session.pause("请输入发送的内容")
    session.state[session.current_key] = stripped_arg
