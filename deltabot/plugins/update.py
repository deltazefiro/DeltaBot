import subprocess
from subprocess import PIPE, STDOUT, CalledProcessError

from loguru import logger
from nonebot import CommandSession, on_command, permission

__plugin_name__ = '[E][A]update (热更新)'
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

    logger.warning("开始从git拉取...")
    await session.send("开始从git拉取 ...")
    try:
        output = subprocess.run(['git', 'pull'], stdout=PIPE, stderr=STDOUT).stdout.decode('utf-8').strip()
        logger.info(output)
        msg = output.replace('https://', '').replace('http://', '') # 防止QQ将链接渲染为卡片
        await session.send(msg.strip())

    except CalledProcessError as e:
        logger.error(f"更新失败: {e}")
        await session.send(f"更新失败: {e}")