#!/usr/bin/env python
# coding: utf-8

from common.request import Connection
from telegram.ext import Updater, MessageHandler, Filters
import logging.config
import logging
from configparser import ConfigParser

logging.config.fileConfig('../logging_config.ini')
log = logging.getLogger(__name__)

log.info("Read configuration")
config = ConfigParser()
config.read('../configuration.ini')
token = config['telegram']['token']
url   = config['backend']['url'] + ':' + config['backend']['port']

conn = Connection(url)


def query(bot, update):
    log.debug("IN: " + update.message.text)
    if update.message.text[:1] == '!':
        message = update.message.text[1:]
        log.info("IN:  " + message)
        response = conn.query(message)
        log.info("OUT: " + response['message'])
        update.message.reply_text(response['message'])


def main():
    log.info("Initializing bot")
    updater = Updater(token)

    dp = updater.dispatcher
    log.info("Adding handlers")
    # responds to any message that starts with '!'
    dp.add_handler(MessageHandler(Filters.text, query))

    log.info("Starting polling")
    updater.start_polling()

    log.info("Bot initialized")
    updater.idle()


if __name__ == '__main__':
    main()
