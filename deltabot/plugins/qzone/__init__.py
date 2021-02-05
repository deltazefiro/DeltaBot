from loguru import logger
from nonebot import on_command, CommandSession, permission, get_bot
from .check_content import *
import os

# Check dependencies
__enabled__ = True
try:
    from .qzone_api import *
except ImportError:
    logger.warning("Qzone simulate-login dependencies not satisfied. Disabled 'qzone' plugin. See https://233a344a455.github.io/DeltaBot/setup.html#qzone%E6%A8%A1%E5%9D%97-%E5%8C%BF%E5%90%8D%E5%A2%99%E5%8A%9F%E8%83%BD-%E5%AE%89%E8%A3%85")
    __enabled__ = False

if not os.path.exists(get_bot().config.CHROME_DRIVER_PATH):
    logger.warning("Chrome Driver not found! Disabled 'qzone' plugin. See https://233a344a455.github.io/DeltaBot/setup.html#qzone%E6%A8%A1%E5%9D%97-%E5%8C%BF%E5%90%8D%E5%A2%99%E5%8A%9F%E8%83%BD-%E5%AE%89%E8%A3%85")
    __enabled__ = False


__plugin_name__ = 'qzone(空间匿名墙)'
__plugin_usage__ = r"""
将消息发送到机器人的空间动态

Command(s):
    - /announce [内容]
      在空间发布公告
      【需管理员权限】
      
    - /anonymous [内容]
      在空间发布匿名内容【匿名墙】
      【禁止发布违规内容！】
""".strip()


@on_command('announce', aliases=('qzone_announce', 'notice'), permission=permission.SUPERUSER)
async def announce(session: CommandSession):

    if not __enabled__:
        logger.warning("Dependencies are not satisfied. Plugin is disabled. See https://233a344a455.github.io/DeltaBot/setup.html#qzone%E6%A8%A1%E5%9D%97-%E5%8C%BF%E5%90%8D%E5%A2%99%E5%8A%9F%E8%83%BD-%E5%AE%89%E8%A3%85")
        await session.send("插件未启用！")
        return

    content = "【公告】\n" + session.get('content', prompt="请输入发送的内容(使用'/kill'取消)")
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
        await session.pause("请输入发送的内容(使用'/kill'取消)")
    session.state[session.current_key] = stripped_arg


@on_command('anonymous', aliases=('anony', 'anonymous_board'))
async def anonymous_board(session: CommandSession):

    if not __enabled__:
        logger.warning("Dependencies are not satisfied / ChromeDriver not found. Plugin is disabled.")
        await session.send("插件未启用！")
        return

    c = session.get('content', prompt="请输入发送的内容(使用'/kill'取消)")

    if get_bot().config.CHECK_ILLEGAL_INFO:
        if not await check_content(session, c):
            return

    content = "【匿名内容】\n" \
              "=============================\n" +\
              c +\
              "\n=============================\n" \
              "以上内容由匿名用户发布，管理员对本动态不负任何责任\n" \
              "如果其中包含违规内容，请及时联系管理员"

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
        await session.pause("请输入发送的内容(使用'/kill'取消)")
    session.state[session.current_key] = stripped_arg
