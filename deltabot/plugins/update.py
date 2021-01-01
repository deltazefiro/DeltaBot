from nonebot import CommandSession, on_command, permission
from aiocqhttp.message import escape
from loguru import logger
from subprocess import PIPE, STDOUT, CalledProcessError
import subprocess

__plugin_name__ = '[E][A]update'
__plugin_usage__ = r"""
从Git上更新DeltaBot
仅对使用克隆获取仓库有效
【实验性功能，可能意外损坏DeltaBot，请谨慎使用】
【需要管理员权限】
""".strip()

@on_command('update', permission=permission.SUPERUSER)
async def update(session: CommandSession):
    ret = session.get('continue', prompt="这是一个实验性功能，可能导致机器人损坏，是否继续？[y/n]")
    if ret != 'y':
        await session.send("已取消")
        return

    logger.warning("Start pulling from git ...")
    await session.send("Start pulling from git ...")
    try:
        process = subprocess.run(['git', 'pull'], stdout=PIPE, stderr=STDOUT)

        logger.info(process.stdout.decode('utf-8').strip())
        await session.send(escape(process.stdout.decode('utf-8').strip()))

    except CalledProcessError as e:
        logger.error(f"Fail to update: {e}")
        await session.send(escape("Fail to update: {e}"))