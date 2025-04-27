from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import GroupMessageReceived
from pkg.platform.types import *
import re
from plugins.SignInPlugin.api.signin_manager import SignInManager
from plugins.SignInPlugin.api.image_fetcher import ImageFetcher
from plugins.SignInPlugin.api.fortunes import get_fortune
import datetime

@register(name="SignInPlugin", description="普通的签到插件", version="0.2.1", author="YuWan_SAMA")
class SignInPlugin(BasePlugin):
    def __init__(self, host: APIHost):
        self.signin_manager = SignInManager()
        self.image_fetcher = ImageFetcher()

    async def initialize(self):
        await self.signin_manager.load_records()

    @handler(GroupMessageReceived)
    async def message_received(self, ctx: EventContext):
        msg = str(ctx.event.message_chain).strip()
        if re.search(r'/签到', msg, re.IGNORECASE):
            ctx.prevent_default()
            user_id = str(ctx.event.sender_id)
            launcher_id = str(ctx.event.launcher_id)
            launcher_type = ctx.event.launcher_type
            nickname = f"{user_id}"

            today = datetime.date.today().isoformat()
            if self.signin_manager.has_signed_in(user_id, today):
                await ctx.send_message(launcher_type, launcher_id, MessageChain([
                    At(nickname),
                    f"你今天已经签到过了！明天再来吧！"
                ]))
                return

            try:
                img_info = await self.image_fetcher.get_random_image()
                self.signin_manager.record_signin(user_id, today)
                fortune = get_fortune()
                
                await ctx.send_message(launcher_type, launcher_id, MessageChain([
                    At(nickname),
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