from nonebot import CommandSession, on_command, permission
from aiocqhttp.message import escape
from loguru import logger
from subprocess import PIPE, STDOUT, CalledProcessError
import subprocess

__plugin_name__ = '[A]update'
__plugin_usage__ = r"""
从Git上更新DeltaBot
【实验性功能，可能意外损坏DeltaBot，请谨慎使用】
【需要管理员权限】
""".strip()

@on_command('update', permission=permission.SUPERUSER)
async def update(session: CommandSession):
    logger.warning("Start pulling from git")
    await session.send("Start pulling from git")
    try:
        process = subprocess.run(['git', 'pull'], stdout=PIPE, stderr=STDOUT)

        logger.info(process.stdout.decode('utf-8').strip())
        await session.send(escape(process.stdout.decode('utf-8').strip()))

    except CalledProcessError as e:
        logger.error(f"Fail to update: {e}")
        await session.send(escape("Fail to update: {e}"))