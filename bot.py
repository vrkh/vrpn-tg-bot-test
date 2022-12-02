import telebot
import database
from telebot import types
from config import TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    user_tuple = (telegram_id, username, firstname, lastname)

    user_in_db = database.select_user(telegram_id)
    if user_in_db:
        if user_in_db == user_tuple:
            pass
        else:
            database.update_user(user_tuple)
    else:
        database.insert_into_user(user_tuple)
        bot.send_message(message.chat.id, f'добро пожаловать, {firstname}!')
        
    
    markup = types.InlineKeyboardMarkup()
    personal_account_button = types.InlineKeyboardButton('🏠 личный кабинет', callback_data='personal_account')
    markup.add(personal_account_button)
    bot.send_message(
        message.chat.id, 
        '*откройте доступ к свободному интернету*\n\n🌐 используйте instagram, twitter, facebook и другие экстремистские соцсети\. ~ну и pornhub~ \n\n🚀 летайте по нужным ресурсам без рекламы\n\n🥸 сохраняйте анонимность для самых важных дел', 
        parse_mode="MarkdownV2",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'personal_account':
            tg_id = call.message.chat.id
            accesskey_tuple = database.select_all_from_accesskey(tg_id)
            try:
                accesskey = accesskey_tuple[2]
            except TypeError:
                accesskey = None

            sub_end_date_tuple = database.select_from_subcription_by_id(tg_id)
            try:
                sub_end_date = sub_end_date_tuple[2]
            except TypeError:
                sub_end_date = None

            markup = types.InlineKeyboardMarkup()
            manual = types.InlineKeyboardButton('🧻 инструкция', callback_data='manual')
            start_message = types.InlineKeyboardButton('🔙 назад', callback_data='start_message')
            send_access_key = types.InlineKeyboardButton('🔑 отправить ключ доступа', callback_data='send_access_key')
            markup.add(send_access_key)
            markup.add(manual, start_message)
            
            bot.edit_message_text(
                chat_id = call.message.chat.id, 
                message_id=call.message.id,
                text = f'личный кабинет\n{call.message.chat.first_name}\n\n🔑 ключ доступа\n{accesskey}\n\n📅 конец подписки:\n{sub_end_date}',
                parse_mode="Markdown",
                reply_markup=markup,
            )
        elif call.data == 'start_message':
            markup = types.InlineKeyboardMarkup()
            personal_account_button = types.InlineKeyboardButton('🏠 личный кабинет', callback_data='personal_account')
            markup.add(personal_account_button)
            bot.edit_message_text(
                chat_id=call.message.chat.id, 
                message_id=call.message.id,
                text='*откройте доступ к свободному интернету*\n\n🌐 используйте instagram, twitter, facebook и другие экстремистские соцсети\. ~ну и pornhub~ \n\n🚀 летайте по нужным ресурсам без рекламы\n\n🥸 сохраняйте анонимность для самых важных дел',
                parse_mode="MarkdownV2",
                reply_markup=markup
            )
        elif call.data == 'manual':
            markup = types.InlineKeyboardMarkup()
            send_access_key = types.InlineKeyboardButton('🔑 отправить ключ доступа', callback_data='send_access_key')
            back = types.InlineKeyboardButton('🔙 назад', callback_data='personal_account')
            markup.add(send_access_key)
            markup.add(back)
            bot.edit_message_text(
                chat_id=call.message.chat.id, 
                message_id=call.message.id,
                text='*инструкция*\n\n1. скачать outline из [google play](https://play.google.com/store/apps/details?id=org.outline.android.client) или [app store](https://apps.apple.com/us/app/outline-app/id1356177741)\n\n2. скопировать ключ доступа\n\n3. перейти в outline -> добавить сервер -> вставить ваш ключ\n\n4. profit',
                parse_mode="Markdown",
                reply_markup=markup
            )
        elif call.data == 'send_access_key':
            tg_id = call.message.chat.id
            accesskey_tuple = database.select_all_from_accesskey(tg_id)
            access_key = accesskey_tuple[2]
            if accesskey_tuple:
                bot.send_message(tg_id, text=access_key)
            else:
                bot.send_message(tg_id, text='у вас нет ключа доступа😢')


@bot.message_handler(commands=['access_key'])
def access_key(message: types.Message):
    tg_id = message.chat.id
    accesskey_tuple = database.select_all_from_accesskey(tg_id)
    access_key = accesskey_tuple[2]
    bot.send_message(message.chat.id, text=access_key)



bot.polling()