import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

# 1. إعداد سجلات الخطأ (Logs) - هذه ضرورية جداً لنرى الأخطاء في Railway
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 2. سحب التوكن من الـ Variables التي أضفتها في Railway
TOKEN = os.environ.get("TOKEN")

# دالة الأمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("البوت يعمل الآن بنجاح على السيرفر!")

if __name__ == '__main__':
    # التأكد من وجود التوكن قبل التشغيل
    if not TOKEN:
        print("خطأ: لم يتم العثور على التوكن في المتغيرات (Variables)!")
    else:
        # بناء البوت باستخدام التوكن المسحوب من المتغيرات
        application = ApplicationBuilder().token(TOKEN).build()
        
        # إضافة الأوامر
        application.add_handler(CommandHandler("start", start))
        
        print("البوت بدأ العمل بنجاح...")
        
        # تشغيل البوت (Polling)
        application.run_polling()
