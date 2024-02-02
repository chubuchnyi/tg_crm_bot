import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dtb.settings')
django.setup()

from telegram import Bot



from tgbot.dispatcher import setup_dispatcher


from telegram.ext import Updater, MessageHandler, Filters
from dtb.settings import TELEGRAM_TOKEN, CRM_CHAT_ID
from users.models import User

def run_polling(tg_token: str = TELEGRAM_TOKEN):
    """ Run bot in polling mode """
    updater = Updater(tg_token, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = Bot(tg_token).get_me()
    bot_link = f"https://t.me/{bot_info['username']}"

    print(f"Polling of '{bot_link}' has started")
    # it is really useful to send '👋' emoji to developer
    # when you run local test
    # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>

    def forward_group_message(update, context):        
        user_chat_id = update.message.message_thread_id
        print("user_chat_id", user_chat_id)
        if user_chat_id is None or user_chat_id == 0:
            print("user_chat_id is None")
            return
        user_id = User.get_topic_user_id(user_chat_id)
        if user_id is None or user_id == 0:
            print("user_id is None")
            return
        try:
            updater.bot.copyMessage(chat_id=user_id, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        except:
            print("Can't forward message to user", str(user_id))
            return
        

    group_message_handler = MessageHandler(Filters.chat_type.groups, forward_group_message)
    dp.add_handler(group_message_handler)

    def forward_user_message(update, context):
        user_id=update.message.from_user.id
        message_thread_id=User.get_user_topic_id(user_id=user_id)
        if message_thread_id is None or message_thread_id == 0:
            print("group_chat_id is None")
            return
        print("group_chat_id", message_thread_id)
      
        try:
            updater.bot.copyMessage(chat_id=CRM_CHAT_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id, message_thread_id = message_thread_id)
        except:
            print("Can't forward message from user", str(user_id))      

    user_message_handler = MessageHandler(Filters.chat_type.private, forward_user_message)
    dp.add_handler(user_message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    run_polling()
