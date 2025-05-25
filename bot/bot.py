import json
from typing import Final
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, filters

with open('../configs/telegram.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN: Final = config['TOKEN']

# Command Handler
from handlers.start_handler import start_command
from handlers.button_handler import button_command
from handlers.message_handler import message_command

if __name__ == '__main__':
    print('MyAry BOT is running')
    app = Application.builder().token(TOKEN).build()

    # Command
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CallbackQueryHandler(button_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_command))

    print('Polling...')
    app.run_polling(poll_interval=1)