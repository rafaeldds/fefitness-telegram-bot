from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json

# Função para exibir o menu vendas


async def vendas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["1. calcas", "2. shorts", "3. blusinhas", "4. tops", "5. casacos"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Por favor, escolha uma opção: \n1. calcas \n2. shorts \n3. blusinhas \n4. tops \n5. casacos", reply_markup=reply_markup)

    # Defina uma variável no contexto para saber que o usuário está esperando a seleção
    context.user_data['esperando_selecao'] = True


async def opcao_escolhida(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Verifique se o usuário está esperando pela seleção. Se não estiver, apenas retorne
    if not context.user_data.get('esperando_selecao'):
        return

    text = update.message.text

    # Dicionário para associar o nome do produto a seus arquivos de imagem:
    calca = {
        "1. legging-jacar": "assets/calca/legging-jacar.jpg",
        "2. legging-new-vision": "assets/calca/legging-new-vision.jpg",
        "3. legging-wonder": "assets/calca/legging-wonder.jpg",
    }
    short = {
        "1. short-blackout": "assets/short/short-blackout.jpg",
        "2. short-cordao": "assets/short/short-cordao.jpg",
        "3. short-jacar": "assets/short/short-jacar.jpg",
    }
    blusinha = {
        "1. legging-jacar": "assets/calca/legging-jacar.jpg",
        "2. legging-new-vision": "assets/calca/legging-new-vision.jpg",
        "3. legging-wonder": "assets/calca/legging-wonder.jpg",
    }
    top = {
        "1. top-basico": "assets/top/top-basico.jpg",
        "2. top-jade": "assets/top/top-jade.jpg",
    }
    casaco = {
        "1. casaco-corta-vento": "assets/casaco/casaco-corta-vento.jpg",
        "2. casaco-poliamida": "assets/casaco/casaco-poliamida.jpg",
    }

    if text == "1" or text == "1. calcas":
        for descricao, caminho_imagem in calca.items():
            with open(caminho_imagem, "rb") as image_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=image_file,
                    caption=descricao
                )

    elif text == "2" or text == "2. shorts":
        for descricao, caminho_imagem in short.items():
            with open(caminho_imagem, "rb") as image_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=image_file,
                    caption=descricao
                )

    elif text == "3" or text == "3. blusinhas":
        for descricao, caminho_imagem in blusinha.items():
            with open(caminho_imagem, "rb") as image_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=image_file,
                    caption=descricao
                )

    elif text == "4" or text == "4. tops":
        for descricao, caminho_imagem in top.items():
            with open(caminho_imagem, "rb") as image_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=image_file,
                    caption=descricao
                )

    elif text == "5" or text == "5. casacos":
        for descricao, caminho_imagem in casaco.items():
            with open(caminho_imagem, "rb") as image_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=image_file,
                    caption=descricao
                )

    else:
        resposta = "Opção inválida. Por favor, use uma das opcoes fornecidas."
        await update.message.reply_text(resposta)

    # Após a seleção, resete a variável de contexto
    context.user_data['esperando_selecao'] = False

# Função para exibir o menu iniciar


async def iniciar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        fr"Olá, {user.mention_html()}! Bem-vindo ao bot da loja FeFitness.")

# Função para exibir o menu ajuda


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Como podemos te ajudar?")

# Função para exibir o menu parceria


async def parceria(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Se você está interessado em uma parceria, entre em contato conosco para discutir as oportunidades.")

# Função para exibir o menu deixe sua mensagem


async def mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Você pode deixar uma mensagem aqui. Estamos ansiosos para ouvir de você!")

# Função para exibir o menu sugestão


async def sugestao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Se você tiver uma sugestão, sinta-se à vontade para compartilhá-la conosco.")

# Função para exibir o menu reclamação


async def reclamacao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Se você tiver uma reclamação, sinta-se à vontade para compartilhá-la conosco.")

with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["TELEGRAM_BOT_TOKEN"]

app = ApplicationBuilder().token(TOKEN).build()

# Manipuladores de comando para os comandos personalizados
app.add_handler(CommandHandler("iniciar", iniciar))
app.add_handler(CommandHandler("ajuda", ajuda))
app.add_handler(CommandHandler("vendas", vendas))
app.add_handler(CommandHandler("parceria", parceria))
app.add_handler(CommandHandler("mensagem", mensagem))
app.add_handler(CommandHandler("sugestao", sugestao))
app.add_handler(CommandHandler("reclamacao", reclamacao))
app.add_handler(MessageHandler(
    filters.TEXT & ~filters.COMMAND, opcao_escolhida))

app.run_polling()
