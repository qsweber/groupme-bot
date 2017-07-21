# Groupme Bot

This is a Groupme Bot that determines who in a group chat has received the
most likes on their posts. It is invoked by mentioning the name of the bot
and asking "who is in the lead".

# Setup

## Create the bot on the Groupme Website

Follow this tutorial. For now, leave the `Callback URL` blank.

## Clone this repo

    git clone https://github.com/qsweber/groupme-bot.git

## Configure a heroku app

Begin by changing to the local directory of this repo

    cd groupme-bot

Ensure you are logged into heroku

    heroku login

Create the heroku app. This will print out the URL for accessing the app. This
is the URL we will use on the GroupMe bot registration page.

    heroku create

## Add environment variables to heroku app

    heroku config:set GROUPME_BOT_ID="<from GroupMe bot registration>"
    heroku config:set GROUPME_GROUP_NAME="<name of GroupMe group>"
    heroku config:set GROUPME_TOKEN="<GroupMe developer token>"

## Deploy app

    git push --set-upstream heroku master

## Set the callback URL on GroupMe bot

    Copy the Heroku app URL onto the GroupMe bot registration page

# Usage

For now, the only supported feature is asking for who has the most likes.
To do so, simply type `leader` into your GroupMe chat.

# Future Work

Support multiple queries.
