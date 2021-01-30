import os
import re
import subprocess
import sys
import threading

from loguru import logger
from nonebot import on_startup

from .. import config

__plugin_name__ = '[I]run_cqhttp'
__plugin_usage__ = r"""
[内部插件]
在安装时配置并启动go_cqhttp。
请不要手动调用插件。
""".strip()

def _configure_cqhttp():
    with open('cqhttp/config_template.hjson', 'r') as f:
        cq_config = f.read()

    cq_config = cq_config.replace('[uin]', str(config.UIN))
    cq_config = cq_config.replace('[password]', str(config.PASSWORD))
    cq_config = cq_config.replace('[port]', str(config.PORT))

    with open('cqhttp/config.hjson', 'w') as f:
        f.write(cq_config)

def log_cqhttp(cqhttp_process):
    with cqhttp_process.stdout:
        for line in iter(cqhttp_process.stdout.readline, b''):  # b'\n'-separated lines
            l = line.decode('utf-8').strip()[22:]
            match = re.search(r'\[.*]:', l)
            if not match:
                continue #防止多行信息报错
            r = match.span()
            level, content = l[r[0]+1:r[1]-2], l[r[1]+1:]
            if level == 'INFO':
                logger.info(content)
            elif level == 'WARNING':
                logger.warning(content)
            elif level == 'FAULT':
                logger.critical(content)
            elif level == 'DEBUG':
                logger.debug(content)
            else:
                logger.error(content)


@on_startup
async def run_cqhttp():

    if config.AUTO_CONFIGURE_GO_CQHTTP:
        _configure_cqhttp()
        logger.info("生成go-cqhttp配置成功。")

    if not config.AUTO_START_GO_CQHTTP:
        logger.warning(f"禁用了go-cqhttp的自动启动。请在 {config.PORT} 端口上手动运行go-cqhttp.")
        return

    if sys.platform == 'linux':
        command = ['./go-cqhttp', 'faststart']

        # Check is go-cqhttp executable
        if not os.access('cqhttp/go-cqhttp', os.X_OK):
            mode = os.stat('cqhttp/go-cqhttp').st_mode | 0o100
            logger.warning("go-cqhttp不可执行!设置权限所需的Sudo权限。go-cqhttp is not executable! Sudo authority required to set permissions.")
            os.chmod('cqhttp/go-cqhttp', mode)
            logger.info("设置权限成功。Sudo权限将不需要在下一次运行。Set permissions successful. Sudo authority will not required on next running.")

    elif sys.platform == 'win32':
        command = ['./go-cqhttp.exe', 'faststart']
    else:
        logger.critical(f"不受支持的平台!请在 {config.PORT}端口上手动运行go-cqhttp.")
        return

    logger.info("启动go-cqhttp!")
    cqhttp_process = subprocess.Popen(command, cwd='cqhttp',
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)

    cqhttp_log_thread = threading.Thread(target=log_cqhttp, args=[cqhttp_process], daemon=True)
    cqhttp_log_thread.start()

    return
