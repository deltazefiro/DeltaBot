---
sidebarDepth: 2
---
# Usage
使用方式 可通过'/help'查看  

友情提示:有图，国内可能无法查看，请以科学的方式查看图片

## 基本
如果在私聊中使用命令，需要以你于./deltabot/config.py 中的COMMAND_START设置的命令开头符在最开始。如果其中设置空字符串，则表示可以不使用开头符

默认情况下，允许使用无开头字符，以全角和半角的!以及/开头
![](https://raw.githubusercontent.com/sandboxdream/figurebed/master/20210203133657.png)

## 在群聊中使用
在群聊中使用时，为了避免误触，需要在命令开头at机器人或使用机器人的昵称激活。
![](https://raw.githubusercontent.com/sandboxdream/figurebed/master/20210203134115.png)

## 基础命令
### help 
获取机器人有关帮助
![](https://raw.githubusercontent.com/sandboxdream/figurebed/master/20210203134256.png)

如果需要有关插件的帮助，请使用空格分开help和插件名如`/help gomoku`

![](https://raw.githubusercontent.com/sandboxdream/figurebed/master/20210203135548.png)


### ping
确认机器人当前仍在运行
![](https://raw.githubusercontent.com/sandboxdream/figurebed/master/20210203134411.png)

### update
从github库进行自动升级

需要安装git

此命令为git pull 所以无需指定库和分支

更新日志可能会造成刷屏，请谨慎地在群聊中操作

![](https://raw.githubusercontent.com/sandboxdream/figurebed/master/20210203132112.png)
![](https://raw.githubusercontent.com/sandboxdream/figurebed/master/20210203132135.png)

