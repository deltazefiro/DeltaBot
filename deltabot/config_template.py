from nonebot.default_config import *

"""
配置样板，请填充以下配置后将本文件重命名为 'config.py'
**注意敏感信息安全!**
"""

# =========== Go-Cqhttp ===========
# 自动管理[Go-cqhttp](https://github.com/Mrs4s/go-cqhttp/)
# [暂时仅支持linux-amd64与windows-amd64平台的自动管理，
# 其它平台请将本分类下所有以'AUTO_'开头的选项为False并手动获取并在'PORT'设置的端口运行go-cqhttp]

# 与cqhttp通讯的端口
HOST = '0.0.0.0'
PORT = 8080

# 自动从go-cqhttp的Github下载其Release (同时控制是否自动更新go-cqhttp)
# 若下载失败，请关闭此项并手动从 https://github.com/Mrs4s/go-cqhttp/releases 下载对应平台的版本，
# 并将其重命名为 go-cqhttp (文件扩展名不变)
AUTO_DOWNLOAD_GO_CQHTTP = True

# 是否自动生成go-cqhttp配置/启动go-cqhttp
AUTO_CONFIGURE_GO_CQHTTP = True
AUTO_START_GO_CQHTTP = True

# 机器人账号&密码[若自动生成go-cqhttp配置则必填]
UIN = ''
PASSWORD = ''


# =========== Basic Config ===========

# 群聊唤醒机器人的关键词
NICKNAME = {'DeltaBot', 'deltabot', 'Deltabot', 'delta_bot'}

# 命令的起始标记
COMMAND_START = {'', '/', '!', '！'}

# 当有命令会话正在运行时，给用户新消息的回复
SESSION_RUNNING_EXPRESSION = "您有命令正在执行，请稍后再试（可以使用'/kill'强制结束）"

# 是否输出调试信息
DEBUG = False

# 通过好友后的欢迎信息
WELCOME_MESSAGE = "Hello!欢迎使用DeltaBot~\n请使用'/help'查看功能列表"

# 管理员账号
SUPERUSERS = {}

# =========== NLP Process API ===========

# 当对话API无返回结果时的输出
EXPR_DONT_UNDERSTAND = (
    '您搁那说啥呢...',
    '啥玩意？',
    '其实我不太明白你的意思……'
)

# 对话API平台选择 ('tencent' / 'itpk' / '')
# 若为 '' 则不启用对话功能
NLP_API = 'itpk'

# [可选]腾讯AI开发平台(https://ai.qq.com/)对话API
TENCENT_APP_ID = ''
TENCENT_APP_KEY = ''

# [可选]茉莉机器人(http://www.itpk.cn/)对话API [不填也可调用]
ITPK_API_KEY = ''
ITPK_APT_SECRET = ''

# =========== Hitokoto ===========

# 一言的句子类型，见 https://developer.hitokoto.cn/sentence/#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0
# 若要启用所有类型，可不填
HITOKOTO_CATEGORY = {'a', 'i'}

# =========== Qzone ===========
# [仅在使用 Qzone 插件时需要填写以下项]

# 驱动器ChromeDriver的绝对位置
CHROME_DRIVER_PATH = ''

# 模拟登录超时限制
QZONE_SIM_LOGIN_TIMEOUT = 8

# 是否调用 百度AI开发平台 进行的非法信息审核
CHECK_ILLEGAL_INFO = False

# [可选]百度AI开发平台的 API Key & Secret Key
# 参见 https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjgn3
# [创建应用时必须勾选接口 '内容审核平台-文本' 才可使用]
# 可以在 https://ai.baidu.com/censoring#/strategylist 配置审核策略
BAIDU_API_KEY = ''
BAIDU_SECRET_KEY = ''

# =========== Internal Config ===========
# 内部配置，请勿更改