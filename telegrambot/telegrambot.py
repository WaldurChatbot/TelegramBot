#!/usr/bin/env python
# coding: utf-8

import os
import traceback
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
url = config['backend']['url'] + ':' + config['backend']['port']

log.info("Telegram token: {}".format(obscure(telegram_token)))
log.info("Backend url: {}".format(url))

conn = BackendConnection(url)


def query(bot, update):
    user_id = update.effective_user.id
    message = update.message.text

    response = conn.get_response(message, user_id)
    for item in response:
        if item['type'] == 'text':
            update.message.reply_text(item['data'])
        elif item['type'] == 'graph':
            update.message.reply_photo(photo=make_graph(item['data']))
        else:
            raise Exception("Unknown response type")


def error_callback(bot, update, error):
    try:
        raise error
    except:
        for line in traceback.format_exc().split("\n"): log.error(line)


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
