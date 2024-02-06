import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from users.models import User
from tgbot.handlers.onboarding.keyboards import make_keyboard_for_start_command
from tgbot.main import bot
from dtb.settings import CRM_CHAT_ID

def command_start(update: Update, context: CallbackContext) -> None:
    user_id = extract_user_data_from_update(update)['user_id']
   
    #check if topic_id == 0
    if User.get_user_topic_id(user_id=user_id) == 0:
        u, created = User.get_user_and_created(update, context)
        text = static_text.start_created.format(first_name=u.first_name)
        chat_id=CRM_CHAT_ID      
        topic = bot.createForumTopic(chat_id=chat_id, name=u.first_name)

        topic_id = topic.message_thread_id
        print ("topic", topic_id)
        if topic_id is not None:
            
            User.set_user_topic_id(user_id=u.user_id, topic_id=topic_id)
            bot.sendMessage(chat_id=chat_id, text="Warm welcom to new user "+u.first_name, message_thread_id=topic_id)
    else:
        text = static_text.start_not_created.format(first_name="Amigo")

    update.message.reply_text(text=text,
                              reply_markup=make_keyboard_for_start_command())


def add_topic(update: Update, context: CallbackContext) -> None:
    # callback_data: ADD_TOPIC_BUTTON variable from manage_data.py
    """ Pressed 'add_topic' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    bot.sendMessage(chat_id=user_id, text="Please enter request")
    
    
def secret_level(update: Update, context: CallbackContext) -> None:
    # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = static_text.unlock_secret_room.format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML
    )