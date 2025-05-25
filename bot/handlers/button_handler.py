from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
    
async def button_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    userTeleId = query.from_user.id
        
    if query.data == '2':
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(chat_id=query.message.chat_id, text="How was your day?", reply_markup=reply_markup)