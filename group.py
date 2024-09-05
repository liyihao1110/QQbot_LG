import os
import re
import botpy
import json
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message
from models.xunfei import xfly
from models.kimi import chat
from models.ai360 import chat1

# 用户数据文件路径
USER_JSON_PATH = "user.json"

# 读取配置文件 "config.yaml"
test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

# 设置日志记录器
_log = logging.get_logger()
_log_group = logging.get_logger("group")
_log_at = logging.get_logger("at")


class MyClient(botpy.Client):
    """
    自定义客户端类，处理机器人准备就绪、群组@消息和频道@消息的事件。
    """

    def __init__(self, intents):
        super().__init__(intents=intents)
        self.listening = False  # 初始状态为不监听群组消息
        self.users = self.load_users()  # 加载用户信息
        self.response_function = xfly  # 默认响应函数为 xunfei

    def load_users(self):
        """
        从 user.json 文件中加载用户数据。
        """
        if not os.path.exists(USER_JSON_PATH):
            return {}
        try:
            with open(USER_JSON_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            _log.error("用户数据文件格式错误，无法解析。")
            return {}

    def save_users(self):
        """
        将当前用户数据保存到 user.json 文件中。
        """
        with open(USER_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=4)

    async def on_ready(self):
        """
        当机器人准备就绪时调用。
        """
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_at_message_create(self, message: GroupMessage):
        """
        处理群组中的@消息。
        """
        if not self.listening:
            return

        user_id = message.author.member_openid
        message_content = message.content.strip()

        # 处理注册逻辑
        if message_content.startswith("/sign"):
            await self.handle_sign_command(message, user_id, message_content)
        elif user_id in self.users:
            await self.handle_registered_user_message(message, user_id, message_content)

    async def handle_sign_command(self, message, user_id, content):
        """
        处理用户注册命令 /sign {用户名}
        """
        sign_match = re.match(r"/sign\s+(\w+)", content)
        if not sign_match:
            await message.reply(content="注册失败，请使用正确的格式：/sign {用户名}")
            return

        register_name = sign_match.group(1)
        if user_id in self.users:
            await message.reply(content=f"用户 {self.users[user_id]['username']} 已注册，无需重复注册。")
            return

        self.users[user_id] = {"username": register_name, "balance": 500}
        self.save_users()
        await message.reply(content=f"欢迎新用户 {register_name}，您的初始余额为 500 次。")
        _log_group.info(f"新用户注册：{register_name}，ID：{user_id}")

    async def handle_registered_user_message(self, message, user_id, content):
        """
        处理已注册用户的消息和扣费逻辑。
        """
        user_info = self.users[user_id]
        if user_info.get("balance", 0) <= 0:
            await message.reply(content=f"{user_info['username']}，您的余额不足，请充值后再试。")
            _log_group.info(f"用户余额不足：{user_info['username']}，ID：{user_id}")
            return

        # 扣除一次余额并保存
        self.users[user_id]['balance'] -= 1
        self.save_users()
        _log_group.info(f"群消息：{content}")
        _log_at.info(f"用户ID：{user_id}，用户名：{user_info['username']}，余额：{user_info['balance']}，内容：{content}")

        # 调用响应函数处理消息
        try:
            response = self.response_function(content)
            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=response
            )
        except Exception as e:
            _log_group.error(f"发送群消息失败：{e}")

    async def on_at_message_create(self, message: Message):
        """
        处理频道内的@消息，不涉及用户注册。
        """
        try:
            cleaned_content = re.sub(r"<@!?\d+>", "", message.content).strip()
            user_name = message.author.username
            _log_at.info(f"频道内用户{user_name}消息：{cleaned_content}")

            # 处理控制命令
            if cleaned_content.lower() == "/xunfei":
                self.response_function = xfly
                _log_at.info(f"频道用户 {user_name} 切换到 xunfei 模式")
                await message.reply(content="已切换到 xunfei 模式")
            elif cleaned_content.lower() == "/kimi":
                self.response_function = chat
                _log_at.info(f"频道用户 {user_name} 切换到 kimi 模式")
                await message.reply(content="已切换到 kimi 模式")
            elif cleaned_content.lower() == "/ai360":
                self.response_function = chat1
                _log_at.info(f"频道用户 {user_name} 切换到 ai360 模式")
                await message.reply(content="已切换到 ai360 模式")
            elif cleaned_content.lower() == "start":
                self.listening = True
                await message.reply(content="开始监听群消息")
            elif cleaned_content.lower() == "stop":
                self.listening = False
                await message.reply(content="停止监听群消息")
            else:
                # 使用当前模式的响应函数处理消息
                response = self.response_function(cleaned_content)
                await message.reply(content=f"[bot]:{self.robot.name}->[user]:{user_name}\n------\n{response}")

        except Exception as e:
            _log_at.error(f"处理@消息失败：{e}")


if __name__ == "__main__":
    intents = botpy.Intents(public_messages=True, public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])
