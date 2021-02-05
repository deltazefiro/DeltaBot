import os
import re
import subprocess
import sys

from loguru import logger
from nonebot import on_startup

from .. import _version
from .. import config
from ..utils import download_file

__plugin_name__ = '[I]manage_cqhttp'
__plugin_usage__ = r"""
[Internal plugin]
Configure and start go_cqhttp on setup.
Please DO NOT call the plugin *manually*.
""".strip()

cqhttp_version = _version.__cqhttp_version__
pf = sys.platform


def _download_cqhttp():
    if pf == 'linux':
        url = f"https://github.com/Mrs4s/go-cqhttp/releases/download/{cqhttp_version}/go-cqhttp-{cqhttp_version}-linux-amd64"
        logger.info(f"Start downloading go-cqhttp from {url} ...")
        download_file(url, f'cqhttp/go-cqhttp-{cqhttp_version}-linux-amd64')
    elif pf == 'win32':
        url = f"https://github.com/Mrs4s/go-cqhttp/releases/download/{cqhttp_version}/go-cqhttp-{cqhttp_version}-windows-amd64.exe"
        logger.info(f"Start downloading go-cqhttp from {url} ...")
        download_file(url, f'cqhttp/go-cqhttp-{cqhttp_version}-windows-amd64.exe')

    logger.info("Downloaded go-cqhttp successfully.")

    for file_name in os.listdir('cqhttp/'):
        if file_name[:11] == 'go-cqhttp-v' and not f'go-cqhttp-{cqhttp_version}-' in file_name:
            os.remove(f'cqhttp/{file_name}')
    logger.info("Removed outdated go-cqhttp.")


def _configure_cqhttp():
    with open('cqhttp/config_template.hjson', 'r', encoding='utf-8') as f:
        cq_config = f.read()

    cq_config = cq_config.replace('[uin]', str(config.UIN))
    cq_config = cq_config.replace('[password]', str(config.PASSWORD))
    cq_config = cq_config.replace('[port]', str(config.PORT))

    with open('cqhttp/config.hjson', 'w') as f:
        f.write(cq_config)


def _get_cqhttp_file_name(match_version=True):
    if match_version:
        for file_name in os.listdir('cqhttp/'):
            if f'go-cqhttp-{cqhttp_version}' in file_name and file_name[0] != '_':
                return file_name
    else:
        for file_name in os.listdir('cqhttp/'):
            if file_name[:11] == 'go-cqhttp-v':
                return file_name
    return None


def _log_cqhttp(cqhttp_process):
    with cqhttp_process.stdout:
        for line in iter(cqhttp_process.stdout.readline, b''):  # b'\n'-separated lines
            l = line.decode('utf-8').strip()[22:]
            match = re.search(r'\[.*]:', l)
            if not match:
                continue  # 防止多行信息报错
            r = match.span()
            level, content = l[r[0] + 1:r[1] - 2], l[r[1] + 1:]
            if level == 'INFO':
                logger.info(content)
            elif level == 'WARNING':
                logger.warning(content)
            elif level == 'FAULT':
                logger.error(content)
            elif level == 'DEBUG':
                logger.debug(content)
            else:
                logger.error(content)


def _start_cqhttp(cqhttp_file_name):
    # Check is go-cqhttp executable
    if not os.access(f'cqhttp/{cqhttp_file_name}', os.X_OK):
        mode = os.stat(f'cqhttp/{cqhttp_file_name}').st_mode | 0o100
        logger.warning("go-cqhttp is not executable! Sudo authority required to set permissions.")
        os.chmod(f'cqhttp/{cqhttp_file_name}', mode)
        logger.info("Set permissions successful. Sudo authority will not required on next running.")

    logger.info("Start go-cqhttp!")
    subprocess.Popen([f'./{cqhttp_file_name}', 'faststart'], cwd='cqhttp')

    # # handle go-cqhttp output with loguru
    # cqhttp_process = subprocess.Popen([f'./{cqhttp_file_name}', 'faststart'], cwd='cqhttp',
    #                                   stdout=subprocess.PIPE,
    #                                   stderr=subprocess.STDOUT)
    #
    # cqhttp_log_thread = threading.Thread(target=_log_cqhttp, args=[cqhttp_process], daemon=True)
    # cqhttp_log_thread.start()


@on_startup
async def main():
    if pf not in ('win32', 'linux'):
        logger.error(f"Unsupported platform! Please download go-cqhttp https://github.com/Mrs4s/go-cqhttp/releases/ "
                     f"and run it manually on port {config.PORT}.")
        return

    if config.AUTO_CONFIGURE_GO_CQHTTP:
        _configure_cqhttp()
        logger.info("Generate go-cqhttp config successfully.")

    if not config.AUTO_START_GO_CQHTTP:
        logger.warning(f"Auto-start go-cqhttp is disabled. Please run go-cqhttp manually on port {config.PORT}.")
        return

    if config.AUTO_DOWNLOAD_GO_CQHTTP:
        if not _get_cqhttp_file_name():
            logger.warning("Go-cqhttp is out of date / not existed. Download it from github release...")
            _download_cqhttp()

    p = _get_cqhttp_file_name(True)
    if not p:
        p = _get_cqhttp_file_name(False)
        if p:
            logger.warning(
                f"DeltaBot v{_version.__version__} recommend go-cqhttp {cqhttp_version}, got an unrecommended cqhttp version instead!")
            _start_cqhttp(p)
        else:
            logger.error(
                f"go-cqhttp not exist! Enable 'AUTO_DOWNLOAD_GO_CQHTTP' in config file to download it automatically "
                f"or download it manually from https://github.com/Mrs4s/go-cqhttp/releases/ and move into 'cqhttp/' folder.")
    else:
        _start_cqhttp(p)
