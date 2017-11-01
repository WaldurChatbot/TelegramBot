#!/usr/bin/env python
# coding: utf-8

from configparser import ConfigParser
from logging import getLogger
from logging.config import fileConfig
from os import path

log_file_path = path.join(path.dirname(path.abspath(__file__)), '..', 'logging_config.ini')
fileConfig(log_file_path)
log = getLogger(__name__)
# logger must be loaded before the following imports, otherwise no logging from them
from common.request import BackendConnection
import traceback
from common.utils import obscure
from telegram.ext import Updater, MessageHandler, Filters


log.info("Read configuration")
config = ConfigParser()
config.read('../configuration.ini')
telegram_token = config['telegram']['token']
url   = config['backend']['url'] + ':' + config['backend']['port']
log.info("Telegram token: {}".format(obscure(telegram_token)))
log.info("Backend url: {}".format(url))

conn = BackendConnection(url)


def query(bot, update):
    user_id = update.effective_user.id
    message = update.message.text

    response = conn.get_response(message, user_id)
    for item in response:
        if item['type'] == 'text':
            message = item['data']
        elif item['type'] == 'graph':
            message = "this should be a graph"
            # todo get graph id and make graph
        else:
            raise Exception("Unknown response type")

        if response is not None:
            update.message.reply_text(message)


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

    log.info("Starting polling")
    updater.start_polling()

    log.info("Bot initialized")
    updater.idle()


if __name__ == '__main__':
    main()
