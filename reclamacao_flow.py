from telegram import (Update, ReplyKeyboardRemove)
from telegram.ext import (ContextTypes)
from utils import (send_email)

AGUARDANDO_RESPOSTA = 0
AGUARDANDO_NOME = 1
AGUARDANDO_TELEFONE = 2
AGUARDANDO_EMAIL = 3
AGUARDANDO_RECLAMACAO = 4


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Processo de reclamação cancelado.",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()


async def check_if_user_still_here(update, context) -> bool:
    rtn: bool = False
    if not context.user_data.get('menu_reclamacao'):
        await cancel(update, context)
        rtn = True
    return rtn


async def receber_resposta(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    resposta = update.message.text
    if resposta == "Não":
        await update.message.reply_text(
            "Tudo bem! Se precisar, estamos aqui.",
            reply_markup=ReplyKeyboardRemove()
        )
        return -1
    if resposta == "Sim":
        context.user_data['menu_reclamacao'] = True
        await update.message.reply_text(
            "Qual o seu nome completo?",
            reply_markup=ReplyKeyboardRemove()
        )
        return AGUARDANDO_NOME
    return -1


async def receber_nome(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    nome = update.message.text
    context.user_data['nome'] = nome

    if await check_if_user_still_here(update, context):
        return -1

    await update.message.reply_text(
        "Qual o seu número de telefone caso necessitarmos entrar em contato?"
    )
    return AGUARDANDO_TELEFONE


async def receber_telefone(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    telefone = update.message.text
    context.user_data['telefone'] = telefone

    if await check_if_user_still_here(update, context):
        return -1

    await update.message.reply_text("Qual o seu e-mail?")
    return AGUARDANDO_EMAIL


async def receber_email(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    email = update.message.text
    context.user_data['email'] = email

    if await check_if_user_still_here(update, context):
        return -1

    await update.message.reply_text(
        "Agora, por favor, digite sua reclamação em apenas uma mensagem."
    )
    return AGUARDANDO_RECLAMACAO


async def receber_reclamacao(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    reclamacao = update.message.text
    nome = context.user_data.get('nome', "Desconhecido")
    telefone = context.user_data.get('telefone', "Desconhecido")
    email = context.user_data.get('email', "Desconhecido")

    corpo_email = f"Reclamação de {nome}:\n\n{reclamacao}\n\nContato:\nTelefone: {telefone}\nEmail: {email}"
    send_email("RECLAMAÇÃO", corpo_email)

    if await check_if_user_still_here(update, context):
        return -1

    await update.message.reply_text(
        "Sua reclamação foi enviada com sucesso e iremos responder assim que possível!"
    )
    context.user_data.clear()
    return -1
