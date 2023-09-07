from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json

# Função para exibir o menu vendas
async def vendas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["1. Calcas", "2. Shorts", "3. Blusinhas", "4. Tops", "5. Casacos"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Por favor, escolha uma opção: \n1. Calcas \n2. Shorts \n3. Blusinhas \n4. Tops \n5. Casacos", reply_markup=reply_markup)

    # Defina uma variável no contexto para saber que o usuário está esperando a seleção
    context.user_data['esperando_selecao'] = True

async def opcao_escolhida(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Verifique se o usuário está esperando pela seleção. Se não estiver, apenas retorne
    if not context.user_data.get('esperando_selecao'):
        return

    text = update.message.text

    # Dicionário para associar o nome do produto a seus arquivos de imagem:
    Calca = {
        "1. Legging-jacar": "assets/Calca/Legging-jacar.jpg",
        "2. Legging-new-vision": "assets/Calca/Legging-new-vision.jpg",
        "3. Legging-wonder": "assets/Calca/Legging-wonder.jpg",
    }
    Short = {
        "1. Short-blackout": "assets/Short/Short-blackout.jpg",
        "2. Short-cordao": "assets/Short/Short-cordao.jpg",
        "3. Short-jacar": "assets/Short/Short-jacar.jpg",
    }
    Blusinha = {
        "1. Legging-jacar": "assets/Calca/Legging-jacar.jpg",
        "2. Legging-new-vision": "assets/Calca/Legging-new-vision.jpg",
        "3. Legging-wonder": "assets/Calca/Legging-wonder.jpg",
    }
    Top = {
        "1. Top-basico": "assets/Top/Top-basico.jpg",
        "2. Top-jade": "assets/Top/Top-jade.jpg",
    }
    Casaco = {
        "1. Casaco-corta-vento": "assets/Casaco/Casaco-corta-vento.jpg",
        "2. Casaco-poliamida": "assets/Casaco/Casaco-poliamida.jpg",
    }
    

    if text == "1" or text == "1. Calcas":
        for descricao, caminho_imagem in Calca.items():
            with open(caminho_imagem, "rb") as image_file:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_file, caption=descricao)
        
    elif text == "2" or text == "2. Shorts":
        for descricao, caminho_imagem in Short.items():
            with open(caminho_imagem, "rb") as image_file:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_file, caption=descricao)
        
    elif text == "3" or text == "3. Blusinhas":
        for descricao, caminho_imagem in Blusinha.items():
            with open(caminho_imagem, "rb") as image_file:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_file, caption=descricao)
        
    elif text == "4" or text == "4. Tops":
        for descricao, caminho_imagem in Top.items():
            with open(caminho_imagem, "rb") as image_file:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_file, caption=descricao)
        
    elif text == "5" or text == "5. Casacos":
        for descricao, caminho_imagem in Casaco.items():
            with open(caminho_imagem, "rb") as image_file:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_file, caption=descricao)
        
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