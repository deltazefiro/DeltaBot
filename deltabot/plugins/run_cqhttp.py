from nonebot import on_startup
from loguru import logger
import subprocess
# import logging
# import threading

# def log_cqhttp(cqhttp_process):
#     with cqhttp_process.stdout:
#         for line in iter(cqhttp_process.stdout.readline, b''):  # b'\n'-separated lines
#             logger.info(line.decode('utf-8').strip())

@on_startup
def run_cqhttp():
    # TODO 使用loguru处理go-cqhttp输出
    logger.info("Start go-cqhttp!")
    cqhttp_process = subprocess.Popen(['cd cqhttp;./go-cqhttp'], shell=True)
    #                                   stdout=subprocess.PIPE,
    #                                   stderr=subprocess.STDOUT)
    # cqhttp_log_thread = threading.Thread(target=log_cqhttp, args=[cqhttp_process])
    # cqhttp_log_thread.run()
