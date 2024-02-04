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
        #chek if message has message_thread_id
        #check if message has field message_thread_id
        print("message from groupe:", update.message)
        if not hasattr(update.message, 'message_thread_id'):
            print("update.message.message_thread_id is None")
            return
        if update.message.message_thread_id is None:
            print("update.message.message_thread_id is None")
            return     
        # if not hasattr(update.message, 'animation'):
        #     print("update.message.animation is None")
        #     return
        # if update.message.animation is not None:
        #     print("update.message.animation is not None")
        #     return
        user_chat_id = update.message.message_thread_id
        print("user_chat_id", user_chat_id)
        if user_chat_id is None or user_chat_id == 0 or user_chat_id == 1:
            print("user_chat_id is ", str(user_chat_id))
            return
        user_id = User.get_topic_user_id(user_chat_id)
        if user_id is None or user_id == 0:
            print("user_id is None")
            return
        #check if message has member chat_id and it is not None
        if not hasattr(update.message, 'chat_id'):
            print("update.message.chat_id is None")
            return
        if update.message.chat_id is None:
            print("update.message.chat_id is None")
            return
        if not hasattr(update.message, 'message_id'):
            print("update.message.message_id is None")
            return
        if update.message.message_id is None:
            print("update.message.message_id is None")
            return
        
        # try:
            #updater.bot.send_message(chat_id=user_id, text=update.message.text)
                
            #updater.bot.forward_message(chat_id=user_id, from_chat_id=update.message.chat_id, message_id=update.message.message_id, protect_content=True)
        updater.bot.copyMessage(chat_id=user_id, from_chat_id=update.message.chat_id, message_id=update.message.message_id, protect_content=True)
        # except:
            # print("Can't forward message to user", str(user_id), "from chat", str(update.message.chat_id), "message_id", str(update.message.message_id))
            # return
            # гифки и локации убивают базу пользователя

    group_message_handler = MessageHandler(Filters.chat_type.groups & Filters.chat_id(CRM_CHAT_ID), forward_group_message, run_async=True)
    dp.add_handler(group_message_handler)

    def forward_user_message(update, context):
        print("message from user", update.message)
        if not hasattr(update.message, 'from_user'):
            print("update.message.from_user is None")
            return
        if update.message.from_user is None:
            print("update.message.from_user is None")
            return
        if not hasattr(update.message.from_user, 'id'):
            print("update.message.from_user.id is None")
            return
        if update.message.from_user.id is None:
            print("update.message.from_user.id is None")
            return
        # if not hasattr(update.message, 'animation'):
        #     print("update.message.animation is None")
        #     return
        # if update.message.animation is not None:
        #     print("update.message.animation is not None")
        #     return
        user_id=update.message.from_user.id
        message_thread_id=User.get_user_topic_id(user_id=user_id)
        if message_thread_id is None or message_thread_id == 0 or message_thread_id == 1:
            print("group_chat_id is None")
            return
        if user_id is None or user_id == 0 or user_id == 1:
            print("user_id is None")
            return
        print("group_chat_id", message_thread_id, "user_id", user_id, "message", str(update.message.text))
        if not hasattr(update.message, 'message_id'):
            print("update.message.message_id is None")
            return
        if update.message.message_id is None:
            print("update.message.message_id is None")
            return
        try:
            #updater.bot.send_message(chat_id=CRM_CHAT_ID, text=update.message.text, message_thread_id = message_thread_id)
            #updater.bot.forward_message(chat_id=CRM_CHAT_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id, protect_content=True, message_thread_id = message_thread_id)
            updater.bot.copyMessage(chat_id=CRM_CHAT_ID, from_chat_id=user_id, message_id=update.message.message_id, protect_content=True, message_thread_id = message_thread_id)
        except:
            print("Can't forward message from user", str(user_id), "to chat", str(CRM_CHAT_ID), "message_id", str(update.message.message_id), "message_thread_id", str(message_thread_id))    

    user_message_handler = MessageHandler(Filters.chat_type.private, forward_user_message, run_async=True)
    dp.add_handler(user_message_handler)

    # def forward_gif(update, context):
    #     print("update.message", update.message)
    #     user_id = update.message.from_user.id

    #     # Check if the message contains a GIF
    #     if update.message.animation:
    #         gif = update.message.animation.file_id

    #         # Forward the GIF to the user
    #         context.bot.send_animation(chat_id=user_id, animation=gif)

    # gif_message_handler = MessageHandler( Filters.animation & Filters.chat_type.groups, forward_gif,run_async=True)
    # dp.add_handler(gif_message_handler)




    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    run_polling()
