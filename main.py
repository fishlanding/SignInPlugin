from pkg.platform.types import MessageChain, Image
from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import PersonMessageReceived, GroupMessageReceived
import re
from plugins.SignInPlugin.api.signin_manager import SignInManager
from plugins.SignInPlugin.api.image_fetcher import ImageFetcher
import random
import datetime

@register(name="SignInPlugin", description="普通的签到插件", version="0.1", author="YuWan_SAMA")
class SignInPlugin(BasePlugin):
    def __init__(self, host: APIHost):
        self.signin_manager = SignInManager()
        self.image_fetcher = ImageFetcher()
        self.fortunes = [
            "大吉: 今天是幸运的一天，抓住机会！",
            "吉: 顺利的一天，保持好心情。",
            "中吉: 稳扎稳打，会有收获。",
            "小吉: 小心谨慎，平稳度过。",
            "末吉: 低调行事，避免麻烦。",
            "凶: 保持冷静，谨慎决策。"
        ]

    async def initialize(self):
        await self.signin_manager.load_records()

    @handler(PersonMessageReceived)
    @handler(GroupMessageReceived)
    async def message_received(self, ctx: EventContext):
        msg = str(ctx.event.message_chain).strip()
        if re.search(r'/签到', msg, re.IGNORECASE):
            ctx.prevent_default()
            user_id = str(ctx.event.sender_id)
            launcher_id = str(ctx.event.launcher_id)
            launcher_type = ctx.event.launcher_type

            # 获取发送者昵称，区分私聊和群聊
            if isinstance(ctx.event, PersonMessageReceived):
                nickname = ctx.event.sender.nickname
            else:  # GroupMessageReceived
                nickname = getattr(ctx.event, 'sender_name', None) or getattr(ctx.event, 'sender', {}).get('nickname', f"用户{user_id}")

            today = datetime.date.today().isoformat()
            if self.signin_manager.has_signed_in(user_id, today):
                await ctx.send_message(launcher_type, launcher_id, MessageChain([
                    f"@{nickname} 你今天已经签到过了！明天再来吧！"
                ]))
                return

            try:
                img_info = await self.image_fetcher.get_random_image()
                self.signin_manager.record_signin(user_id, today)
                fortune = random.choice(self.fortunes)
                
                await ctx.send_message(launcher_type, launcher_id, MessageChain([
                    f"@{nickname}\n",
                    Image(url=img_info['url']),
                    f"今日运势：{fortune}"
                ]))
                self.ap.logger.info(f"User {user_id} signed in successfully")
            except Exception as e:
                await ctx.send_message(launcher_type, launcher_id, MessageChain([
                    f"签到失败：{str(e)}"
                ]))
                self.ap.logger.error(f"Sign-in error for user {user_id}: {str(e)}")

    def __del__(self):
        pass