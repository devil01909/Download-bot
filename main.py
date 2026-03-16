import os
import yt_dlp
import asyncio
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --- CONFIGURATION ---
TOKEN = "8712461675:AAFatMyWBaarVg2TO4E8WUl7cviK3slOqWo"

async def handle_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"): return
    
    status_msg = await update.message.reply_text("⚡ **Initializing High-Speed Download...**", parse_mode=constants.ParseMode.MARKDOWN)

    # স্পিড বাড়ানোর জন্য Advanced Options
    ydl_opts = {
        'format': 'best[ext=mp4]/best', 
        'outtmpl': 'video.mp4',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        # স্পিড বুস্ট সেটিংস
        'external_downloader_args': ['-n', '16'], # ১৬টি কানেকশন একসাথে কাজ করবে
        'buffersize': 1024*16,
        'retries': 10,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ভিডিওর ইনফো বের করা এবং ডাউনলোড (Fast Mode)
            info = await asyncio.to_thread(ydl.extract_info, url, download=True)
            title = info.get('title', 'Video')
            
            await status_msg.edit_text("📤 **Upload শুরু হচ্ছে...**", parse_mode=constants.ParseMode.MARKDOWN)
            
            # ভিডিও ফাইল পাঠানো
            with open('video.mp4', 'rb') as video:
                await update.message.reply_video(
                    video=video, 
                    caption=f"✅ **Title:** {title}\n\n⚡ *Downloaded by High-Speed Bot*",
                    supports_streaming=True,
                    parse_mode=constants.ParseMode.MARKDOWN
                )
            
            # ফাইল ডিলিট করে ফোন খালি করা
            if os.path.exists('video.mp4'):
                os.remove('video.mp4')
            await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"❌ **Error:** `{str(e)}`", parse_mode=constants.ParseMode.MARKDOWN)

if __name__ == '__main__':
    # বট স্টার্ট করার স্মার্ট পদ্ধতি
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_download))
    
    print("----------------------------")
    print("🚀 Speed Bot is Running!")
    print("----------------------------")
    
    app.run_polling()
