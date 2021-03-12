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
~~一切介绍不如亲自尝试  
本项目提供一个演示用机器人「人工智障」: QQ 2240701293  
由 [@sandboxdream](https://github.com/sandboxdream) 维护
自动通过好友请求，请注意不要在匿名墙内发布不合规内容~~  
暂不提供示例机器人


## 功能

### 自动配置go-cqhttp
在机器人启动时自动配置并运行QQ协议端 [Go-cqhttp](https://github.com/Mrs4s/go-cqhttp/)  
仅需要在机器人配置文件中填写机器人账号密码信息即可自动配置运行    

### 五子棋
与机器人切磋切磋五子棋 :D  
使用带alpha-beta剪枝的极大极小搜索算法获取落子点  
使用图片形式输出与用户交互


### QQ空间匿名墙(表白墙)
通过机器人在其空间发布匿名动态  
具有违禁词审核功能(BaiduAI-antiporn)  
目前仅支持纯文本格式

其中模拟登录部分修改至 [luolongfei/qzone-spider](https://github.com/luolongfei/qzone-spider/blob/master/qzone_spider.py)

### 关键词触发  
可设置群中关键词，自动回复指定内容  
***[v1.9+]** 实验性功能，尚不稳定*

### 使用陷阱卡片获取他人ip&大致位置
生成一个音乐卡片陷阱  
对方访问卡片后即可获得其ip&大致位置  
*陷阱后端由 https://met.red/ 提供*

### 一言
获取「一言」(名言名句)  
输出排版已对移动设备端进行特别优化  
可以在配置文件中配置获取的句子类型  
*数据来源 https://www.hitokoto.cn*

### 自动对对联
神经网络自动对对联  
不支持繁体字和特殊符号，断句请用全角逗号分隔  
*数据来源 [王斌给您对对联](https://ai.binwang.me/couplet/)*

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

### 简易群轰炸
EXPLOSION is ART!!!  
群刷屏工具  

### 致电管理员
将消息转发给管理员  
适用于报告Bug

### 热重载插件
热重载配置文件和所有插件  
使插件修改立即生效，不需重启，配合热更新使用  

### Github拉取热更新
使用git从Github拉取更新，配合热重载插件可做到远程更新  

### 自动通过好友请求
自动通过好友请求

### ~~时间管理助手~~
~~暂时禁用~~