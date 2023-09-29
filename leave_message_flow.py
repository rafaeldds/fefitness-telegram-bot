from telegram import (Update, ReplyKeyboardRemove)
from telegram.ext import (ContextTypes)
from utils import (send_email)

LMSG_WAIT_MENU = 0
LMSG_WAIT_NAME = 1
LMSG_WAIT_TEL_NUMBER = 2
LMSG_WAIT_EMAIL = 3
LMSG_WAIT_EMAIL_TEXT = 4

dsm_menu_options = [
    "Sugestao",
    "Reclamacao",
    "Parcerias",
    "Intencao de Compra"
]


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "O processo de reclamação foi cancelado!\n\n"
        + "Volte ao menu /deixe_sua_mensagem"
        + "caso deseje iniciar o processo novamente.",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return -1


async def check_if_user_still_here(update, context) -> bool:
    rtn: bool = False
    if not context.user_data.get('menu_leave_message'):
        await cancel(update, context)
        rtn = True
    return rtn


async def lmsg_receive_menu(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    if await check_if_user_still_here(update, context):
        return -1

    try:
        text = update.message.text.split(". ")[1]
    except IndexError:
        text = update.message.text

    if text in dsm_menu_options:
        context.user_data['email_user_menu_title'] = text
        await update.message.reply_text(
            "Okay, vamos precisar de mais algumas informacoes!\n\n"
            + "Por favor, agora nos diga seu nome pra entrarmos em contato.",
            reply_markup=ReplyKeyboardRemove()
        )
        return LMSG_WAIT_NAME

    await update.message.reply_text(
        "Opcao Invalida. \n"
        + "Se precisar nos deixar uma mensagem, estamos aqui.\n"
        + "E so nos chamar de novo no menu /deixe_sua_mensagem"
        + " para recomecarmos.",
        reply_markup=ReplyKeyboardRemove()
    )
    return -1


async def lmsg_receive_name(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    if await check_if_user_still_here(update, context):
        return -1

    context.user_data['email_user_name'] = update.message.text

    await update.message.reply_text(
        "Qual o seu número de telefone caso necessitarmos entrar em contato?"
    )
    return LMSG_WAIT_TEL_NUMBER


async def lmsg_receive_tel_number(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    if await check_if_user_still_here(update, context):
        return -1

    context.user_data['email_user_tel_number'] = update.message.text

    await update.message.reply_text("Qual o seu e-mail?")
    return LMSG_WAIT_EMAIL


async def lmsg_receive_email(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    if await check_if_user_still_here(update, context):
        return -1

    context.user_data['email_user_email'] = update.message.text

    await update.message.reply_text(
        "Agora, por favor, digite sua reclamação em apenas uma mensagem."
    )
    return LMSG_WAIT_EMAIL_TEXT


async def lmsg_receive_email_text(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    if await check_if_user_still_here(update, context):
        return -1

    user_tittle = context.user_data.get(
        'email_user_menu_title', "Desconhecido")
    user_name = context.user_data.get('email_user_name', "Desconhecido")
    user_tel_number = context.user_data.get(
        'email_user_tel_number', "Desconhecido")
    user_email = context.user_data.get('email_user_email', "Desconhecido")
    user_message = update.message.text
    corpo_email = (
        f"{user_tittle} de {user_name}:\n\n"
        f"{user_message}\n\n"
        f"Telefone: {user_tel_number}\n"
        f"Email: {user_email}"
    )

    send_email(f"[FeFitness Bot] - [{user_tittle}] - {user_name}", corpo_email)
    await update.message.reply_text(
        "Muito obrigado por sua mensagem!\n"
        + "Iremos responder assim que possível!"
    )

    context.user_data.clear()
    return -1
