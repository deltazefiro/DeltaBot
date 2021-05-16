---
sidebarDepth: 2
---
# Setup

## 基础安装

1. 安装Python3.7+
   :::warning
   注意必须Python版本必须>=3.7
   :::

2. 克隆本项目

   ```bash
   git clone --depth=1 https://github.com/233a344a455/DeltaBot.git
   ```  
   
   :::tip NOTE
   由于本项目仍在快速迭代中，不建议使用 Release 版本  
   :::

3. 安装依赖库

   ```bash
   pip install -r requirements.txt
   ```

4. 修改配置文件

   将配置信息填充入 `deltabot/config_template.py` 并将其重命名为 `config.py`  
   :::tip NOTE
   go-cqhttp的配置文件将自动使用DeltaBot的配置文件填充
   :::  
   
   配置文件示例  
   
   ```python
   from typing import Union, Pattern, Collection, Iterable

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
   HOST: str = '0.0.0.0'
   PORT: int = 8080
   
   # 自动从go-cqhttp的Github下载其Release (同时控制是否自动更新go-cqhttp)
   # 若下载失败，请关闭此项并手动从 https://github.com/Mrs4s/go-cqhttp/releases 下载对应平台的版本，
   # 并将其重命名为 go-cqhttp (文件扩展名不变)
   AUTO_DOWNLOAD_GO_CQHTTP: bool = True
   
   # 是否自动生成go-cqhttp配置/启动go-cqhttp
   AUTO_CONFIGURE_GO_CQHTTP: bool = True
   AUTO_START_GO_CQHTTP: bool = True
   
   # 机器人账号&密码[若自动生成go-cqhttp配置则必填]
   UIN: str = '12345678'
   PASSWORD: str = '98765432'
   
   
   # =========== Basic Config ===========
   
   # 群聊唤醒机器人的关键词
   NICKNAME: Iterable[Union[str, Pattern]] = {'DeltaBot', 'deltabot', 'Deltabot', 'delta_bot', '@DeltaBot'}
   
   # 命令的起始标记
   COMMAND_START: Iterable[Union[str, Pattern]] = {'', '/', '!', '！'}
   
   # 当有命令会话正在运行时，给用户新消息的回复
   SESSION_RUNNING_EXPRESSION: str = "您有命令正在执行，请稍后再试（可以使用'/kill'强制结束）"
   
   # 是否输出调试信息
   DEBUG: bool = False
   
   # 是否自动通过好友申请
   APPROVE_FRIEND_ADDING: bool = True
   
   # 自动通过加群邀请模式
   # 可选 'everyone'(自动同意所有加群邀请) / 'superuser'(仅通过superuser的加群邀请) / 'disable' (不自动通过任何邀请)
   APPROVE_GROUP_INVITE_MODE: str = 'superuser'
   
   # 通过好友后的欢迎信息
   WELCOME_MESSAGE: str = "Hi!欢迎使用DeltaBot~\n请使用'/help'查看功能列表"
   
   # 管理员账号
   SUPERUSERS: Collection[int] = {12345678}
   
   # =========== NLP Process API ===========
   
   # 当对话API无返回结果时的输出
   EXPR_DONT_UNDERSTAND = (
       '您搁那说啥呢...',
       '啥玩意？',
       '其实我不太明白你的意思……'
   )
   
   # 对话API平台选择 ('tencent' / 'itpk' / '')
   # 若为 '' 则不启用对话功能
   NLP_API: str = 'itpk'
   
   # [可选]腾讯AI开发平台(https://ai.qq.com/)对话API
   TENCENT_APP_ID: str = 'blablabla'
   TENCENT_APP_KEY: str = 'blablabla'
   
   # [可选]茉莉机器人(http://www.itpk.cn/)对话API [不填也可调用]
   ITPK_API_KEY: str = 'blablabla'
   ITPK_APT_SECRET: str = 'blablabla'
   
   # =========== Hitokoto ===========
   
   # 一言的句子类型，见 https://developer.hitokoto.cn/sentence/#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0
   # 若要启用所有类型，可不填
   HITOKOTO_CATEGORY: Iterable[str] = {'a', 'i'}
   
   # =========== Qzone ===========
   # [仅在使用 Qzone 插件时需要填写以下项]
   
   # 驱动器ChromeDriver的绝对位置
   CHROME_DRIVER_PATH = '/home/user/Program/chromedriver'
   
   # 模拟登录超时限制
   QZONE_SIM_LOGIN_TIMEOUT = 8
   
   # 是否调用 百度AI开发平台 进行的非法信息审核
   CHECK_ILLEGAL_INFO = False
   
   # [可选]百度AI开发平台的 API Key & Secret Key
   # 参见 https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjgn3
   # [创建应用时必须勾选接口 '内容审核平台-文本' 才可使用]
   # 可以在 https://ai.baidu.com/censoring#/strategylist 配置审核策略
   BAIDU_API_KEY = 'blablabla'
   BAIDU_SECRET_KEY = 'blablabla'
   
   ```
   
   :::warning
   本示例文件可能不会及时更新，如有不同，请遵循 `config_template.py` 的注释填写
   :::  
   
5. 运行 DeltaBot

   在**本项目根目录**下运行命令：

   ```bash
   python3 start.py
   ```
   ::: warning
   请一定进入本项目所在目录启动项目，否则可能出现相对位置错误  
   :::

   :::tip NOTE
   首次运行时会自动从 GithubRelease 下载并配置协议端 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) , 请确保设备能够连接到Github  

   若下载不成功，可以从 [这里](https://github.com/Mrs4s/go-cqhttp/releases)手动下载对应平台的可执行文件并将其放入 `cqhttp/`  
   :::

   :::warning
   Go-cqhttp的自动下载、配置与运行暂时仅支持linux-amd64与windows-amd64平台，  
   其它平台请手动获取配置运行go-cqhttp，  
   并将`config.py`中的`go-cqhttp`分类下所有以`AUTO_`开头的选项为False
   :::

6.Enjoy!


以下为可选模块:  
## qzone模块(匿名墙功能)安装
:::warning
实验性功能，已知Bug: 在出现验证码时一定概率登录空间失败
:::

1. 安装 `requirements.txt` 中注释掉的Qzone相关依赖库
2. 安装 Chrome 浏览器
3. 下载与浏览器版本对应的 [ChromeDriver](https://chromedriver.chromium.org/)
4. 填写 `deltabot/config.py` 中的Qzone选填项

## gomoku模块(五子棋)安装
为了保证运行效率，搜索算法核心代码使用C++编写  
目前提供了`linux-amd64`平台的可执行文件，请从 [此处](https://github.com/233a344a455/DeltaBot/releases/download/v0.1.8/search.so) 下载并将其放置到 `deltabot/plugins/gomoku/` 目录下  

其它平台需要自行编译，**需要gcc环境**
``` bash
# 编译命令，在项目根目录下运行
g++ -O3 -fPIC -shared -o deltabot/plugins/gomoku/search.so deltabot/plugins/gomoku/search.cpp
```