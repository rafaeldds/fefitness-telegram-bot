import json
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)
from commands import (
    start,
    ajuda,
    vendas,
    parceria,
    mensagem,
    sugestao,
    reclamacao,
    vendas_catalogo
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

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

TOKEN = config["TELEGRAM_BOT_TOKEN"]

app = ApplicationBuilder().token(TOKEN).build()

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

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ajuda", ajuda))
app.add_handler(CommandHandler("vendas", vendas))
app.add_handler(CommandHandler("parceria", parceria))
app.add_handler(CommandHandler("mensagem", mensagem))
app.add_handler(CommandHandler("sugestao", sugestao))

app.add_handler(reclamacao_conversation_handler)

app.add_handler(MessageHandler(
    filters.TEXT & ~filters.COMMAND, vendas_catalogo))

app.run_polling()
