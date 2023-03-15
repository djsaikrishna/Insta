# -*- coding: utf-8 -*-
# DONT_REMOVE_THIS
#  TheDarkW3b (c)

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ParseMode, Update
import logging
import requests
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',

                    level=logging.INFO)

#Logger Setup
logger = logging.getLogger(__name__)

TOKEN = "6200080434:AAE_HowNjNOvFzxAu_ffFyYjj0YCln9m_Ec"

def download(update: Update, context: CallbackContext):
    message = update.effective_message
    instagram_post = message.text
    if instagram_post=="/start":
        context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        update.message.reply_text("Welcome to <b>InstaGram Downloader</b>! \n\nWhat's This Bot Can Do? \n\nI can download any Instagram public post by valid link of that post! Just send me the link of public post of telegram\n\nVideos must be less than 50MB, For Now it Cannot Support Long Videos\n\n<b>Support Group :-</b> @TheDeadlyBots \n <b> Update Channel :- </b> @TheBotUpdates", parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    else:
        pass
    if "instagram.com" in instagram_post:
        changing_url = instagram_post.split("/")
        url_code = changing_url[4]
        url = f"https://instagram.com/p/{url_code}?__a=1"
        try:
            global checking_video
            visit = requests.get(url).json()
            checking_video = visit['graphql']['shortcode_media']['is_video']
        except:
            context.bot.sendMessage(chat_id=update.message.chat_id, text="Sorry i think the post is not available or is private so please send me public post link only ⚡️")
        
        if checking_video==True:
            try:
                video_url = visit['graphql']['shortcode_media']['video_url']
                context.bot.send_chat_action(chat_id=update.message.chat_id, action="upload_video")
                context.bot.sendVideo(chat_id=update.message.chat_id, video=video_url)
            except:
                pass

        elif checking_video==False:
            try:
                post_url = visit['graphql']['shortcode_media']['display_url']
                context.bot.send_chat_action(chat_id=update.message.chat_id, action="upload_photo")
                context.bot.sendPhoto(chat_id=update.message.chat_id, photo=post_url)
            except:
                pass
        else:
            context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
            context.bot.sendMessage(chat_id=update.message.chat_id, text="I Cant download and send Private Posts :-( ")
    else:
        context.bot.sendMessage(chat_id=update.message.chat_id, text="Kindly send me link of Instagram public post private not allowed ")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    logger.info("Setting Up MessageHandler")
    dp.add_handler(MessageHandler(Filters.text, download))
    updater.start_polling()
    logging.info("Starting Long Polling!")
    updater.idle()

if __name__ == "__main__":
    main()
