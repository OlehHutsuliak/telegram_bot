import datetime
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
import logging
import telebot
from telebot import types
from data_scraper import get_sun_time_data, currency_course
import os
import redis

token = os.environ["TOKEN"]
redis_connection = redis.from_url(os.environ["REDIS_URL"])

db_keys = redis_connection.keys(pattern='*')
bot = telebot.TeleBot(token)


def start(update: Update, context: CallbackContext):
    user_name = update.message.from_user.full_name
    if user_name is None:
        user_name = update.message.from_user.name
    start_text = f"Hi, {user_name} \U0001F60A"
    user_id = update.message.from_user.id
    redis_connection.set(user_name, user_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_text)


def suntime(update: Update, context: CallbackContext):
    suntime_text = get_sun_time_data()
    context.bot.send_message(chat_id=update.effective_chat.id, text=suntime_text)


def currency_exchange(update: Update, context: CallbackContext):
    currency_exchange_text = currency_course()
    context.bot.send_message(chat_id=update.effective_chat.id, text=currency_exchange_text)


def message_filter(update: Update, context: CallbackContext):
    message_filter_text = "This Bot doesn't receive messages. Please select one of available commands below"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("SunTime", callback_data='suntime'))
    markup.add(types.InlineKeyboardButton("Currency Exchange", callback_data='currency_exchange'))
    bot.send_message(chat_id=update.effective_chat.id, text=message_filter_text, reply_markup=markup)


def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    selected_button = query.data

    if selected_button == 'suntime':
        suntime(update, context)
    if selected_button == 'currency_exchange':
        currency_exchange(update, context)


def sun_daily_alert(context: CallbackContext):
    suntime_text = get_sun_time_data()
    for keys in db_keys:
        chat_id_value = redis_connection.get(keys).decode("UTF-8")
        context.bot.send_message(chat_id=chat_id_value, text=suntime_text)


def currency_daily_alert(context: CallbackContext):
    currency_exchange_text = currency_course()
    for keys in db_keys:
        chat_id_value = redis_connection.get(keys).decode("UTF-8")
        context.bot.send_message(chat_id=chat_id_value, text=currency_exchange_text)


def main() -> None:
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    job = updater.job_queue

    # logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    # Add handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('suntime', suntime))
    dispatcher.add_handler(CommandHandler('currency', currency_exchange))
    dispatcher.add_handler(MessageHandler(Filters.update & (~Filters.command), message_filter))
    dispatcher.add_handler(CallbackQueryHandler(button))

    job.run_daily(sun_daily_alert, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=6, minute=00, second=00))  # UTC
    job.run_daily(currency_daily_alert, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=6, minute=40, second=00))

    # Start - Stop
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
