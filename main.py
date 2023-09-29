import json
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)
from commands import (
    start,
    help,
    products_catalog,
    catalog_option,
    leave_message_conversation_handler
)

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

TOKEN = config["TELEGRAM_BOT_TOKEN"]

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ajuda", help))
app.add_handler(CommandHandler("catalogo_produtos", products_catalog))
app.add_handler(leave_message_conversation_handler)
app.add_handler(MessageHandler(
    filters.TEXT & ~filters.COMMAND, catalog_option))

app.run_polling()
