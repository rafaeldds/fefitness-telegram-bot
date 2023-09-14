import json
from telegram import (Update, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

with open("catalogo.json", "r", encoding="utf-8") as file:
    CATALOGO = json.load(file)


def desligar_menu_vendas(func):
    async def wrapper(
            update: Update,
            context: ContextTypes.DEFAULT_TYPE,
            *args,
            **kwargs
    ):
        if context.user_data.get('menu_vendas'):
            context.user_data['menu_vendas'] = False
            await update.message.reply_text(
                "Para voltar ao menu vendas, "
                + "digite /vendas, "
                + "ou acesso pelo menu interativo do chat.",
                reply_markup=ReplyKeyboardRemove()
            )
        return await func(update, context, *args, **kwargs)
    return wrapper


async def vendas(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> None:
    categorias = list(CATALOGO.keys())
    keyboard = [[f"{i+1}. {categorias[i]}" for i in range(len(categorias))]]
    menu = "\n".join(
        [f"{i+1}. {categorias[i]}" for i in range(len(categorias))])

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        f"Por favor, escolha uma opção:\n{menu}",
        reply_markup=reply_markup
    )
    context.user_data['menu_vendas'] = True


async def opcao_escolhida(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> None:

    if not context.user_data.get('menu_vendas'):
        return

    text = update.message.text.split(". ")[1]

    produtos = CATALOGO.get(text)
    if produtos:
        for descricao, caminho_imagem in produtos.items():
            with open(caminho_imagem, "rb") as image_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=image_file,
                    caption=descricao
                )
    else:
        resposta = "Opção inválida. Por favor, use uma das opcoes fornecidas."
        await update.message.reply_text(resposta)


@desligar_menu_vendas
async def start(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        fr"Olá, {user.mention_html()}! Bem-vindo ao bot da loja FeFitness.")


@desligar_menu_vendas
async def ajuda(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Como podemos te ajudar?"
    )


@desligar_menu_vendas
async def parceria(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Se você está interessado em uma parceria, "
        + "entre em contato conosco para discutir as oportunidades."
    )


@desligar_menu_vendas
async def mensagem(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Você pode deixar uma mensagem aqui. "
        + "Estamos ansiosos para ouvir de você!"
    )


@desligar_menu_vendas
async def sugestao(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Se você tiver uma sugestão, "
        + "sinta-se à vontade para compartilhá-la conosco."
    )


@desligar_menu_vendas
async def reclamacao(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Se você tiver uma reclamação, "
        + "sinta-se à vontade para compartilhá-la conosco."
    )

with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["TELEGRAM_BOT_TOKEN"]

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ajuda", ajuda))
app.add_handler(CommandHandler("vendas", vendas))
app.add_handler(CommandHandler("parceria", parceria))
app.add_handler(CommandHandler("mensagem", mensagem))
app.add_handler(CommandHandler("sugestao", sugestao))
app.add_handler(CommandHandler("reclamacao", reclamacao))
app.add_handler(MessageHandler(
    filters.TEXT & ~filters.COMMAND, opcao_escolhida))

app.run_polling()
