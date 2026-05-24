import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# إعداد السجلات (Logs)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# سحب التوكن من إعدادات السيرفر
TOKEN = os.environ.get("TOKEN")

# متغيرات لحفظ حالة البوت (هنا يفضل مستقبلاً استخدام قاعدة بيانات)
user_data = {"message": "أهلاً بك!", "interval": 60}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("البوت يعمل الآن! استخدم /setmsg لتغيير الرسالة و /settime لتغيير الوقت.")

async def setmsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        user_data["message"] = " ".join(context.args)
        await update.message.reply_text(f"تم تغيير الرسالة إلى: {user_data['message']}")
    else:
        await update.message.reply_text("أرسل الأمر متبوعاً بالرسالة، مثل: /setmsg Hello")

async def settime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args and context.args[0].isdigit():
        user_data["interval"] = int(context.args[0])
        await update.message.reply_text(f"تم تغيير الوقت إلى: {user_data['interval']} ثانية")
    else:
        await update.message.reply_text("أرسل الوقت بالثواني، مثل: /settime 30")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("setmsg", setmsg))
    application.add_handler(CommandHandler("settime", settime))
    
    print("البوت يعمل الآن...")
    application.run_polling()
