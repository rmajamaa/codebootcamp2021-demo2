Module telegram_bot
===================

Functions
---------

    
`degrees_to_cardinal(angle)`
:   Function converts degrees from the wind direction into cardinal directions

    
`location(update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext)`
:   Funtion listens what the user has typed in, and after receiving a valid city name, 
    replies with the current weather message for that city.

    
`main()`
:   Defing the program execution commands

    
`start(update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext)`
:   Function receives a '/start' message from the Telegram bot, 
    picks up the sender's first name and returns a simple greeting

    
`weather(update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext)`
:   Function invites the user to provide a city name after receiving a '/weather' command