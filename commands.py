import json
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    filters,
    CommandHandler,
    ConversationHandler
)
from leave_message_flow import (
    dsm_menu_options,
    lmsg_receive_menu,
    lmsg_receive_name,
    lmsg_receive_email_text,
    lmsg_receive_email,
    lmsg_receive_tel_number,
    cancel,
    LMSG_WAIT_EMAIL,
    LMSG_WAIT_NAME,
    LMSG_WAIT_EMAIL_TEXT,
    LMSG_WAIT_MENU,
    LMSG_WAIT_TEL_NUMBER
)

with open("catalog.json", "r", encoding="utf-8") as file:
    CATALOG = json.load(file)


def update_opened_menus(func):
    async def wrapper(
            update: Update,
            context: ContextTypes.DEFAULT_TYPE,
            *args,
            **kwargs
    ):
        if context.user_data.get('menu_catalog_opened'):
            context.user_data['menu_catalog_opened'] = False
        if context.user_data.get('menu_leave_message'):
            context.user_data['menu_leave_message'] = False
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


@update_opened_menus
async def start(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        fr"Olá, {user.mention_html()}! Bem-vindo ao bot da loja FeFitness.")


@update_opened_menus
async def help(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['menu_leave_message'] = False
    await update.message.reply_text(
        "1. /catalogo_produtos\n"
        + "- Use essa opcao para poder consultar nosso catalogo de produtos\n\n"
        + " 2. /deixe_sua_mensagem\n"
        + "- Use essa opcao para nos deixar uma mensagem\n\n"
        + " 3. /ajuda\n"
        + "- Use essa opcao para obter ajuda com relacao ao menu\n",
        reply_markup=ReplyKeyboardRemove()
    )
    return -1


@update_opened_menus
async def lmsg_menu(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:

    printed_menu = "\n".join(
        [f"{i+1}. {dsm_menu_options[i]}" for i in range(len(dsm_menu_options))])

    keyboard = [
        [f"{i+1}. {dsm_menu_options[i]}" for i in range(len(dsm_menu_options))]]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        f"Deseja nos deixar que tipo de mensagem?\n{printed_menu} ",
        reply_markup=reply_markup
    )

    context.user_data['menu_leave_message'] = True

    return LMSG_WAIT_MENU

leave_message_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler(
        "deixe_sua_mensagem", lmsg_menu)],
    states={
        LMSG_WAIT_MENU: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, lmsg_receive_menu)],
        LMSG_WAIT_NAME: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, lmsg_receive_name)],
        LMSG_WAIT_TEL_NUMBER: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, lmsg_receive_tel_number)],
        LMSG_WAIT_EMAIL: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, lmsg_receive_email)],
        LMSG_WAIT_EMAIL_TEXT: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, lmsg_receive_email_text)]
    },
    fallbacks=[
        CommandHandler('cancel', cancel)
    ]
)
