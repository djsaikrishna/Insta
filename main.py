

import re
from datetime import datetime
from Reels import Insta, LoginError

from telegram import ParseMode
from telegram.ext import Updater, MessageHandler, CommandHandler

Pattern = r'(?:https?:\/\/)?(?:www\.)?instagram\.com\/(?:p|tv|reel)\/.+\/?'
Gram = Insta()


def log(text):
    print(f"| {datetime.now().strftime('%H:%M:%S')} | {text}")


def start(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "**Welcome to InstaGram Downloader Made By @GitExpert**!\n\n send an instagram url that contains a video to use this bot.\nVideos must be less than 50MB, For Now it Cannot Support Long Videos\n\n<b> Support Chat :-</b> @TheDeadlyBots"
    )


def processor(update, context):
    text = update.message.text    
    chat_id = update.message.chat_id
    name = update.message.chat.first_name
    username = update.message.chat.username
    message_id = update.message.message_id
        
    if not text:
        log(f"@{username} | {name} | {chat_id}\nRequest doesn't contain text, skipping...")
        return

    data = log(f'Request: {username} | {name} | {text}')
    result = re.search(Pattern, text)

    if not result:
        context.bot.send_message(
            chat_id = chat_id,
            reply_to_message_id = message_id,
            text = "I failed to found a Instagram url in your message.\nKindly send me link of Instagram public post private not allowed ",
            parse_mode = ParseMode.MARKDOWN
        )
        return
    
    try:
        video = Gram.VideoURL(result.group(0))
    except LoginError:
        context.bot.send_message(
            chat_id = chat_id,
            reply_to_message_id = message_id,
            text = "The Post is not available for public so Instagram API doesn't let me see this post without logging in.",
            parse_mode = ParseMode.MARKDOWN
        )
        return

    if video is not None:
        try:
            context.bot.send_video(
                chat_id = chat_id,
                video = video,
                reply_to_message_id = message_id,
                supports_streaming = True
            )
        except:
            context.bot.send_message(
                chat_id = chat_id,
                reply_to_message_id = message_id,
                text = f"Something's went wrong\ncannot send video but don't worry here is your download url of the post\n\n{video}"
            )
    else:
        context.bot.send_message(
            chat_id = chat_id,
            reply_to_message_id = message_id,
            text = f"TelegramAPI is running Low at this time. Please try again later\n\n{video}",
            parse_mode = ParseMode.MARKDOWN
        )

def main():
    updater = Updater(
        token = '6200080434:AAE_HowNjNOvFzxAu_ffFyYjj0YCln9m_Ec',
        use_context = True,
        request_kwargs = {'read_timeout': 1000, 'connect_timeout': 1000}
    )

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(None, processor))

    updater.start_polling() 
    updater.idle()
    


if __name__ == '__main__':
    log('ONLINE')
    main()
