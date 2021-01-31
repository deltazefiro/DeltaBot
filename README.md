![DeltaBot](https://raw.githubusercontent.com/233a344a455/ImageHost/master/deltabot.jpg)
<div align="center">

**DeltaBot** 是一个基于 [NoneBot](https://github.com/nonebot/nonebot) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的没用的QQ机器人

有些写着玩、没啥用的无聊功能

**本项目为个人学习用项目!!!**

![License](https://img.shields.io/github/license/233a344a455/DeltaBot)
![Release](https://img.shields.io/github/v/release/233a344a455/DeltaBot?include_prereleases)
![Python Version](https://img.shields.io/badge/python-3.7+-ff69b4.svg)
![NoneBot Version](https://img.shields.io/badge/nonebot-1.8.0+-red.svg)
![Demo](https://img.shields.io/badge/demoQQ-2240701293-yellow.svg)

</div>

## Features / TODO list

- [x] 自然语言对话
  - [x] 茉莉机器人API
  - [x] 腾讯AI开放平台API
- [x] 简易群轰炸 [plugins/boom]
- [x] 时间管理助手 [plugins/time_planning]
- [x] 呼叫管理员 (修改自[Angel-Hair/XUN_Bot](https://github.com/Angel-Hair/XUN_Bot/blob/master/xunbot/plugins/call_admin)) [plugins/test]
- [x] 重载插件 [plugins/reload]
- [x] 自动通过好友请求 [plugins/request_process]
- [x] 使用说明 [plugins/usage]
- [x] 转换xml代码为卡片 [plugins/xml]
- [x] 使用陷阱网站获取他人ip&大致位置 [plugins/get_ip]
  - [x] 陷阱网站嵌入音乐xml卡片
  - [ ] 支持自定义陷阱歌曲
- [x] Qzone(QQ空间)发说说 [plugins/qzone] [**需单独安装**]
  - [x] 公告
  - [x] 简易匿名墙
  - [x] 模拟登录 (修改自 [luolongfei/qzone-spider](https://github.com/luolongfei/qzone-spider)) [plugins/qzone/sim_login]
  - [x] 接入敏感词识别接口
  - [ ] 举报机制
  - [ ] 图片发送支持
- [x] 接入「[一言](hitokoto.cn)」[plugins/hitokoto]
- [x] 接入 [自动对对联](https://ai.binwang.me/couplet/) [plugins/couplet]
- [ ] scp基金会猜标号小游戏


## Demo

本项目提供一个演示用机器人「人工智障」: QQ 2240701293  
由 [@sandboxdream](https://github.com/sandboxdream) 维护 ~~要是挂了去打他~~  
自动通过好友请求，请注意不要在匿名墙内发布不合规内容


## Usage

1. 安装Python3.7+ **[注意必须Python版本必须>=3.7]**

2. 克隆本项目

   ```bash
   git clone --depth=1 https://github.com/233a344a455/DeltaBot.git
   ```

   

3. 安装依赖库

   ```bash
   pip install -r requirements.txt
   ```

   

4. 修改配置文件

   将配置信息填充入 `deltabot/config_template.py` 并将其重命名为 `config.py`  
   [go-cqhttp的配置文件将自动使用DeltaBot的配置文件填充]

   

5. [Optional] 启用 'qzone' 插件

   **[以下操作仅用于启用 Qzone 相关功能(匿名墙、公告等功能)，非必须步骤]**  
   **[实验性功能，已知Bug: 在出现验证码时一定概率登录空间失败]**

   1. 安装 `requirements.txt` 中注释掉的Qzone相关依赖库

   2. 安装 Chrome 浏览器
   3. 下载与浏览器版本对应的 [ChromeDriver](https://chromedriver.chromium.org/)
   4. 填写 `deltabot/config.py` 中的Qzone选填项

   

6. 运行 DeltaBot

   在**本项目根目录**下运行命令：

   ```bash
   python3 start.py
   ```

   **[请一定进入本项目所在目录启动项目，否则可能出现相对位置错误]**  
   首次运行时会自动从 GithubRelease 下载并配置协议端 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) , **请确保设备能够连接到Github**  
   若下载不成功，可以从[这里](https://github.com/Mrs4s/go-cqhttp/releases)手动下载对应平台的可执行文件并将其放入 `cqhttp/`

   

   Go-cqhttp的自动下载、配置与运行暂时仅支持linux-amd64与windows-amd64平台，  
   其它平台请手动获取配置运行go-cqhttp，  
   并将`config.py`中的`go-cqhttp`分类下所有以`AUTO_`开头的选项为False

   

## Thanks

感谢以下伟大的项目:

- QQ协议端 [Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- 前端框架 [NoneBot](https://github.com/nonebot/nonebot)
- 部分代码修改自 [Angel-Hair/XUN_Bot](https://github.com/Angel-Hair/XUN_Bot)
- Qzone模拟登录修改自 [luolongfei/qzone-spider](https://github.com/luolongfei/qzone-spider)
- 网易云 [@littlealone100](https://music.163.com/#/artist?id=12063182) 所创作的充满吸引力的作品「 [逍遥游](https://music.163.com/#/song?id=532522915) 」作为音乐陷阱的诱饵
- ~~[@sandboxdream](https://github.com/sandboxdream) 为本项目readme做出的 [至关重要的贡献](https://github.com/233a344a455/DeltaBot/commit/91dc0601fb0c5ed48caaa6f6cc99a77280d3e52a)~~



## License

MIT
