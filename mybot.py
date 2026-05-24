from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

TOKEN = "8911147590:AAEou9OR4RCQIckp8lFEm4mMzHGz0nTbv8w"

config = {
    "is_running": False,
    "message": "مرحباً! هذه رسالة تلقائية.",
    "interval": 10,
    "job": None
}

async def send_periodic_message(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await context.bot.send_message(chat_id=job.chat_id, text=config["message"])

async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if config["is_running"]:
        await update.message.reply_text("البوت يعمل بالفعل!")
        return
    
    config["is_running"] = True
    chat_id = update.effective_message.chat_id
    
    # إضافة وظيفة إرسال متكررة في الخلفية
    job = context.job_queue.run_repeating(send_periodic_message, interval=config["interval"], first=1, chat_id=chat_id)
    config["job"] = job
    await update.message.reply_text(f"تم التشغيل! سأرسل الرسالة كل {config['interval']} ثانية.")

async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if config["job"]:
        config["job"].schedule_removal()
        config["is_running"] = False
        await update.message.reply_text("تم إيقاف الإرسال التلقائي.")
    else:
        await update.message.reply_text("البوت متوقف أصلاً.")

async def set_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        config["message"] = " ".join(context.args)
        await update.message.reply_text(f"تم تغيير الرسالة.")

async def set_interval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        config["interval"] = int(context.args[0])
        await update.message.reply_text(f"تم تغيير الوقت. أوقف البوت وشغله لتطبيق الوقت الجديد.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("startbot", start_bot))
    app.add_handler(CommandHandler("stop", stop_bot))
    app.add_handler(CommandHandler("setmsg", set_message))
    app.add_handler(CommandHandler("settime", set_interval))
    
    print("البوت يعمل الآن...")
    app.run_polling()