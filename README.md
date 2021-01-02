# DeltaBot

DeltaBot 是一个基于 [NoneBot](https://github.com/nonebot/nonebot) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的的QQ机器人

有些写着玩、没啥用的无聊功能

***本项目目前处于开发阶段***

[ [@sandboxdream](https://github.com/sandboxdream) 注意不要把敏感信息提交上来啊！]



## Features / TODO list

- [x] 自然语言对话
  - [x] 茉莉机器人API
  - [x] 腾讯AI开放平台API
- [x] 简易群轰炸
- [x] 时间管理助手
- [x] 呼叫管理员 (修改自[Angel-Hair/XUN_Bot](https://github.com/Angel-Hair/XUN_Bot/blob/master/xunbot/plugins/call_admin))
- [x] 重载所有插件 (软重启)
- [x] 自动通过好友请求
- [x] 使用说明
- [x] 转换xml代码为卡片
- [x] 使用陷阱网站获取ip
  - [ ] 陷阱网站嵌入音乐xml卡片
- [x] Qzone发说说
  - [x] 公告
  - [x] 简易匿名墙
  - [ ] 接入敏感词识别接口
  - [ ] 举报机制
  - [ ] 图片发送支持
- [ ] 安装向导
- [ ] 音乐xml
- [ ] scp基金会猜标号小游戏
- [ ] 子插件管理
- [ ] 群管理
  - [ ] 指令禁言
  - [ ] 发布群公告
  - [ ] 撤回成员消息
  - [ ] 踢出不活跃群员
  - [ ] 全局黑名单 


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

