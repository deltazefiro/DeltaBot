---
sidebarDepth: 2
---
# Features

## 特点

DeltaBot 有以下特点:

- ### 傻瓜式部署
  全自动化管理配置QQ协议端(go-cqhttp)，免除配置复杂易错等问题，开箱即用

- ### 轻量

  不需要 Docker、mysql 等其它应用，使用Python完成一切，减少额外的性能开销

- ### 高性能

  所有网络IO均使用异步处理，防止发生阻塞，保证高并发性

## Demo
![demo](https://img.shields.io/badge/demoQQ-2240701293-yellow.svg)  
一切介绍不如亲自尝试  
本项目提供一个演示用机器人「人工智障」: QQ 2240701293  
由 [@sandboxdream](https://github.com/sandboxdream) 维护 ~~要是挂了去打他~~  
自动通过好友请求，请注意不要在匿名墙内发布不合规内容


## 功能

### 自动配置go-cqhttp
在机器人启动时自动配置并运行QQ协议端 [Go-cqhttp](https://github.com/Mrs4s/go-cqhttp/)  
仅需要在机器人配置文件中填写机器人账号密码信息即可自动配置运行    
::: warning
目前本功能仅支持`linux-amd64`与`windows-amd64`平台的自动管理
:::

::: tip NOTE
首次运行时，机器人会自动从go-cqhttp的Github下载其Release，请保证网络畅通
:::

### 五子棋

与机器人切磋切磋五子棋 :D  
使用带alpha-beta剪枝的极大极小搜索算法获取落子点  
使用图片形式输出与用户交互

::: warning
为了保证运行效率，搜索算法核心代码使用C++编写  
仓库内目前仅封装了`linux-amd64`平台的可执行文件  
其它平台需要自行编译！  
```
# 编译命令，在项目根目录下运行 (需要gcc环境)
g++ -O3 -fPIC -shared -o deltabot/plugins/gomoku/search.so deltabot/plugins/gomoku/search.cpp
```
:::

### QQ空间匿名墙(表白墙)
通过机器人在其空间发布匿名动态  
具有违禁词审核功能(BaiduAI-antiporn)  
目前仅支持纯文本格式

::: warning
本功能需要单独配置以启用  
详见 [Setup](/setup)
:::  

其中模拟登录部分修改至 [luolongfei/qzone-spider](https://github.com/luolongfei/qzone-spider/blob/master/qzone_spider.py)

### 使用陷阱卡片获取他人ip&大致位置
生成一个音乐卡片陷阱  
对方访问卡片后即可获得其ip&大致位置  
*陷阱后端由 https://met.red/ 提供*

::: tip NOTE
目前陷阱音乐使用的歌曲暂时硬编码为「[逍遥游 by littlealone100]((https://music.163.com/#/song?id=532522915))」，暂不支持自定义歌曲
:::

### 一言
获取「一言」(名言名句)  
输出排版已对移动设备端进行特别优化  
可以在配置文件中配置获取的句子类型  
*数据来源 https://www.hitokoto.cn*

### 自动对对联
神经网络自动对对联  
不支持繁体字和特殊符号，断句请用全角逗号分隔  
::: warning
本插件使用的API为「[王斌给您对对联](https://ai.binwang.me/couplet/)」 通过抓包取得的**非公开API**  
因此请不要频繁调用，对服务器产生影响  
如果条件允许，请自行搭建对对联后端 [wb14123/seq2seq-couplet](https://github.com/wb14123/seq2seq-couplet)
:::

### 让我帮你百度一下
Let Me Baidu That For You.  
> 好消息！本机器人已与百度达成合作关系，今后大家有什么不懂的可以直接让我帮你百度一下！  

群内伸手党治理利器  
*网站由 http://tool.mkblog.cn/lmbtfy/ 提供*

### 自然语言对话
闲聊功能
目前提供两个API接口选用:
- [腾讯AI开发平台](https://ai.qq.com/)
- [ITPK(茉莉机器人)](http://www.itpk.cn/)

可在配置文件中选择调用接口

### 转换xml代码为卡片

将xml代码转换为卡片  
::: danger
过度使用有封号风险！
:::
*需要管理员权限*

### 简易群轰炸

EXPLOSION is ART!!!  
群刷屏工具  
::: danger
过度使用可能触发风控/群管理暴怒！
:::
*需要管理员权限*

### 致电管理员
将消息转发给管理员  
适用于报告Bug

### 热重载插件
热重载配置文件和所有插件  
使插件修改立即生效，不需重启，配合热更新使用  
*需要管理员权限*

### Github拉取热更新
使用git从Github拉取更新，配合热重载插件可做到远程更新  
:::tip NOTE
若更新中包含配置文件内容更新，仍需要手动重新配置配置文件  
本功能需要额外安装 `git`
:::
:::danger
实验性功能，可能损坏机器人！
:::

### 自动通过好友请求
自动通过好友请求

### ~~时间管理助手~~
~~暂时禁用~~