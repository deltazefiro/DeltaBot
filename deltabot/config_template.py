from nonebot.default_config import *

"""
Config template. Please fill up the file and rename it to 'config.py'
**Cautious about privacy leaks!**
"""

# =========== Basic config ===========

# Bot account
UIN = ''
PASSWORD = ''

# Administer(s)
SUPERUSERS = {}

# Keyword to active the bot in group chat
NICKNAME = {'DeltaBot', 'deltabot', 'Deltabot', 'delta_bot'}

# Cqhttp connection
HOST = '0.0.0.0'
PORT = 8080

# Output debug info
DEBUG = False

# Welcome Message
WELCOME_MESSAGE = "Hello!欢迎使用DeltaBot~\n请使用'/help'查看功能列表"

# =========== NLP Process API ===========

# Expressing no chat answers are found
EXPR_DONT_UNDERSTAND = (
    '您搁那说啥呢...',
    '啥玩意？',
    '其实我不太明白你的意思……',
    '您搁那滚键盘呢？',
    '啥？'
)

# NLP API type ('tencent' / 'itpk')
NLP_API = 'itpk'

# Tencent AI Open Platform API (https://ai.qq.com/)
TENCENT_APP_ID = ''
TENCENT_APP_KEY = ''

# ITPK Robot API (http://www.itpk.cn/)
ITPK_API_KEY = ''
ITPK_APT_SECRET = ''

# =========== Qzone ===========
QZONE_COOKIE = ""