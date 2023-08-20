from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json


async def vendas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["1. Calcas", "2. Camisas"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Por favor, escolha uma opção: \n1. Calcas \n2. Camisas", reply_markup=reply_markup)

    # Defina uma variável no contexto para saber que o usuário está esperando a seleção
    context.user_data['esperando_selecao'] = True


async def opcao_escolhida(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Verifique se o usuário está esperando pela seleção. Se não estiver, apenas retorne
    if not context.user_data.get('esperando_selecao'):
        return

    text = update.message.text

    # Primeiro, vamos criar um dicionário para associar o nome das calças a seus arquivos de imagem:
    calcados = {
        "1. Calca 1": "assets/calca1.png",
        "2. Calca 2": "assets/calca2.jpeg",
        "3. Calca 3": "assets/calca3.jpeg"
    }

    if text == "1" or text == "1. Calcas":
        for descricao, caminho_imagem in calcados.items():
            with open(caminho_imagem, "rb") as image_file:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_file, caption=descricao)
    elif text == "2" or text == "2. Camisas":
        resposta = "\n".join([
            "1. Camisa 1",
            "2. Camisa 2",
            "3. Camisa 3"
        ])
        await update.message.reply_text(resposta)
    else:
        resposta = "Opção não reconhecida. Por favor, use uma das opcoes fornecidas."
        await update.message.reply_text(resposta)

    # Após a seleção, resete a variável de contexto
    context.user_data['esperando_selecao'] = False


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["TELEGRAM_BOT_TOKEN"]

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("vendas", vendas))
app.add_handler(MessageHandler(
    filters.TEXT & ~filters.COMMAND, opcao_escolhida))

app.run_polling()
