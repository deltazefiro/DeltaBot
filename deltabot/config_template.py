from nonebot.default_config import *

"""
Config template. Please fill up the file and rename it to 'config.py'
配置样板，请填充以下配置后将本文件重命名为 'config.py'
**Cautious about privacy leaks!**
**[注意敏感信息安全!]**
"""

# =========== Go-Cqhttp ===========

# Auto manage go-cqhttp 是否自动生成配置/启动go-cqhttp
AUTO_CONFIGURE_GO_CQHTTP = True
AUTO_START_GO_CQHTTP = True

# Bot account 机器人账号&密码[若自动生成go-cqhttp配置则必填]
UIN = ''
PASSWORD = ''

# Administer(s) 管理员账号
SUPERUSERS = {}

# Cqhttp connection 与cqhttp通讯的端口
HOST = '0.0.0.0'
PORT = 8080

# =========== Basic Config ===========

# Keyword to active the bot in group chat 群聊唤醒机器人的关键词
NICKNAME = {'DeltaBot', 'deltabot', 'Deltabot', 'delta_bot'}

# Command start sign 命令的起始标记
COMMAND_START = {'', '/', '!', '！'}

# Session running expression 当有命令会话正在运行时，给用户新消息的回复
SESSION_RUNNING_EXPRESSION = "您有命令正在执行，请稍后再试（可以使用'/kill'强制结束）"

# Output debug info 是否输出调试信息
DEBUG = False

# Welcome Message 通过好友后的欢迎信息
WELCOME_MESSAGE = "Hello!欢迎使用DeltaBot~\n请使用'/help'查看功能列表"

# =========== NLP Process API ===========

# Expressing no chat answers are found 当对话API无返回结果时的输出
EXPR_DONT_UNDERSTAND = (
    '您搁那说啥呢...',
    '啥玩意？',
    '其实我不太明白你的意思……',
    '您搁那滚键盘呢？',
    '啥？'
)

# NLP API type ('tencent' / 'itpk') 对话API平台
NLP_API = 'itpk'

# Tencent AI Open Platform API 腾讯AI开发平台(https://ai.qq.com/)对话API
TENCENT_APP_ID = ''
TENCENT_APP_KEY = ''

# ITPK Robot API 茉莉机器人(http://www.itpk.cn/)对话API [不填也可调用]
ITPK_API_KEY = ''
ITPK_APT_SECRET = ''

# =========== Qzone ===========

# ChromeDriver executable path 用于模拟登录的ChromeDriver绝对位置 [尚不稳定]
CHROME_DRIVER_PATH = ''
QZONE_COOKIE = ""

# Timeout 模拟登录超时限制
QZONE_SIM_LOGIN_TIMEOUT = 8