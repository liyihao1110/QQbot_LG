# QQbot_LG
QQ频道机器人🤖，接入国内大模型，目前接入讯飞，kimi，360智脑，可视化UI界面😊，持续更新ing😁

## 开始前说两句

❤️因为看的人不多，加上时间有限，所以更新会比较慢。有什么问题欢迎来问，关注微信公众号：吃点李子。欢迎打扰！❤️

---

| 如果对你有帮助，请三连支持，项目持续更新中。源码和疑问请联系公众号：吃点李子 |
|--|

---

🌸项目由我纯手工打造，不同于市面上基于某某接入ChatGPT的项目，我的项目主要基于国内大模型，并提供详细的接入说明。请三连支持！🌸

---

## 前言

QQ机器人通过开放平台支持定制化功能，方便开发者。来看这篇文章的朋友们可能都想要搭建一个属于自己的QQ群机器人，但因为不能翻墙，所以推荐使用国内大模型。希望这篇文章能帮到有需要的朋友们！😁

### 项目介绍

项目架构如下：
```python
## models文件夹
- __init__.py
- ai360.py
- kimi.py
- xunfei.py

## templates文件夹
- index.html

## 其他文件
- 可视化界面启动.bat
- 无可视化界面启动.bat
- config.yaml
- group.py
- login.py
- requirements.txt
- web_UI.py
```

⏰本次更新增加了可视化控制界面，便于配置机器人和管理监听界面，还增加了两个国产大模型的接入，同时提供两个启动脚本：可视化启动和无可视化启动。

### 操作流程

#### 1. 获取项目

从GitHub克隆项目：
```bash
git clone https://github.com/liyihao1110/QQbot_LG.git
```

或者从Gitee克隆项目：
```bash
git clone https://gitee.com/li-yihao0328/QQbot_LG.git
```

跳转到项目目录，安装依赖：
```bash
pip install -r requirements.txt
```

运行主文件（二选一）：
```bash
- 可视化界面启动.bat
- 无可视化界面启动.bat
```

⏰启动方式说明：
1. 可视化界面启动：快捷方便，但需要确保安装Flask库且端口5000未被占用。
2. 无可视化界面启动：简单直接，但需要准备好所有模型的API和QQ机器人的授权信息。

#### 2. 可视化界面启动及配置

1. **双击启动可视化界面**：启动后，前往获取你需要的模型API，按需选择模型，注册和配置API。

2. **接入QQ机器人**：获取QQ机器人的appid和secret，完成授权配置。

3. **配置并启动机器人**：配置好API后启动机器人，查看监听界面。

本次更新优化了机器人文本回复功能，新增了以下亮点：
1. 管理员可切换模型及控制群监听；普通用户增加了问答次数限制和注册功能。
2. 群聊和频道聊天日志分离，便于查看。

#### 3. QQ频道操作与测试

以下是测试方法：

1. **频道内简单对话**：支持基本的对话测试。

2. **频道内切换模型**：在频道内切换使用的模型，确保模型配置正确。

3. **监听与关闭群聊监听**：支持对绑定群的监听操作，机器人需在对应群中。

4. **普通用户注册**：通过指令注册，获得对话次数，注册信息可动态修改。

5. **普通用户群聊测试**：支持群聊测试与消息记录。

---

至此，一个简单的QQ频道机器人搭建完成，部署在Windows服务器上即可使用。

---

## 开源地址

项目代码已开源至GitHub：[项目代码](https://github.com/liyihao1110/qq_bot_cmd)，也可在Gitee上查看：[项目代码](https://gitee.com/li-yihao0328/qq_bot_cmd)。

---

## 致谢

😍😍😍感谢支持，欢迎三连！😍😍😍
