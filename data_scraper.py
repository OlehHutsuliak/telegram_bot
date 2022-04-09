import requests
from bs4 import BeautifulSoup
from datetime import date

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/51.0.2704.103 ""Safari/537.36 "}


def get_sun_time_data():
    url = 'https://www.sunrise-and-sunset.com/en/sun/poland/krakow'
    page = requests.get(url, headers=headers)

    time_data = BeautifulSoup(page.text, 'html.parser').table.find_all('td')[2:6]

    index = 0
    while index != len(time_data):
        time_data[index] = time_data[index].text.strip()
        index += 1

    sunrise, sunset, timezone, day_length = time_data
    today_date = date.today().strftime('%d %B, %Y')

    suntime_text = f"\U0001F313 Hi, today is {today_date} \U0001F313\n" \
                   f"                sunrise - {sunrise}\n" \
                   f"                 sunset - {sunset}\n" \
                   f"           day length - {day_length}"

    return suntime_text


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

    usd_pln = currency_pair_one_page_element.text[:4]
    eur_pln = currency_pair_two_page_element.text[:4]

    currency_exchange_text = f"   According to the Lord's will\n" \
                             f"               \U0001F640 \U0001F640 \U0001F640\n" \
                             f" \U0001F56F {usd_pln} PLN for 1 USD \U0001F56F\n" \
                             f" \U0001F56F {eur_pln} PLN for 1 EUR \U0001F56F"
    return currency_exchange_text
