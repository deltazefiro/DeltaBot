---
sidebarDepth: 2
---
# Usage

:::tip NOTE  
本页面`示例`部分尚待补充
:::

## 基本
### 私聊使用
如果在私聊中使用命令，需要以你于`./deltabot/config.py` 中的`COMMAND_START`设置的命令开头符在最开始。如果其中设置空字符串，则表示可以不使用开头符

默认情况下，允许使用**无开头字符**，或以全角和半角的`!`以及`/`开头
![](https://cdn.jsdelivr.net/gh/sandboxdream/figurebed/20210203133657.png)

### 在群聊中使用
在群聊中使用时，为了避免误触，需要在命令开头**at机器人**或**使用机器人触发词**激活。
![](https://cdn.jsdelivr.net/gh/sandboxdream/figurebed/20210203134115.png)


## 插件使用说明
### usage(使用帮助)
获取机器人有关帮助

#### 命令:  

- `help`
- `help [插件名称]`

当`[插件名称]`为空时，输出插件列表
![](https://cdn.jsdelivr.net/gh/sandboxdream/figurebed/20210203134256.png)
:::tip NOTE  
普通用户获取的插件列表中会自动隐藏管理员命令
:::

如果需要有关插件的详细帮助，请使用空格分开help和插件名如 `help gomoku`

![](https://cdn.jsdelivr.net/gh/sandboxdream/figurebed/20210203135548.png)


### basic(基础控制)
机器人基础控制插件

#### 命令：

- `ping`
  测试机器人存活性
- `kill`
  终止当前命令任务，用于处理卡死
- `log` <Badge type="warning" text="仅管理员"/> 
  发送信息到控制台
- `version`
  获取机器人版本信息

#### 示例：  

![](https://cdn.jsdelivr.net/gh/sandboxdream/figurebed/20210203134411.png)



### boom(消息轰炸) <Badge type="warning" text="仅管理员"/>
直接进行刷屏，请小心群管、群主。 
::: danger
过度使用可能触发风控/群管理暴怒！
:::
*需要管理员权限*

#### 命令:

- `boom` 消息轰炸

#### 示例:  

### calladmin(致电管理员)
用于给管理员(Superuser)发送消息  
发送的消息包括消息内容、消息发送者、发送时间  

#### 命令:

- `calladmin [消息内容]`

#### 示例:  

![](https://cdn.jsdelivr.net/gh/sandboxdream/figurebed/20210203145245.png)



### couplet(对对联)

你出上联，机器人会自动对出下联
::: warning
本插件使用的API为「[王斌给您对对联](https://ai.binwang.me/couplet/)」 通过抓包取得的**非公开API**  
因此请不要频繁调用，对服务器产生影响  
如果条件允许，请自行搭建对对联后端 [wb14123/seq2seq-couplet](https://github.com/wb14123/seq2seq-couplet)
:::

#### 命令:

- `couplet [上联]`

#### 示例:  

![](https://cdn.jsdelivr.net/gh/sandboxdream/figurebed/20210203150531.png)



### getip(获取IP陷阱)
生成一个音乐卡片陷阱  
对方访问卡片后即可获得其ip&大致位置  
*陷阱后端由 https://met.red/ 提供*

::: tip NOTE
目前陷阱音乐使用的歌曲暂时硬编码为「[逍遥游 by littlealone100]((https://music.163.com/#/song?id=532522915))」，暂不支持自定义歌曲
:::

#### 使用方式:
  1. 使用命令 '/gettrap' 生成一个含有陷阱的音乐卡片（同时生成一个key）
  2. 将陷阱音乐卡片【转发】给你想获取ip的用户
  3. 当此用户进入听过此音乐后, 你可以通过 '/getip' 并输入key获取此用户的ip

#### 命令:
- `gettrap`
  生成陷阱音乐卡片
  
- `getip [key]`
  获取用户ip  
  请确保陷阱网址**已被访问**



### getlog(输出log)
输出log文件的最后10行

#### 命令:
- `getlog` 输出log

#### 示例:


### gomoku(五子棋)

来和机器人搓一把五子棋吧  
使用图片形式输出与用户交互  
:::warning
本插件需要单独安装配置以启用！详见 [gomoku模块安装](/setup.html#gomoku模块-五子棋-安装)
:::

#### 命令:

- `gomoku` 开始游戏

#### 示例:  

![](https://cdn.jsdelivr.net/gh/sandboxdream/figurebed/20210203151323.png)



### hitokoto(一言)
获取「一言」(名言名句)  
输出排版已对移动设备端进行特别优化  
可以在配置文件中配置获取的句子类型  
*数据来源 https://www.hitokoto.cn*

#### 命令:
- `hitokoto`

#### 示例:  



### keyword(关键词触发) <Badge type="warning" text="仅管理员"/>
设置特定关键词，触发机器人自动回复群组中含关键词的特定消息   
:::tip NOTE
以下命令仅在群组中可用！
:::  

*需要机器人管理员(SuperUser)/群组管理员(GroupAdmin)权限*

#### 命令:
 - `/keyword add [触发词] [回复内容]`  
    添加触发词
    
 - `/keyword ls`  
    列出设置的触发词
 
 - `/keyword rm [触发词]`  
    删除特定的触发词
    
#### 示例:
如需检测到群信息中包含 '笨蛋' 自动回复 '请文明交流'，  
则使用 '/keyword add 笨蛋 请文明交流' 添加该触发词  
如要删除上述触发词，可输入 '/keyword rm 笨' 然后选择对应序号删除



### lmbtfy(帮你百度)
Let Me Baidu That For You.  
> 好消息！本机器人已与百度达成合作关系，今后大家有什么不懂的可以直接让我帮你百度一下！  

群内伸手党治理利器  
*网站由 http://tool.mkblog.cn/lmbtfy/ 提供*  

#### 命令:
- `lmbtfy [搜索关键词]` 生成「帮你百度」网址

#### 示例:  



### qzone(空间匿名墙)
通过机器人在其空间发布动态  
目前仅支持纯文本格式

::: danger
请勿发布违规内容，有自动违禁词审核功能！
:::  
::: tip NOTE
若在发送内容时提醒 `空间登录令牌不存在/QQ空间cookie已过期`  
此为正常现象，机器人会模拟登录自动重新获取令牌  
可以稍等片刻后再使用此功能  
管理员可以收到模拟登录的进度
:::  
:::warning
本插件需要单独安装配置以启用！详见 [qzone模块安装](/setup.html#qzone模块-匿名墙功能-安装)
:::

#### 命令:
- `announce [内容]`
  在空间发布公告 <Badge type="warning" text="仅管理员"/> 
  
- `anonymous [内容]`
  在空间发布匿名内容(匿名墙)

#### 示例:



### reload(热重载) <Badge type="warning" text="仅管理员"/> 
热重载配置文件和所有插件  
使插件修改立即生效，不需重启，配合热更新使用  
*需要管理员权限*
#### 命令:
- `reload`
#### 示例:



### update(热更新) <Badge type="warning" text="仅管理员"/> <Badge type="error" text="实验性功能"/>
使用git从Github拉取更新，配合热重载插件可做到远程更新  
:::tip NOTE
若更新中包含配置文件内容更新，仍需要手动重新配置配置文件  
更新日志可能会造成刷屏，请谨慎地在群聊中操作  
本功能需要额外安装 `git`
:::
:::danger
实验性功能，可能损坏机器人！
:::

#### 命令:

- `update`

#### 示例:  

![](https://cdn.jsdelivr.net/gh/sandboxdream/figurebed/20210203132112.png)



### xml(xml卡片转换)
将xml代码转换为卡片  
::: danger
过度使用有封号风险！
:::

#### 命令:

- `xml [xml代码]`

#### 示例: 