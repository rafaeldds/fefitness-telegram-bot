import json
from telegram import (Update, ReplyKeyboardMarkup,
                      ReplyKeyboardRemove, KeyboardButton)
from telegram.ext import (ContextTypes)
from reclamacao_flow import (AGUARDANDO_RESPOSTA)

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
        "Como podemos te ajudar?",
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
