import requests
from telegram import Update
from bs4 import BeautifulSoup
from datetime import date
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging


def getTimeData():
    # create url
    url = 'https://www.sunrise-and-sunset.com/en/sun/poland/krakow'
    # get page
    page = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, "
                                                    "like Gecko) Chrome/51.0.2704.103 ""Safari/537.36 "})
    html_structure = BeautifulSoup(page.text, 'html.parser')
    table_with_data = html_structure.table.find_all('td')[2:6]
    sunrise_time, sunset_time, day_length_time = \
        table_with_data[0].text, table_with_data[1].text, table_with_data[3].text
    today = date.today().strftime('%d %B, %Y')
    return sunrise_time.strip(), sunset_time.strip(), day_length_time.strip().replace(' ', ':'), today


token = 'TELEGRAM TOKEN'
sunrise, sunset, day_length, today_date = getTimeData()


def suntime(update: Update, context: CallbackContext):
    text_to_send = f"Hi, today is {today_date} \U0001F600\n" \
                   f"sunrise - {sunrise}\n" \
                   f"sunset - {sunset}\n" \
                   f"day length - {day_length}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{text_to_send}")


def main() -> None:
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    # logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    # Add handlers
    dispatcher.add_handler(CommandHandler('suntime', suntime))
    # Start - Stop
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
