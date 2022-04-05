import datetime
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import logging
from variables import Variables as V

redis_connection = V.redis_connection
db_keys = redis_connection.keys(pattern='*')


def start(update: Update, context: CallbackContext):
    user_name = update.message.from_user.name
    if user_name is None:
        user_name = update.message.from_user.full_name
    start_text = f"Hi, {user_name} \U0001F60A"
    user_id = update.message.from_user.id
    redis_connection.set(user_name, user_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_text)


def suntime(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=V.suntime_text)


def currency_exchange(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=V.currency_exchange_text)


def message_filter(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=V.message_filter_text)


def sun_daily_alert(context: CallbackContext):
    for keys in db_keys:
        chat_id_value = redis_connection.get(keys).decode("UTF-8")
        context.bot.send_message(chat_id=chat_id_value, text=V.suntime_text)


def currency_daily_alert(context: CallbackContext):
    for keys in db_keys:
        chat_id_value = redis_connection.get(keys).decode("UTF-8")
        context.bot.send_message(chat_id=chat_id_value, text=V.currency_exchange_text)


def main() -> None:
    updater = Updater(token=V.token)
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

    job.run_daily(sun_daily_alert, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=9, minute=00, second=00))  # UTC
    job.run_daily(currency_daily_alert, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=8, minute=30, second=00))

    # Start - Stop
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
