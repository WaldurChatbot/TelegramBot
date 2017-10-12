#!/usr/bin/env python
# coding: utf-8

from configparser import ConfigParser
from telegram.ext import Updater, MessageHandler, Filters
import __init__ as init
from common.request import BackendConnection


log = init.getLogger(__name__)

log.info("Read configuration")
config = ConfigParser()
config.read('../configuration.ini')
telegram_token = config['telegram']['token']
url   = config['backend']['url'] + ':' + config['backend']['port']

conn = BackendConnection(url)


def query(bot, update):
    user_id = update.effective_user.id
    message = update.message.text

    response = conn.get_response(message, user_id)

    if response is not None:
        update.message.reply_text(response)


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
