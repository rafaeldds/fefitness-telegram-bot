from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '123456789:xxxxxxxxxxxxxxxxxxxx'
BOT_USERNAME: Final = '@yourbotname'

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Olá! Obrigado pela presença! Nós somos a Loja Fe Fitness!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Eu sou o robô da loja! Digite algo para que eu possa responder!')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Este é um comando personalizado!')

async def custom_command1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Este é um comando personalizado!')

# Responses
def handle_response(text: str) -> str:       # respostas de manipulação
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'

    if 'how are you' in processed:
        return 'I am good!'

    if "i love python!" in processed:
        return 'Remember to subscribe!'

    return 'I do not understand what you wrote...'

# Handling messages (Reponde os usuários)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    response: str = handle_response(text)
    
    print('Bot:', response)
    await update.message.reply_text(response)

# Trata dos erros
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('custom', custom_command1))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    # Errors
    app.add_error_handler(error)
    print('Polling...')
    app.run_polling(poll_interval=3)