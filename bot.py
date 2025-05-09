import os
from telegram.ext import ApplicationBuilder, CommandHandler
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
AUTHORIZED_CHAT_ID = int(os.getenv("AUTHORIZED_CHAT_ID"))

async def status(update, context):
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        await update.message.reply_text("Unauthorized access!")
        return
    await update.message.reply_text("✅ Der Raspberry Pi Zero läuft!")

async def shell(update, context):
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        await update.message.reply_text("Unauthorized access!")
        return

    command = ' '.join(context.args)
    if not command:
        await update.message.reply_text("Bitte einen Befehl angeben!")
        return

    result = os.popen(command).read()
    if not result:
        result = "Kein Output."
    await update.message.reply_text(f"```\n{result}\n```", parse_mode="Markdown")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("shell", shell))

    app.run_polling()