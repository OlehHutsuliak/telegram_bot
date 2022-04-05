import requests
from telegram import Update
from bs4 import BeautifulSoup
from datetime import date
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging
import os

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/51.0.2704.103 ""Safari/537.36 "}
token = os.environ["TOKEN"]


def get_sun_time_data():
    url = 'https://www.sunrise-and-sunset.com/en/sun/poland/krakow'
    page = requests.get(url, headers=headers)

    time_data = BeautifulSoup(page.text, 'html.parser').table.find_all('td')[2:6]

    index = 0
    while index != len(time_data):
        time_data[index] = time_data[index].text.strip()
        index += 1

    sunrise_time, sunset_time, timezone, day_length_time = time_data
    today = date.today().strftime('%d %B, %Y')

    return sunrise_time, sunset_time, day_length_time.replace(' ', ':'), today


def currency_course():
    amount = "1"
    sell = ["USD", "EUR"]
    buy = "PLN"
    url_usd_pln = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={sell[0]}&To={buy}"
    url_eur_pln = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={sell[1]}&To={buy}"

    # Get pages
    currency_pair_one_page = requests.get(url_usd_pln, headers=headers)
    currency_pair_two_page = requests.get(url_eur_pln, headers=headers)

    currency_pair_one_page_element = BeautifulSoup(currency_pair_one_page.text, 'html.parser').main.find_all('p')[1]
    currency_pair_two_page_element = BeautifulSoup(currency_pair_two_page.text, 'html.parser').main.find_all('p')[1]

    usd_to_pln = currency_pair_one_page_element.text[:4]
    eur_to_pln = currency_pair_two_page_element.text[:4]

    return usd_to_pln, eur_to_pln


def start(update: Update, context: CallbackContext):
    text_to_send = f"Hi, {update.effective_user.username}. I see, you  are new here. Let's check how I can help you."
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_to_send)


def suntime(update: Update, context: CallbackContext):
    text_to_send = f"Hi, today is {today_date} \U0001F600\n" \
                   f"sunrise - {sunrise}\n" \
                   f"sunset - {sunset}\n" \
                   f"day length - {day_length}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_to_send)


def currency_exchange(update: Update, context: CallbackContext):
    text_to_send = f"Today God gives us:\n" \
                   f"        \U0001F928 just \U0001F928\n" \
                   f"{usd_pln} PLN for 1 USD\n" \
                   f"{eur_pln} PLN for 1 EUR"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_to_send)


sunrise, sunset, day_length, today_date = get_sun_time_data()
usd_pln, eur_pln = currency_course()


def main() -> None:
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    # logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    # Add handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('suntime', suntime))
    dispatcher.add_handler(CommandHandler('currency', currency_exchange))
    # Start - Stop
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
