# DeltaBot

DeltaBot 是一个基于 [NoneBot](https://github.com/nonebot/nonebot) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的的QQ机器人

有些写着玩、没啥用的无聊功能

***本项目目前处于开发阶段***

[ [@sandboxdream](https://github.com/sandboxdream) 注意不要把敏感信息提交上来啊！]



## Features / TODO list

- [x] 自然语言对话
  - [x] 茉莉机器人API
  - [x] 腾讯AI开放平台API
- [x] 简易群轰炸 [plugins/boom]
- [x] 时间管理助手 [plugins/time_planning]
- [x] 呼叫管理员 (修改自[Angel-Hair/XUN_Bot](https://github.com/Angel-Hair/XUN_Bot/blob/master/xunbot/plugins/call_admin)) [plugins/call_admin]
- [x] 重载插件 [plugins/reload]
- [x] 自动通过好友请求 [plugins/request_process]
- [x] 使用说明 [plugins/usage]
- [x] 转换xml代码为卡片 [plugins/xml]
- [x] 使用陷阱网站获取ip [plugins/get_ip]
  - [ ] 陷阱网站嵌入音乐xml卡片
- [x] Qzone(QQ空间)发说说 [plugins/qzone] [**需单独安装**]
  - [x] 公告
  - [x] 简易匿名墙
  - [x] 模拟登录 (修改自 [luolongfei/qzone-spider](https://github.com/luolongfei/qzone-spider)) [plugins/qzone/sim_login]
  - [ ] 接入敏感词识别接口
  - [ ] 举报机制
  - [ ] 图片发送支持
- [ ] 安装向导
- [ ] scp基金会猜标号小游戏




## Usage

### Linux

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

   将配置信息填充入 *deltabot/config_template.py* 并将其重命名为 *config.py*

   [go-cqhttp的配置文件将自动使用DeltaBot的配置文件填充]

   

5. 运行 DeltaBot

   在**本项目根目录**下运行命令：

   ```bash
   python3 start.py
   ```

   **[请一定进入本项目所在目录启动项目，否则可能出现相对位置错误]**

   [go-cqhttp将自动被DeltaBot启动，请勿手动启动]
   
   
   
6. [Optional] 启用 'qzone' 插件

   **[以下操作仅用于启用 Qzone 相关功能(匿名墙、公告等功能)，非必须步骤]**

   **[实验性功能，已知Bug: 在出现验证码时一定概率登录空间失败]**

   1. 安装 requirements.txt 中注释掉的Qzone相关依赖库
   2. 安装 Chrome 浏览器
   3. 下载与浏览器版本对应的 [ChromeDriver](https://chromedriver.chromium.org/)
   4. 填写 *deltabot/config.py* 中的Qzone选填项



### Windows

- 待补充



## Thanks

感谢以下项目:

- QQ协议端 [Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- 前端框架 [NoneBot](https://github.com/nonebot/nonebot)
- 部分代码修改自 [Angel-Hair/XUN_Bot](https://github.com/Angel-Hair/XUN_Bot)
- Qzone模拟登录修改自 [luolongfei/qzone-spider](https://github.com/luolongfei/qzone-spider)


## License

go-cqhttp下的文件 ([go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的可执行程序) 保持使用原 [AGPL-3.0 License](https://github.com/Mrs4s/go-cqhttp/blob/master/LICENSE) 许可

项目中其余内容使用 MIT License

