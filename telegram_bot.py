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
"""Loading the value keys for OPEN_WEATHER_TOKEN and TELEGRAM_BOT_TOKEN from the .env file"""


def start(update: Update, context: CallbackContext):
    """
    Function receives a '/start' message from the Telegram bot, 
    picks up the sender's first name and returns a simple greeting
    """
    update.message.reply_text(
        f'Hello, {update.effective_user.first_name}! I am wishing you a pleasent day!')


def weather(update: Update, context: CallbackContext):
    """
    Function invites the user to provide a city name after receiving a '/weather' command
    """
    update.message.reply_text(
        'Please tell me the city name you would like to know the current weather for.')


def location(update: Update, context: CallbackContext):
    """
    Funtion listens what the user has typed in, and after receiving a valid city name, 
    replies with the current weather message for that city.
    """

    location_received = update.message.text
    """Storing the value for the city name"""

    api_key = os.environ['OPEN_WEATHER_TOKEN']
    base_url = 'http://api.openweathermap.org/data/2.5/weather?&q='
    city_name = location_received
    complete_url = base_url + city_name + '&&units=metric' + '&appid=' + api_key
    """Compiling the URL for OwnWeatherMap API"""

    response = requests.get(complete_url)
    """Sending a request to the OpenWeatherMap API and receiving a JSON response"""

    owm_reply = response.json()
    """The JSON response"""

    if owm_reply['cod'] == 200:
        """
        After receiving a successful response (status code = 200) from the API,
        the JSON response is parsed
        """
        temperature = owm_reply['main']
        current_temperature = temperature['temp']
        feels_like = temperature['feels_like']
        descr = owm_reply['weather']
        weather_description = descr[0]['description']

        wind = owm_reply['wind']
        wind_speed = wind['speed']
        wind_direction = wind['deg']
        wind_direction_text = degrees_to_cardinal(int(wind_direction))
        """The 'degrees_to_cardinal' function defined below converts degrees into cardinal directions"""

        sun = owm_reply['sys']
        sun_rise = sun['sunrise']
        sun_set = sun['sunset']

        country_code = sun['country']
        weather_city = owm_reply['name']

        sun_rise_unix_time = sun['sunrise']
        finland = pytz.timezone('Europe/Helsinki')
        gmt = pytz.timezone('GMT')
        my_sun_rise_timezone = datetime.utcfromtimestamp(sun_rise_unix_time)
        my_sun_rise_timezone = gmt.localize(my_sun_rise_timezone)
        my_sun_rise_timezone_finland = my_sun_rise_timezone.astimezone(finland)
        """Converting Unix timestamp into local time using PYTZ"""

        sun_set_unix_time = sun['sunset']
        finland = pytz.timezone('Europe/Helsinki')
        gmt = pytz.timezone('GMT')
        my_sun_set_timezone = datetime.utcfromtimestamp(sun_set_unix_time)
        my_sun_set_timezone = gmt.localize(my_sun_set_timezone)
        my_sun_set_timezone_finland = my_sun_set_timezone.astimezone(finland)
        """Converting Unix timestamp into local time using PYTZ"""

        degree_sign = u'\N{DEGREE SIGN}'
        """Degree sign for the weather message temperatures"""

        update.message.reply_text('The current weather for ' + str(weather_city) + ', ' + str(country_code)
                                  + '\nTemperature: ' + str(current_temperature) + str(degree_sign) + 'C' + '\nFeels like: ' + str(feels_like) + str(degree_sign) + 'C' +
                                  '\nDescription: ' + str(weather_description) + '\nWind speed: ' + str(wind_speed) + ' m/s' + '\nWind direction: ' + str(wind_direction_text) + '\nSunrise: ' + str(my_sun_rise_timezone_finland.strftime('%d-%m-%Y %H:%M')) + '\nSunset: ' + str(my_sun_set_timezone_finland.strftime('%d-%m-%Y %H:%M')))
        """Compiling the weather message for the Telegram bot"""

    else:
        """If the listerer function was not able to receive a valid city name in response"""
        update.message.reply_text(
            'I am so sorry! I could not find that city. Please try a different city, or perhaps try adding the country code after the city name, e.g. Manchester, US ')


def degrees_to_cardinal(angle):
    """Function converts degrees from the wind direction into cardinal directions"""
    directions = ['North ↓', 'North East ↙', 'East ←', 'South East ↖',
                  'South ↑', 'South West ↗', 'West →', 'North West ↘']
    ix = int((angle + 22.5) / 45)
    return directions[ix % 8]


def main():
    """Defing the program execution commands"""

    updater = Updater(os.environ['TELEGRAM_BOT_TOKEN'])
    dispatcher = updater.dispatcher
    """Creating updater and dispatcher"""

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('weather', weather))
    dispatcher.add_handler(MessageHandler(Filters.text, location))
    """Adding the Telegram bot handlers"""

    updater.start_polling()
    """Bot will start polling for any chat updates on Telegram"""
    updater.idle()
    """Will stop the bot gracefully"""


if __name__ == '__main__':
    main()
