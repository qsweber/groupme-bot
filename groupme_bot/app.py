import datetime
import operator
import os
import random
import requests

from flask import Flask, request

from groupme_bot.groupme_api_client import get_messages

LOOKBACK = 7

app = Flask(__name__)


def _post_as_bot(text):
    return requests.post(
        'https://api.groupme.com/v3/bots/post',
        data={
            'bot_id': os.environ['GROUPME_BOT_ID'],
            'text': text,
        }
    )


# def _check_double_post(data):
#     if len(data['text'] > 100):
#         lookbacks = [
#             7, 30, 365, 700
#         ]
#         for lookback in lookbacks:
#             messages, user_names = get_messages(
#                 datetime.datetime.now() - datetime.timedelta(days=lookback)
#             )
#     messages_sorted = sorted(
#         [
#             (message, len(message['likers']))
#             for message_id, message in messages.items()
#         ],
#         key=operator.itemgetter(1),
#         reverse=True,
#     )


def _query_leaderboard(data):
    word_after_command = None
    check_next = False
    for word in data.get('text').split():
        if word == 'leaderboard':
            check_next = True
            continue
        if check_next:
            word_after_command = word
            break

    try:
        lookback = int(word_after_command)
    except TypeError:
        lookback = LOOKBACK

    messages, user_names = get_messages(
        datetime.datetime.now() - datetime.timedelta(days=lookback)
    )

    data = {
        username: sum([
            len(message['likers'])
            for message_id, message in messages.items()
            if message['user'] == user_id
        ]) for user_id, username in user_names.items()
    }

    text = '\n'.join([
        '{}: {}'.format(key, val)
        for key, val in sorted(
            data.items(),
            reverse=True,
            key=operator.itemgetter(1),
        )
    ])

    _post_as_bot('here it is for the last {} days:'.format(lookback))
    _post_as_bot(text)


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if data['sender_id'] == os.environ.get('USER_TO_REPEAT'):
        if random.random() > 0.9:
            _post_as_bot(data['text'])

        return 'ok', 200

    if (
        data.get('text').lower().startswith(os.environ['GROUPME_BOT_NAME']) and
        data.get('sender_type') != 'bot'
    ):
        func = None
        for function_name in globals():
            if function_name.startswith('_query_'):
                if function_name.strip('_query_') in data.get('text').lower():
                    func = globals()[function_name]
                    break

        if not func:
            _post_as_bot('Sorry, I can\'t help you with that.')
            return 'ok', 200

        _post_as_bot('Checking {}...'.format(
            func.__name__.strip('_query_')
        ))

        return func(data)

    return "ok", 200
