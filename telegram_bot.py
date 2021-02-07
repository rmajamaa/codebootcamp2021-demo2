from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
import os
import json
import pytz
import requests
import datetime
from datetime import timedelta, datetime
import dotenv
from dotenv import load_dotenv
load_dotenv()


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        f'Hello, {update.effective_user.first_name}! I am wishing you a pleasent day!')


def weather(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Please tell me the city name you would like to know the current weather for.')


def location(update: Update, context: CallbackContext) -> None:
    location_received = update.message.text

    degree_sign = u'\N{DEGREE SIGN}'

    api_key = os.environ['OPEN_WEATHER_TOKEN']
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = location_received
    complete_url = base_url + "&q=" + city_name + \
        "&&units=metric" + "&appid=" + api_key
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] == 200:
        y = x['main']
        current_temperature = y["temp"]
        feels_like = y["feels_like"]
        z = x["weather"]
        weather_description = z[0]["description"]

        w = x["wind"]
        wind_speed = w["speed"]
        wind_direction = w["deg"]
        wind_direction_text = degrees_to_cardinal(int(wind_direction))

        s = x["sys"]
        sun_rise = s["sunrise"]
        sun_set = s["sunset"]

        country_code = s['country']
        weather_city = x['name']
        sun_rise_unix_time = s["sunrise"]
        finland = pytz.timezone('Europe/Helsinki')
        gmt = pytz.timezone('GMT')
        my_sun_rise_timezone = datetime.utcfromtimestamp(sun_rise_unix_time)
        my_sun_rise_timezone = gmt.localize(my_sun_rise_timezone)
        my_sun_rise_timezone_finland = my_sun_rise_timezone.astimezone(finland)

        sun_set_unix_time = s["sunset"]
        finland = pytz.timezone('Europe/Helsinki')
        gmt = pytz.timezone('GMT')
        my_sun_set_timezone = datetime.utcfromtimestamp(sun_set_unix_time)
        my_sun_set_timezone = gmt.localize(my_sun_set_timezone)
        my_sun_set_timezone_finland = my_sun_set_timezone.astimezone(finland)

        update.message.reply_text("The current weather for " + str(weather_city) + ", " + str(country_code)
                                  + "\nTemperature: " + str(current_temperature) + str(degree_sign) + "C" + "\nFeels like: " + str(feels_like) + str(degree_sign) + "C" +
                                  "\nDescription: " + str(weather_description) + "\nWind speed: " + str(wind_speed) + " m/s" + "\nWind direction: " + str(wind_direction_text) + "\nSunrise: " + str(my_sun_rise_timezone_finland.strftime("%d-%m-%Y %H:%M")) + "\nSunset: " + str(my_sun_set_timezone_finland.strftime("%d-%m-%Y %H:%M")))
    else:
        update.message.reply_text(
            "I am so sorry! I could not find that city. Please try a different city, or perhaps try adding the country code after the city name, e.g. Manchester, US ")


def degrees_to_cardinal(angle):
    directions = ["North ↓", "North East ↙", "East ←", "South East ↖",
                  "South ↑", "South West ↗", "West →", "North West ↘"]
    ix = int((angle + 22.5) / 45)
    return directions[ix % 8]


updater = Updater(os.environ['TELEGRAM_BOT_TOKEN'])
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('hello', hello))
dispatcher.add_handler(CommandHandler('weather', weather))
dispatcher.add_handler(MessageHandler(Filters.text, location))

updater.start_polling()
updater.idle()
