# Groupme Bot

[![Build Status](https://travis-ci.org/qsweber/groupme-bot.svg?branch=master)](https://travis-ci.org/qsweber/groupme-bot) [![Coverage Status](https://coveralls.io/repos/github/qsweber/groupme-bot/badge.svg?branch=master)](https://coveralls.io/github/qsweber/groupme-bot?branch=master)

This is a Groupme Bot created primarily for determining who in a group chat has received the
most likes on their posts. The full set of behaviors is listed below.

# Setup

## Create a bot on the Groupme Website

Follow this tutorial. For now, leave the `Callback URL` blank.

## Clone this repo

    git clone https://github.com/qsweber/groupme-bot.git

## Create a heroku app

Begin by changing to the local directory of this repo

    cd groupme-bot

Ensure you are logged into heroku

    heroku login

Create the heroku app. This will print out the URL for accessing the app. This
is the URL we will use on the GroupMe bot registration page.

    heroku create

## Set required environment variables

    heroku config:set GROUPME_BOT_ENABLED="<switch for turning bot on and off>"
    heroku config:set GROUPME_BOT_ID="<from GroupMe bot registration site>"
    heroku config:set GROUPME_BOT_NAME="<from GroupMe bot registration site>"
    heroku config:set GROUPME_GROUP_NAME="<switch for turning bot on and off>"
    heroku config:set GROUPME_TOKEN="<GroupMe developer token>"

## Deploy app

    git push --set-upstream heroku master

## Set the callback URL on GroupMe bot

    Copy the Heroku app URL onto the GroupMe bot registration page

# Behaviors

## Leaderboard

    <bot name> leaderboard <number of days to lookback>

This will pull all of the data going back the specified number of days and return an ordered list of likes by username.

![leaderboard](/../screenshots/leaderboard.png?raw=true "leaderboard")

## Double Post Check

A frequent cause of tension in GroupMe is when somebody posts an article that has already been posted. This bot will constantly monitor for those situations and immediately reprimand any violators.

![doublepost](/../screenshots/doublepost.png?raw=true "doublepost")
