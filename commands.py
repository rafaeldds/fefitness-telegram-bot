import json
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton
)
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    filters,
    CommandHandler,
    ConversationHandler
)
from reclamacao_flow import (
    receber_resposta,
    receber_nome,
    receber_reclamacao,
    receber_email,
    receber_telefone,
    cancel,
    AGUARDANDO_EMAIL,
    AGUARDANDO_NOME,
    AGUARDANDO_RECLAMACAO,
    AGUARDANDO_RESPOSTA,
    AGUARDANDO_TELEFONE
)

with open("catalog.json", "r", encoding="utf-8") as file:
    CATALOG = json.load(file)


def desligar_menu_catalog_opened(func):
    async def wrapper(
            update: Update,
            context: ContextTypes.DEFAULT_TYPE,
            *args,
            **kwargs
    ):
        if context.user_data.get('menu_catalog_opened'):
            context.user_data['menu_catalog_opened'] = False
        if context.user_data.get('menu_reclamacao'):
            context.user_data['menu_reclamacao'] = False
        return await func(update, context, *args, **kwargs)
    return wrapper


async def products_catalog(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:

    categories = list(CATALOG.keys())

    keyboard = [[f"{i+1}. {categories[i]}" for i in range(len(categories))]]
    menu = "\n".join(
        [f"{i+1}. {categories[i]}" for i in range(len(categories))])

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        f"Por favor, escolha uma opção:\n{menu}",
        reply_markup=reply_markup
    )
    context.user_data['menu_catalog_opened'] = True
    return -1


async def catalog_option(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> True:

    if not context.user_data.get('menu_catalog_opened'):
        return

    text = update.message.text.split(". ")[1]

    products = CATALOG.get(text)
    if products:
        for description, image_path in products.items():
            with open(image_path, "rb") as image_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=image_file,
                    caption=description
                )
    else:
        await update.message.reply_text(
            "Opção inválida. Por favor, use uma das opcoes fornecidas."
        )
    return -1


@desligar_menu_catalog_opened
async def start(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        fr"Olá, {user.mention_html()}! Bem-vindo ao bot da loja FeFitness.")


@desligar_menu_catalog_opened
async def help(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "1. /catalogo_produtos\n"
        + " Use essa opcao para poder consultar nosso catalogo de produtos\n\n"
        + " 2. /deixe_sua_mensagem\n"
        + " Use essa opcao para nos deixar uma mensagem\n\n"
        + " 3. /ajuda\n"
        + " Use essa opcao para obter ajuda com relacao ao menu\n",
        reply_markup=ReplyKeyboardRemove()
    )
    return -1


@desligar_menu_catalog_opened
async def reclamacao(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[KeyboardButton("Sim"), KeyboardButton("Não")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "Deseja nos enviar uma reclamação?",
        reply_markup=reply_markup
    )

    return AGUARDANDO_RESPOSTA

reclamacao_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('reclamacao', reclamacao)],
    states={
        AGUARDANDO_RESPOSTA: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, receber_resposta)],
        AGUARDANDO_NOME: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, receber_nome)],
        AGUARDANDO_TELEFONE: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, receber_telefone)],
        AGUARDANDO_EMAIL: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, receber_email)],
        AGUARDANDO_RECLAMACAO: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, receber_reclamacao)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
