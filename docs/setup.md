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

3. 安装依赖库

   ```bash
   pip install -r requirements.txt
   ```

4. 修改配置文件

   将配置信息填充入 `deltabot/config_template.py` 并将其重命名为 `config.py`  
   :::tip NOTE
   go-cqhttp的配置文件将自动使用DeltaBot的配置文件填充
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
仓库内目前仅封装了`linux-amd64`平台的可执行文件  
其它平台需要自行编译，**需要gcc环境**
``` bash
# 编译命令，在项目根目录下运行
g++ -O3 -fPIC -shared -o deltabot/plugins/gomoku/search.so deltabot/plugins/gomoku/search.cpp
```