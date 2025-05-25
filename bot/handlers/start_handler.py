from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = main_menu_keyboard()
    userId = update.message.from_user.id

    await update.message.reply_text(
        f"Welcome to MyAry!\n",
        reply_markup=reply_markup
    )

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Getting Started", callback_data='1')],
    ]
    return InlineKeyboardMarkup(keyboard)