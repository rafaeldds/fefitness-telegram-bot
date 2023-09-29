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
        if context.user_data.get('menu_reclamacao'):
            context.user_data['menu_reclamacao'] = False
        return await func(update, context, *args, **kwargs)
    return wrapper


async def vendas(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:

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
    return -1


async def vendas_catalogo(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> True:

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
    return -1


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


@desligar_menu_vendas
async def parceria(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Se você está interessado em uma parceria, "
        + "entre em contato conosco para discutir as oportunidades.",
        reply_markup=ReplyKeyboardRemove()
    )
    return -1


@desligar_menu_vendas
async def mensagem(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Você pode deixar uma mensagem aqui. "
        + "Estamos ansiosos para ouvir de você!",
        reply_markup=ReplyKeyboardRemove()
    )
    return -1


@desligar_menu_vendas
async def sugestao(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Se você tiver uma sugestão, "
        + "sinta-se à vontade para compartilhá-la conosco.",
        reply_markup=ReplyKeyboardRemove()
    )
    return -1


@desligar_menu_vendas
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
