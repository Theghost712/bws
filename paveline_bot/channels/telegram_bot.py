import logging
from typing import Optional, Set

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from .. import config
from ..core.wish_service import generate_wishes
from ..db.repository import Repository

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self, token: str, admin_ids: Optional[Set[int]] = None):
        self.token = token
        self.admin_ids = admin_ids or set()
        self.repo = Repository()
        self.application: Optional[Application] = None

    def _is_admin(self, user_id: int) -> bool:
        try:
            return int(user_id) in self.admin_ids
        except Exception:
            return False

    # ------------------------------------------------------------------ helpers
    async def _send(self, context: ContextTypes.DEFAULT_TYPE, text: str, reply_markup=None) -> None:
        try:
            await context.bot.send_message(chat_id=context.chat_id, text=text, reply_markup=reply_markup)
        except Exception as e:
            logger.error(f"Telegram send failed: {e}")

    # ------------------------------------------------------------------ commands
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        text = "🎉 Welcome to the Paveline Bot! Make every birthday unforgettable."
        await self._send(context, text)

    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        text = (
            "/start - Start\n"
            "/help - Help\n"
            "/wish <name> - Generate a birthday wish\n"
            "/card <name> - Generate a birthday card\n"
            "/add - Add a birthday\n"
            "/list - List upcoming birthdays\n"
            "/remove - Remove a birthday\n"
            "/language <en|sw|fr|es|ar> - Set language\n"
            "/remind on|off - Toggle reminders\n"
            "/deleteme - Erase my data\n"
        )
        await self._send(context, text)

    async def cmd_wish(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        args = context.args
        name = args[0] if args else "friend"
        context.user_data["wish_name"] = name
        wishes = await generate_wishes(
            {
                "name": name,
                "relationship": "friend",
                "language": "en",
                "style": "heartfelt",
                "sender": "",
                "extra": "",
                "length": "medium",
                "age": None,
            },
            count=3,
        )
        text = f"Here are 3 wishes for {name}:"
        await self._send(context, text)
        for w in wishes:
            await self._send(context, w["text"])

    async def cmd_card(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        args = context.args
        name = args[0] if args else "friend"
        await self._send(context, f"Card generation for {name} coming soon.")

    async def cmd_add(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._send(context, "Use /add to register a birthday.")

    async def cmd_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._send(context, "Use /list to see upcoming birthdays.")

    async def cmd_remove(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._send(context, "Use /remove to delete a birthday.")

    async def cmd_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        args = context.args
        lang = args[0] if args else "en"
        context.user_data["language"] = lang
        await self._send(context, f"Language set to {lang}.")

    async def cmd_remind(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        args = context.args
        state = args[0] if args else "on"
        context.user_data["remind"] = state == "on"
        await self._send(context, f"Reminders turned {'on' if state == 'on' else 'off'}.")

    async def cmd_deleteme(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        if user and self._is_admin(user.id):
            await self._send(context, "Admin-only command.")
            return
        await self._send(context, "Use /deleteme to erase your data.")

    # ------------------------------------------------------------------ dispatch
    async def dispatch(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            if update.effective_user is None:
                return
            user_id = update.effective_user.id
            command = update.effective_message.text.split("@")[0].lstrip("/").split("@")[0].lower() if update.effective_message else ""
            handler = getattr(self, f"cmd_{command}", None) if command else None
            if handler is None:
                await self._send(context, "Unknown command. Use /help.")
                return
            if command in {"admin"} and not self._is_admin(user_id):
                await self._send(context, "Admins only.")
                return
            await handler(update, context)
        except Exception as e:
            logger.error(f"Bot error: {e}")
            try:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, something went wrong.")
            except Exception:
                pass

    def register_handlers(self) -> List[CommandHandler]:
        handlers = [
            CommandHandler("start", self.cmd_start),
            CommandHandler("help", self.cmd_help),
            CommandHandler("wish", self.cmd_wish),
            CommandHandler("card", self.cmd_card),
            CommandHandler("add", self.cmd_add),
            CommandHandler("list", self.cmd_list),
            CommandHandler("remove", self.cmd_remove),
            CommandHandler("language", self.cmd_language),
            CommandHandler("remind", self.cmd_remind),
            CommandHandler("deleteme", self.cmd_deleteme),
        ]
        return handlers
