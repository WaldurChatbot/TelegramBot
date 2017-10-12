#!/usr/bin/env python
# coding: utf-8

from configparser import ConfigParser
from telegram.ext import Updater, MessageHandler, Filters
import __init__ as init
from common.request import BackendConnection, InvalidTokenException


log = init.getLogger(__name__)

log.info("Read configuration")
config = ConfigParser()
config.read('../configuration.ini')
telegram_token = config['telegram']['token']
url   = config['backend']['url'] + ':' + config['backend']['port']

conn = BackendConnection(url)

tokens = {}


def query(bot, update):
    user_id = update.effective_user.id
    token = None if user_id not in tokens else tokens.get(user_id)

    log.debug("user_id: "  + str(user_id) + " token: " + str(token))
    log.debug("IN: " + update.message.text)
    if update.message.text[:1] == '!':
        message = update.message.text[1:]
        log.info("IN:  " + message)
        try:
            response = conn.query(
                q=message,
                token=token
            )
            response = response['message']
        except InvalidTokenException:
            log.info("Needed token to query Waldur, asking user for token.")
            response = "Needed token to query Waldur API. " \
                       "Token was either invalid or missing. " \
                       "Please send token like this '?<TOKEN>'"

        update.message.reply_text(response)
        log.info("OUT: " + response)
    elif update.message.text[:1] == '?':
        log.info("Received token from user " + str(user_id) + " with a length of " + str(len(update.message.text[1:])))
        tokens[user_id] = update.message.text[1:]
        update.message.reply_text("Thanks")


def main():
    log.info("Initializing bot")
    updater = Updater(telegram_token)

    dp = updater.dispatcher
    log.info("Adding handlers")
    # responds to any message that starts with '!'
    dp.add_handler(MessageHandler(Filters.text, query))
    # todo add error handler
    log.info("Starting polling")
    updater.start_polling()

    log.info("Bot initialized")
    updater.idle()


if __name__ == '__main__':
    main()
