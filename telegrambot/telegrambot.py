#!/usr/bin/env python
# coding: utf-8

import os
from configparser import ConfigParser
from logging import getLogger
from logging.config import fileConfig

fileConfig("../logging_config.ini")
log = getLogger(__name__)

# logger must be loaded before the following imports, otherwise no logging from them
from common.request import BackendConnection
from common.utils import obscure
from telegram.ext import Updater, MessageHandler, Filters
from common.graphs import make_graph

# If config file location is setup in environment variables
# then read conf from there, otherwise from project root
if 'WALDUR_CONFIG' in os.environ:
    config_path = os.environ['WALDUR_CONFIG']
else:
    config_path = '../configuration.ini'


log.info("Reading configuration from {}".format(config_path))
config = ConfigParser()
config.read(config_path)

telegram_token = config['telegram']['token']
backend_url = config['backend']['url'] + ':' + config['backend']['port']

auth_url = config['auth']['url']
if config['auth']['port'] != '80':
    auth_url += ':' + config['auth']['port']

log.info("Telegram token: {}".format(obscure(telegram_token)))
log.info("Backend url: {}".format(backend_url))
log.info("Auth url: {}".format(auth_url))

conn = BackendConnection(backend_url, auth_url)


def query(bot, update):
    user_id = update.effective_user.id
    message = update.message.text

    prefix = message[0]
    if prefix == '!':
        response = conn.get_response(message[1:], user_id)
    elif prefix == '?':
        response = conn.set_token(message[1:], user_id)
    else:
        response = []

    for item in response:
        if item['type'] == 'text':
            update.message.reply_text(item['data'])
        elif item['type'] == 'graph':
            update.message.reply_photo(photo=make_graph(item['data']))
        else:
            raise Exception("Unknown response type")


def error_callback(bot, update, error):
    log.exception("Error from update: {}".format(update))
    log.exception(error)


def main():
    log.info("Initializing bot")
    updater = Updater(telegram_token)

    log.info("Adding handlers")
    updater.dispatcher.add_handler(MessageHandler(Filters.text, query))
    updater.dispatcher.add_error_handler(error_callback)

    log.info("Starting polling")
    updater.start_polling()

    log.info("Bot initialized")
    updater.idle()


if __name__ == '__main__':
    main()
