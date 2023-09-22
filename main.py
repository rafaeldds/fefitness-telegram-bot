import json
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)
from commands import (
    start,
    ajuda,
    vendas,
    parceria,
    mensagem,
    sugestao,
    vendas_catalogo,
    reclamacao_conversation_handler
)


with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

TOKEN = config["TELEGRAM_BOT_TOKEN"]

app = ApplicationBuilder().token(TOKEN).build()


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
