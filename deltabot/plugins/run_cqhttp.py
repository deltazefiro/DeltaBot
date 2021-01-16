import os
import re
import subprocess
import threading

from loguru import logger
from nonebot import on_startup

from .. import config

__plugin_name__ = '[I]run_cqhttp'
__plugin_usage__ = r"""
[Internal plugin]
Configure and start go_cqhttp on setup.
Please DO NOT call the plugin *manually*.
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
            r = re.search(r'\[.*]:', l).span()
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
        logger.info("Generate go-cqhttp config successfully.")

    if not config.AUTO_START_GO_CQHTTP:
        logger.warning("Auto-start go-cqhttp is disabled. Please start go-cqhttp manually on port.")
        return

    # Check is go-cqhttp executable
    if not os.access('cqhttp/go-cqhttp', os.X_OK):
        mode = os.stat('cqhttp/go-cqhttp').st_mode | 0o100
        logger.warning("go-cqhttp is not executable! Sudo authority required to set permissions.")
        os.chmod('cqhttp/go-cqhttp', mode)
        logger.info("Set permissions successful. Sudo authority will not required on next running.")

    logger.info("Start go-cqhttp!")
    cqhttp_process = subprocess.Popen(['cd cqhttp;./go-cqhttp faststart'], shell=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)

    cqhttp_log_thread = threading.Thread(target=log_cqhttp, args=[cqhttp_process], daemon=True)
    cqhttp_log_thread.start()

    return
