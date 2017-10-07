#!/bin/bash

# the target should already have cloned this repo
cd TelegramBot

# if supplied argument is 'dev', use develop branch
if [ ! -z $1 ]; then
    if [ $1 == "dev" ]; then
        git checkout develop
    else
        git checkout master
    fi
else
    git checkout master
fi

git pull

# install requirements
sudo pip install -r requirements.txt --upgrade

# kill running tgbot
[ -f pid ] && kill `cat pid`

# start processes
cd telegrambot
nohup python3.5 telegrambot.py > /dev/null 2>&1 & echo $! > ../pid
echo "Started telegram bot"

sleep 5

if ps -p `cat ../pid` > /dev/null
then
   echo "`cat ../pid` is running"
   exit 0
else
   echo "Telegram bot is not running"
   exit 100
fi